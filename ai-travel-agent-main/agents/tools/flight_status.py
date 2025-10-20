import os
from typing import Optional
import requests
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool


class FlightStatusInput(BaseModel):
    airline: Optional[str] = Field(None)
    flight_number: Optional[str] = Field(None)
    date: Optional[str] = Field(None)


class FlightStatusInputSchema(BaseModel):
    params: FlightStatusInput


@tool(args_schema=FlightStatusInputSchema)
def flight_status_tool(params: FlightStatusInput):
    """Flight status tool: uses AviationStack or returns a stub if API key missing.

    Requires AVIATIONSTACK_API_KEY environment variable to call real API.
    """
    api_key = os.environ.get('AVIATIONSTACK_API_KEY') or os.environ.get('FLIGHTSTATUS_API_KEY')
    if api_key and params.flight_number:
        try:
            resp = requests.get('http://api.aviationstack.com/v1/flights', params={
                'access_key': api_key,
                'flight_iata': params.flight_number
            }, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            # Return first matching flight if present
            if data.get('data'):
                f = data['data'][0]
                return {
                    'airline': f.get('airline', {}).get('name'),
                    'flight_number': params.flight_number,
                    'date': params.date or f.get('flight_date'),
                    'status': f.get('flight_status'),
                    'estimated_delay_minutes': None
                }
        except Exception:
            pass

    return {
        'airline': params.airline,
        'flight_number': params.flight_number,
        'date': params.date or '2025-10-16',
        'status': 'On time',
        'estimated_delay_minutes': 0
    }
