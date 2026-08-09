from knowledge.knowledge_base import (MARKET_RISK_MAP,INDUSTRY_RISK_MAP)


def evaluate_market_risk(markets: list) -> tuple[float, float, str]:
    if not markets:
        return 0.4, 0.6, "No export markets were specified, so a baseline demand risk was applied."

    risks = [MARKET_RISK_MAP.get(m.lower().strip(), 0.5) for m in markets]

    # Blend avg and max
    avg_risk = sum(risks) / len(risks)
    max_risk = max(risks)
    blended_risk = round(min((0.7 * avg_risk) + (0.3 * max_risk), 1.0), 4)

    reasoning = (
        f"Revenue is tied to demand conditions in {', '.join(markets)}. "
        "A slowdown or shift in these markets would directly affect sales volumes."
    )
    return blended_risk, 0.7, reasoning


def evaluate_industry_risk(industry: str) -> tuple[float, str]:
    if not industry:
        return 0.5, "The industry could not be identified, so a baseline demand-sensitivity risk was applied."

    industry_lower = industry.lower().strip()

    for key in INDUSTRY_RISK_MAP:
        if key in industry_lower:
            risk = INDUSTRY_RISK_MAP[key]
            level = "high" if risk >= 0.6 else "moderate" if risk >= 0.4 else "low"
            return risk, f"The {key} industry tends to have {level} sensitivity to demand cycles."

    return 0.5, "This industry isn't in our classification set, so a baseline demand-sensitivity risk was applied."


def run(state) -> dict:
    exposures = state.exposures
    profile = state.business_profile

    markets = exposures.get("demand_markets", [])
    industry = profile.get("industry", "")

    market_risk, confidence, market_reason = evaluate_market_risk(markets)
    industry_risk, industry_reason = evaluate_industry_risk(industry)

    # Weighted blend
    final_risk = round(min((0.6 * market_risk) + (0.4 * industry_risk), 1.0), 4)
    reasoning = f"{market_reason} {industry_reason}"

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