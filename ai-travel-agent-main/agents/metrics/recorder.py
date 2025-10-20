from typing import Dict, Any
import time

_METRICS = {
    'sessions': 0,
    'total_planning_time_seconds': 0.0,
    'total_savings': 0.0,
    'satisfaction_scores': []
}


def start_session():
    return time.time()


def end_session(start_time: float, time_saved_seconds: float = 0.0, savings: float = 0.0, satisfaction: int = None):
    _METRICS['sessions'] += 1
    _METRICS['total_planning_time_seconds'] += time_saved_seconds
    _METRICS['total_savings'] += savings
    if satisfaction is not None:
        _METRICS['satisfaction_scores'].append(satisfaction)


def snapshot():
    avg_satisfaction = None
    if _METRICS['satisfaction_scores']:
        avg_satisfaction = sum(_METRICS['satisfaction_scores']) / len(_METRICS['satisfaction_scores'])
    return {
        'sessions': _METRICS['sessions'],
        'total_planning_time_seconds': _METRICS['total_planning_time_seconds'],
        'total_savings': _METRICS['total_savings'],
        'avg_satisfaction': avg_satisfaction
    }
