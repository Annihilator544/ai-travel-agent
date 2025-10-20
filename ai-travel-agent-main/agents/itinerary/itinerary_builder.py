from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from agents.tools.flights_finder import FlightsInput, flights_finder
from agents.tools.hotels_finder import HotelsInput, hotels_finder
from agents.tools.weather import WeatherInput, weather_tool
from agents.optimizer.cost_optimizer import recommend, rank_by_price
from agents.recommender.collaborative import load_sample_data
from agents.pricing.price_forecast import forecast_price_trend


class ItineraryInput(BaseModel):
    departure_airport: str = Field(description='IATA code')
    arrival_location: str = Field(description='City or destination')
    outbound_date: str = Field(description='YYYY-MM-DD')
    return_date: Optional[str] = Field(None, description='YYYY-MM-DD')
    adults: Optional[int] = Field(1)
    budget: Optional[float] = Field(None)


class ItineraryInputSchema(BaseModel):
    params: ItineraryInput


@tool(args_schema=ItineraryInputSchema)
def itinerary_builder(params: ItineraryInput):
    """Build a simple itinerary by calling flights, hotels, and weather stubs.

    This is a pragmatic first-pass that demonstrates multi-step planning and
    cost-based selection. Replace with richer LLM orchestration as needed.
    """
    # Flights search
    flights_query = FlightsInput(
        departure_airport=params.departure_airport,
        arrival_airport=None,
        outbound_date=params.outbound_date,
        return_date=params.return_date,
        adults=params.adults,
    )
    flights = flights_finder(flights_query)

    # Hotels search (use arrival_location as query)
    hotels_query = HotelsInput(
        q=params.arrival_location,
        check_in_date=params.outbound_date,
        check_out_date=params.return_date or params.outbound_date,
        adults=params.adults,
    )
    hotels = hotels_finder(hotels_query)

    # Weather check for outbound date
    weather_q = WeatherInput(location=params.arrival_location, date=params.outbound_date)
    weather = weather_tool(weather_q)

    # Cost-based selection for demo
    # Normalize flight and hotel options into lists with numeric price field if possible
    flight_options = []
    try:
        # flights may be list-like
        for f in flights[:5]:
            price = f.get('price') or f.get('total_price') or f.get('amount') or None
            flight_options.append({'source': f, 'price': float(price) if price else None})
    except Exception:
        flight_options = []

    hotel_options = []
    try:
        for h in hotels:
            price = h.get('price') or h.get('rate') or None
            hotel_options.append({'source': h, 'price': float(price) if price else None})
    except Exception:
        hotel_options = []

    chosen_flight = recommend(flight_options, budget=params.budget) if flight_options else {}
    chosen_hotel = recommend(hotel_options, budget=params.budget) if hotel_options else {}

    # Forecast price trend for flights (basic stub)
    flight_price_trend = None
    try:
        if chosen_flight and chosen_flight.get('price'):
            flight_price_trend = forecast_price_trend(chosen_flight['price'])
    except Exception:
        flight_price_trend = None

    # Sample recommender usage
    sample_data = load_sample_data()

    itinerary = {
        'flights_found': len(flight_options),
        'hotels_found': len(hotel_options),
        'chosen_flight': chosen_flight,
        'chosen_hotel': chosen_hotel,
        'weather': weather,
        'flight_price_trend': flight_price_trend,
        'sample_recommender_data_present': bool(sample_data)
    }

    return itinerary
