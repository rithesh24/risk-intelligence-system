from knowledge.knowledge_base import (MARKET_RISK_MAP,INDUSTRY_RISK_MAP)


def evaluate_market_risk(markets: list) -> tuple[float, float, str]:
    if not markets:
        return 0.4, 0.6, "No export markets specified"

    risks = []
    reasoning = []

    for market in markets:
        market_lower = market.lower().strip()
        risk = MARKET_RISK_MAP.get(market_lower, 0.5)
        risks.append(risk)
        reasoning.append(f"{market} risk={risk}")

    # Blend avg and max
    avg_risk = sum(risks) / len(risks)
    max_risk = max(risks)
    blended_risk = round(min((0.7 * avg_risk) + (0.3 * max_risk), 1.0), 4)

    return blended_risk, 0.7, "Market demand exposure: " + " | ".join(reasoning)


def evaluate_industry_risk(industry: str) -> tuple[float, str]:
    if not industry:
        return 0.5, "Unknown industry — baseline risk applied"

    industry_lower = industry.lower().strip()

    for key in INDUSTRY_RISK_MAP:
        if key in industry_lower:
            risk = INDUSTRY_RISK_MAP[key]
            return risk, f"Industry: {key} — demand sensitivity risk={risk}"

    return 0.5, "Industry not classified — baseline risk applied"


def run(state) -> dict:
    exposures = state.exposures
    profile = state.business_profile

    markets = exposures.get("demand_markets", [])
    industry = profile.get("industry", "")

    market_risk, confidence, market_reason = evaluate_market_risk(markets)
    industry_risk, industry_reason = evaluate_industry_risk(industry)

    # Weighted blend 
    final_risk = round(min((0.6 * market_risk) + (0.4 * industry_risk), 1.0), 4)
    reasoning = f"{market_reason}. {industry_reason}"

    return {
        "risk_score": final_risk,
        "confidence": confidence,
        "reasoning": reasoning,
        "metadata": {
            "markets": markets,
            "industry": industry,
            "market_risk": market_risk,
            "industry_risk": industry_risk,
        },
    }