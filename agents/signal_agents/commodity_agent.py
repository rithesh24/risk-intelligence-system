import re

from knowledge.knowledge_base import (
    COMMODITY_RISK_MAP,
    CATEGORY_RISK_MAP,
    COMMODITY_CATEGORY_MAP,
)


def _best_match(text: str, keys) -> str | None:
    """
    Finds known commodity terms inside a longer phrase (e.g. "APIs from China"
    contains the known term "apis"), rather than requiring an exact match.
    Word-boundary-matched so short keys like "tin" don't match inside unrelated
    words like "destination". Trailing "s?" tolerates singular/plural mismatches
    (key "chemicals" also matches "chemical inputs"). Picks the longest match
    when several apply.
    """
    matches = [
        k for k in keys
        if re.search(rf"\b{re.escape(k[:-1] if k.endswith('s') else k)}s?\b", text)
    ]
    return max(matches, key=len) if matches else None


def evaluate_commodity_risk(
    dependencies: list, market_prices: dict
) -> tuple[float, float, str]:
    if not dependencies:
        return 0.1, 0.9, (
            "This business has no major commodity dependencies, so raw material "
            "price swings are unlikely to be a significant risk driver."
        )

    risks = []
    item_sentences = []
    confidence_values = []

    for commodity in dependencies:
        commodity_lower = commodity.lower().strip()

        # Check if we have a live market price for this commodity
        price = market_prices.get(commodity)
        price_note = f", currently trading around ${price}" if price is not None else ""

        risk_match = _best_match(commodity_lower, COMMODITY_RISK_MAP.keys())
        category_match = _best_match(commodity_lower, COMMODITY_CATEGORY_MAP.keys())

        if risk_match:
            risk = COMMODITY_RISK_MAP[risk_match]
            confidence = 0.9 if price is not None else 0.8
            item_sentences.append(f"{commodity} is a known volatile input{price_note}")

        elif category_match:
            category = COMMODITY_CATEGORY_MAP[category_match]
            risk = CATEGORY_RISK_MAP.get(category, 0.5)
            confidence = 0.8 if price is not None else 0.7
            item_sentences.append(
                f"{commodity} falls under the {category} category, which carries its own price risk{price_note}"
            )

        else:
            risk = 0.5
            confidence = 0.5
            item_sentences.append(
                f"{commodity} isn't in our risk database, so a baseline risk was assumed{price_note}"
            )

        risks.append(risk)
        confidence_values.append(confidence)

    avg_risk = sum(risks) / len(risks)
    max_risk = max(risks)
    blended_risk = round(min((0.7 * avg_risk) + (0.3 * max_risk), 1.0), 4)
    avg_confidence = round(sum(confidence_values) / len(confidence_values), 4)

    reasoning = (
        f"This business depends on {len(dependencies)} key commodity input"
        f"{'s' if len(dependencies) > 1 else ''}: " + "; ".join(item_sentences) + ". "
        f"Combined, these inputs carry a blended volatility risk of {blended_risk:.2f}, "
        "so cost pressure from this side should be actively monitored."
    )

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