from typing import List, Dict, Any, Optional


"""Simple cost optimizer for VoyageVerse.

This module provides a minimal, easily testable cost-ranking helper that
accepts lists of flight or hotel option dicts (expected to include a numeric
`price` field) and returns ranked results and a recommended choice. The
implementation is intentionally small — it is a starting point for more
advanced optimization (constraints, multi-objective optimization, budgets,
and trade-offs).
"""


def rank_by_price(options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return options sorted ascending by their numeric `price` field.

    Options without a valid price will be placed at the end.
    """
    def _key(o: Dict[str, Any]) -> float:
        try:
            return float(o.get('price', float('inf')))
        except Exception:
            return float('inf')

    return sorted(options, key=_key)


def recommend(options: List[Dict[str, Any]], budget: Optional[float] = None) -> Dict[str, Any]:
    """Return the best affordable option.

    If `budget` is provided, select the cheapest option within budget. If no
    options are within budget, return the overall cheapest with a `within_budget`
    flag set to False.
    """
    ranked = rank_by_price(options)
    if budget is not None:
        for o in ranked:
            try:
                if float(o.get('price', float('inf'))) <= budget:
                    o['within_budget'] = True
                    return o
            except Exception:
                continue
        # None within budget — return cheapest but flag it
        if ranked:
            ranked[0]['within_budget'] = False
            return ranked[0]
        return {}
    else:
        if ranked:
            ranked[0]['within_budget'] = True
            return ranked[0]
        return {}
