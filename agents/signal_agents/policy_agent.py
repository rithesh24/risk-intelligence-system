from knowledge.knowledge_base import (INDUSTRY_POLICY_RISK, MARKET_POLICY_RISK)


def evaluate_industry_policy(industry: str) -> tuple[float, str]:
    if not industry:
        return 0.5, "The industry could not be identified, so a baseline regulatory risk was applied."

    industry_lower = industry.lower().strip()

    for key in INDUSTRY_POLICY_RISK:
        if key in industry_lower:
            risk = INDUSTRY_POLICY_RISK[key]
            level = "high" if risk >= 0.6 else "moderate" if risk >= 0.4 else "low"
            return risk, f"The {key} industry typically carries {level} regulatory sensitivity."

    return 0.5, "This industry isn't in our classification set, so a baseline regulatory risk was applied."


def evaluate_market_policy(markets: list) -> tuple[float, str]:
    if not markets:
        return 0.4, "No export markets were specified, so a baseline policy risk was applied."

    risks = [MARKET_POLICY_RISK.get(m.lower().strip(), 0.5) for m in markets]

    # Blend avg and max
    avg_risk = sum(risks) / len(risks)
    max_risk = max(risks)
    blended_risk = round(min((0.7 * avg_risk) + (0.3 * max_risk), 1.0), 4)

    reasoning = (
        f"Operating in {', '.join(markets)} exposes the business to policy and "
        "trade decisions made in those markets, such as tariffs or compliance changes."
    )
    return blended_risk, reasoning


def run(state) -> dict:
    profile = state.business_profile
    exposures = state.exposures

    industry = profile.get("industry", "")
    markets = exposures.get("demand_markets", [])

    industry_risk, industry_reason = evaluate_industry_policy(industry)
    market_risk, market_reason = evaluate_market_policy(markets)

    # Weighted blend
    final_risk = round(min((0.5 * industry_risk) + (0.5 * market_risk), 1.0), 4)
    reasoning = f"{industry_reason} {market_reason}"

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