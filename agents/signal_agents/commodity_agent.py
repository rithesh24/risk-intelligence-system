from knowledge.knowledge_base import (
    COMMODITY_RISK_MAP,
    CATEGORY_RISK_MAP,
    COMMODITY_CATEGORY_MAP,
)


def evaluate_commodity_risk(
    dependencies: list, market_prices: dict
) -> tuple[float, float, str]:
    if not dependencies:
        return 0.1, 0.9, "No major commodity dependencies detected"

    risks = []
    reasoning_parts = []
    confidence_values = []

    for commodity in dependencies:
        commodity_lower = commodity.lower().strip()

        # Check if we have a live market price for this commodity
        price = market_prices.get(commodity)
        live_price_note = f" (live price: ${price})" if price is not None else ""

        # Exact commodity match
        if commodity_lower in COMMODITY_RISK_MAP:
            risk = COMMODITY_RISK_MAP[commodity_lower]
            confidence = 0.9 if price is not None else 0.8  
            reasoning_parts.append(
                f"{commodity} — known volatility risk={risk}{live_price_note}"
            )

        # Category based match
        elif commodity_lower in COMMODITY_CATEGORY_MAP:
            category = COMMODITY_CATEGORY_MAP[commodity_lower]
            risk = CATEGORY_RISK_MAP.get(category, 0.5)
            confidence = 0.8 if price is not None else 0.7
            reasoning_parts.append(
                f"{commodity} — categorized under {category}, risk={risk}{live_price_note}"
            )

        # Unknown commodity fallback
        else:
            risk = 0.5
            confidence = 0.5
            reasoning_parts.append(
                f"{commodity} — unknown commodity, using baseline risk=0.5{live_price_note}"
            )

        risks.append(risk)
        confidence_values.append(confidence)

    avg_risk = sum(risks) / len(risks)
    max_risk = max(risks)
    blended_risk = round(min((0.7 * avg_risk) + (0.3 * max_risk), 1.0), 4)

    avg_confidence = round(sum(confidence_values) / len(confidence_values), 4)
    reasoning = "Commodity exposure: " + " | ".join(reasoning_parts)

    return blended_risk, avg_confidence, reasoning


def run(state) -> dict:
    exposures = state.exposures
    dependencies = exposures.get("commodity_dependencies", [])

    market_prices = state.market_data.get("commodities", {})

    risk_score, confidence, reasoning = evaluate_commodity_risk(
        dependencies, market_prices
    )

    return {
        "risk_score": risk_score,
        "confidence": confidence,
        "reasoning": reasoning,
        "metadata": {
            "commodities": dependencies,
            "dependency_count": len(dependencies),
            "live_prices": market_prices,  
        },
    }