from knowledge.knowledge_base import (INDUSTRY_POLICY_RISK, MARKET_POLICY_RISK)


def evaluate_industry_policy(industry: str) -> tuple[float, str]:
    if not industry:
        return 0.5, "Unknown industry — baseline policy risk applied"

    industry_lower = industry.lower().strip()

    for key in INDUSTRY_POLICY_RISK:
        if key in industry_lower:
            risk = INDUSTRY_POLICY_RISK[key]
            return risk, f"Industry: {key} — regulatory sensitivity risk={risk}"

    return 0.5, "Industry not classified — baseline policy risk applied"


def evaluate_market_policy(markets: list) -> tuple[float, str]:
    if not markets:
        return 0.4, "No export markets specified"

    risks = []
    reasoning = []

    for market in markets:
        market_lower = market.lower().strip()  
        risk = MARKET_POLICY_RISK.get(market_lower, 0.5)
        risks.append(risk)
        reasoning.append(f"{market} policy risk={risk}")

    # Blend avg and max 
    avg_risk = sum(risks) / len(risks)
    max_risk = max(risks)
    blended_risk = round(min((0.7 * avg_risk) + (0.3 * max_risk), 1.0), 4)

    return blended_risk, "Market policy exposure: " + " | ".join(reasoning)


def run(state) -> dict:
    profile = state.business_profile
    exposures = state.exposures

    industry = profile.get("industry", "")
    markets = exposures.get("demand_markets", [])

    industry_risk, industry_reason = evaluate_industry_policy(industry)
    market_risk, market_reason = evaluate_market_policy(markets)

    # Weighted blend 
    final_risk = round(min((0.5 * industry_risk) + (0.5 * market_risk), 1.0), 4)
    reasoning = f"{industry_reason}. {market_reason}"

    return {
        "risk_score": final_risk,
        "confidence": 0.7,
        "reasoning": reasoning,
        "metadata": {
            "industry": industry,
            "markets": markets,
            "industry_policy_risk": industry_risk,
            "market_policy_risk": market_risk,
        },
    }