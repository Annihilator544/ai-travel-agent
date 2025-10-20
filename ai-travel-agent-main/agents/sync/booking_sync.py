from typing import Dict, Any
from agents.tools.flight_status import flight_status_tool
from agents.tools.hotels_finder import hotels_finder

"""Simple booking synchronizer.

This module demonstrates cross-service data synchronization: when a flight
is delayed beyond a threshold, we mark linked hotel bookings for recheck and
generate recommended actions.
"""


def check_and_sync(flight_info: Dict[str, Any], booking_reference: Dict[str, Any]):
    """Check flight status and return suggested hotel actions.

    flight_info expects keys: airline, flight_number, date
    booking_reference is the hotel booking metadata (id, check_in, check_out)
    """
    status = flight_status_tool(type('P', (object,), dict(**flight_info)))
    # status is a dict with 'status' and 'estimated_delay_minutes'
    delay = status.get('estimated_delay_minutes') or 0
    actions = []
    if delay and delay > 60:
        actions.append({'action': 'notify_user', 'message': 'Flight delayed >60 mins; consider adjusting hotel.'})
        actions.append({'action': 'hold_or_cancel', 'booking_id': booking_reference.get('id')})
    else:
        actions.append({'action': 'no_change'})
    return {'flight_status': status, 'suggested_actions': actions}
