"""agents.agent

Core agent implementation for the VoyageVerse project.

This module contains a lightweight orchestrator that uses an LLM to call
tooling for flight and hotel lookups and to render email-friendly HTML
summaries. The implementation and system prompts were updated to align
with the VoyageVerse project report: include personalization, cost
optimization guidance, real-time update awareness (weather, delays,
local events), and privacy-preserving instructions (avoid leaking
sensitive payment or full-user identifiers in generated outputs).

Keywords: Unified Travel Platform, AI-Driven Recommendations, Real-Time Analytics,
Dynamic Itinerary Optimization, Collaborative Filtering
"""


# pylint: disable = http-used,print-used,no-self-use

import datetime
import operator
import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from agents.privacy.masking import mask_pii, mask_pii_in_obj
from agents.security.intent_filter import is_malicious, sanitize

from agents.tools.flights_finder import flights_finder
from agents.tools.hotels_finder import hotels_finder
from agents.tools.weather import weather_tool
from agents.tools.flight_status import flight_status_tool
from agents.itinerary.itinerary_builder import itinerary_builder

_ = load_dotenv()

CURRENT_YEAR = datetime.datetime.now().year


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


PROJECT_METADATA = {
    'title': 'VoyageVerse - Unified AI-Driven Travel Platform',
    'abstract': (
        'VoyageVerse proposes an integrated AI-driven platform that consolidates '
        'flight/hotel bookings, itinerary generation, local recommendations, and '
        'real-time updates into a single interface. Leverages LLMs and predictive '
        'analytics to personalize travel plans, integrate live data, and optimize costs.'
    ),
    'keywords': ['Unified Travel Platform', 'AI-Driven Recommendations', 'Real-Time Analytics',
                 'Dynamic Itinerary Optimization', 'Collaborative Filtering']
}


TOOLS_SYSTEM_PROMPT = f"""You are a smart travel agency assistant working for VoyageVerse.
    Use the tools to look up flight and hotel information when appropriate.
    You are allowed to make multiple calls (either together or in sequence).
    Only look up information when you are reasonably certain of the tool arguments.
    The current year is {CURRENT_YEAR}.

    Requirements derived from the project specification:
    - Personalization: tailor recommendations to user preferences (budget, food, accessibility,
      preferred airlines/hotel classes, dates).
    - Cost optimization: when possible, present price breakdowns (rate per night, taxes, fees,
      total cost) and suggest lower-cost alternatives if cost savings are meaningful.
    - Real-time awareness: mention if data could be affected by live variables (weather, flight
      delays, local events) and recommend re-checking bookings if relevant.
    - Privacy: never include raw payment details, full credit card numbers, or other sensitive
      personal identifiers in the output. When sending emails or reports, mask or omit such data.
    - Links & logos: include booking links and vendor logos when available; include currency codes
      and clear price annotations.

    Output format guidance:
    - Include explicit price information and currency (e.g., Rate: $581 per night, Total: $3,488 USD).
    - Provide booking links for flights and hotels when possible, and include image URLs for logos
      if available.
    - If you call tools, return tool_call objects according to the tool schema; otherwise produce
      a human-readable summary that follows the above rules.
    """


TOOLS = [flights_finder, hotels_finder, weather_tool, flight_status_tool, itinerary_builder]


