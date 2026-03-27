def compute_amplification(state) -> dict:
    """
    Detects structural fragility signals and computes a risk boost.
    Each signal type can only contribute once — no double counting.
    Max total boost is capped at 0.30.
    """
    exposures = state.exposures if isinstance(state.exposures, dict) else {}
    additional = exposures.get("additional_exposures", [])

    if not additional:
        return {"boost": 0.0, "signals": []}

    # Track triggered signals as a set — no duplicates
    triggered = set()

    SIGNAL_RULES = [
        (["100%", "single supplier"],          "supplier_concentration",  0.15),
        (["no hedging", "zero hedging"],        "hedging_absence",         0.10),
        (["strait of hormuz", "suez canal"],    "logistics_chokepoint",    0.10),
        (["no alternative", "no backup"],       "no_alternative_supply",   0.10),
        (["geopolitical", "sanctions"],         "geopolitical_risk",       0.10),
        (["single market", "100% export"],      "market_concentration",    0.10),
    ]

    for item in additional:
        description = item.get("description", "").lower()

        for keywords, signal_name, _ in SIGNAL_RULES:
            if signal_name not in triggered:
                if any(kw in description for kw in keywords):
                    triggered.add(signal_name)

    # Compute boost from triggered signals only
    signal_boost_map = {rule[1]: rule[2] for rule in SIGNAL_RULES}
    boost = sum(signal_boost_map[s] for s in triggered)
    boost = round(min(boost, 0.30), 4)

    return {
        "boost": boost,
        "signals": list(triggered),
    }