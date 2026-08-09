def calculate_currency_risk(exposures) -> tuple[float, str]:
    if not exposures:
        return 0.0, "No exposure data was available to assess currency risk."

    if not exposures.get("currency_exposure"):
        return 0.1, (
            "This business shows minimal foreign currency exposure, so FX "
            "volatility is unlikely to significantly affect its financials."
        )

    markets = exposures.get("demand_markets", [])
    markets_upper = [m.upper() for m in markets]

    if any(m in markets_upper for m in ["US", "USA", "UNITED STATES"]):
        return 0.7, (
            "Because a large share of revenue comes from the US, this business is "
            "highly exposed to USD/INR movements. Without hedging, a sudden swing "
            "in the exchange rate could meaningfully affect margins."
        )

    if any(m in markets_upper for m in ["EU", "EUR", "EUROPE"]):
        return 0.6, (
            "With meaningful revenue tied to European markets, this business "
            "carries moderate-to-high EUR/INR exposure — currency movements here "
            "can noticeably affect revenue once converted back to rupees."
        )

    return 0.4, (
        "This business has some exposure to foreign markets, giving it moderate "
        "currency risk that's worth monitoring as trade volumes grow."
    )


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