EMAILS_SYSTEM_PROMPT = """Your task is to convert structured markdown-like text into a valid HTML email body.

- Do not include a ```html preamble in your response.
- The output should be in proper HTML format, ready to be used as the body of an email.
- Privacy: do not include any full payment details, passwords, or unmasked personally-identifiable
  information in the email body. Mask or omit sensitive fields.
- Where prices are shown, include currency codes and a total breakdown (per-night, taxes, fees, total).

Here is an example:
<example>
Input:

I want to travel to New York from Madrid from October 1-7. Find me flights and 4-star hotels.

Expected Output:

<!DOCTYPE html>
<html>
<head>
    <title>Flight and Hotel Options</title>
</head>
<body>
    <h2>Flights from Madrid to New York</h2>
    <ol>
        <li>
            <strong>American Airlines</strong><br>
            <strong>Departure:</strong> Adolfo Suárez Madrid–Barajas Airport (MAD) at 10:25 AM<br>
            <strong>Arrival:</strong> John F. Kennedy International Airport (JFK) at 12:25 PM<br>
            <strong>Duration:</strong> 8 hours<br>
            <strong>Aircraft:</strong> Boeing 777<br>
            <strong>Class:</strong> Economy<br>
            <strong>Price:</strong> $702 USD<br>
            <img src="https://www.gstatic.com/flights/airline_logos/70px/AA.png" alt="American Airlines"><br>
            <a href="https://www.google.com/flights">Book on Google Flights</a>
        </li>
        <!-- More entries omitted -->
    </ol>

    <h2>4-Star Hotels in New York</h2>
    <ol>
        <li>
            <strong>NobleDen Hotel</strong><br>
            <strong>Rate per Night:</strong> $537 USD<br>
            <strong>Total Rate:</strong> $3,223 USD<br>
            <img src="https://lh5.googleusercontent.com/p/AF1QipNDUrPJwBhc9ysDhc8LA822H1ZzapAVa-WDJ2d6=s287-w287-h192-n-k-no-v1" alt="NobleDen Hotel"><br>
            <a href="http://www.nobleden.com/">Visit Website</a>
        </li>
    </ol>
</body>
</html>

</example>


"""


class Agent:

    def __init__(self):
        self._tools = {t.name: t for t in TOOLS}
        self._tools_llm = ChatOpenAI(model='gpt-4o').bind_tools(TOOLS)

        builder = StateGraph(AgentState)
        builder.add_node('call_tools_llm', self.call_tools_llm)
        builder.add_node('invoke_tools', self.invoke_tools)
        builder.add_node('email_sender', self.email_sender)
        builder.set_entry_point('call_tools_llm')

        builder.add_conditional_edges('call_tools_llm', Agent.exists_action, {'more_tools': 'invoke_tools', 'email_sender': 'email_sender'})
        builder.add_edge('invoke_tools', 'call_tools_llm')
        builder.add_edge('email_sender', END)
        memory = MemorySaver()
        self.graph = builder.compile(checkpointer=memory, interrupt_before=['email_sender'])

        print(self.graph.get_graph().draw_mermaid())

    @staticmethod
    def exists_action(state: AgentState):
        result = state['messages'][-1]
        if len(result.tool_calls) == 0:
            return 'email_sender'
        return 'more_tools'

    def email_sender(self, state: AgentState):
        print('Sending email')
        email_llm = ChatOpenAI(model='gpt-4o', temperature=0.1)  # Instantiate another LLM
        email_message = [SystemMessage(content=EMAILS_SYSTEM_PROMPT), HumanMessage(content=state['messages'][-1].content)]
        email_response = email_llm.invoke(email_message)
        print('Email content:', email_response.content)

        # Mask PII in the generated HTML email body before sending
        safe_html = mask_pii(email_response.content)
        message = Mail(from_email=os.environ['FROM_EMAIL'], to_emails=os.environ['TO_EMAIL'], subject=os.environ['EMAIL_SUBJECT'],
                       html_content=safe_html)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(str(e))

    def call_tools_llm(self, state: AgentState):
        messages = state['messages']
        # Intent filtering: check human messages for jailbreak/malicious intent
        human_msgs = [m for m in messages if isinstance(m, HumanMessage)]
        for hm in human_msgs:
            if is_malicious(hm.content):
                # sanitize and return a safe reply that refuses malicious requests
                sanitized = sanitize(hm.content)
                refuse = SystemMessage(content="I cannot assist with that request."
                                       " Please rephrase your query without instructions to bypass safety.")
                return {'messages': [refuse]}

        messages = [SystemMessage(content=TOOLS_SYSTEM_PROMPT)] + messages
        message = self._tools_llm.invoke(messages)
        return {'messages': [message]}

    def invoke_tools(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f'Calling: {t}')
            if not t['name'] in self._tools:  # check for bad tool name from LLM
                print('\n ....bad tool name....')
                result = 'bad tool name, retry'  # instruct LLM to retry if bad
            else:
                result = self._tools[t['name']].invoke(t['args'])
                # Mask any detected PII in the tool result before returning it to the model
                try:
                    masked = mask_pii_in_obj(result)
                except Exception:
                    masked = result
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(masked)))
        print('Back to the model!')
        return {'messages': results}
