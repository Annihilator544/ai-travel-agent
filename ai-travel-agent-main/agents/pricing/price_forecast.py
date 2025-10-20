from typing import Dict


def forecast_price_trend(current_price: float) -> Dict[str, str]:
    """Return a tiny heuristic-based forecast for demonstrative purposes.

    This is a placeholder. Replace with a real time-series model (Prophet,
    LSTM) for production usage.
    """
    if current_price < 100:
        advice = 'buy'
    elif current_price < 300:
        advice = 'hold'
    else:
        advice = 'consider_waiting'
    return {'current_price': current_price, 'advice': advice}
