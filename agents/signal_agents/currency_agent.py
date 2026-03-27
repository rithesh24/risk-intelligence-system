def calculate_currency_risk(exposures) -> tuple[float, str]:
    if not exposures:
        return 0.0, "No exposure data available"
    
    if not exposures.get("currency_exposure"):
        return 0.1, "Low currency exposure detected"
    
    markets = exposures.get("demand_markets", [])
    
    markets_upper = [m.upper() for m in markets]
    
    if any(m in markets_upper for m in ["US", "USA", "UNITED STATES"]):
        return 0.7, "High USD/INR exposure due to US export dependency"
    
    if any(m in markets_upper for m in ["EU", "EUR", "EUROPE"]):
        return 0.6, "Moderate-high EUR/INR exposure due to European market dependency"
    
    return 0.4, "Moderate currency exposure to foreign markets"


def run(state) -> dict:
    exposures = state.exposures

    risk_score, reasoning = calculate_currency_risk(exposures)

    return {
        "risk_score": risk_score,
        "confidence": 0.8,
        "reasoning": reasoning,
        "metadata": {
            "markets": exposures.get("demand_markets", []),
            "currency_exposure": exposures.get("currency_exposure", False),
        },
    }
