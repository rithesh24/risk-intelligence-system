import os
import requests
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Symbol Maps 
FX_SYMBOLS = {
    "USD": "USD",
    "EUR": "EUR",
    "CNY": "CNY",
    "GBP": "GBP",
}

# Alpha Vantage physical commodity symbols
COMMODITY_SYMBOL_MAP = {
    "oil":         "WTI",
    "crude oil":   "WTI",
    "brent":       "BRENT",
    "natural gas": "NATURAL_GAS",
    "copper":      "COPPER",
    "wheat":       "WHEAT",
    "corn":        "CORN",
    "cotton":      "COTTON",
    "sugar":       "SUGAR",
    "coffee":      "COFFEE",
    "gold":        "GOLD",
    "silver":      "SILVER",
    "aluminium":   "ALUMINUM",
    "aluminum":    "ALUMINUM",
    # No direct symbol — agent uses risk map fallback
    "dyes":        None,
    "chemicals":   None,
    "steel":       None,
    "soy":         None,
}


#  Currency (live via open.er-api) 
def get_fx_rate(base: str = "USD") -> float | None:
    """Fetches live INR rate for given base currency."""
    try:
        response = requests.get(
            f"https://open.er-api.com/v6/latest/{base}",
            timeout=5,
        )
        data = response.json()
        return round(data["rates"]["INR"], 4)
    except Exception:
        return None


#  Commodities (live via Alpha Vantage) 
def get_commodity_price(commodity_name: str) -> float | None:
    """
    Fetches latest monthly price for a commodity from Alpha Vantage.
    Returns None if commodity has no symbol or API call fails.
    """
    if not ALPHA_VANTAGE_KEY:
        return None

    commodity_lower = commodity_name.lower().strip()
    symbol = COMMODITY_SYMBOL_MAP.get(commodity_lower)

    if not symbol:
        return None  # agent will use its own risk map fallback

    try:
        response = requests.get(
            "https://www.alphavantage.co/query",
            params={
                "function": symbol,
                "interval": "monthly",
                "apikey": ALPHA_VANTAGE_KEY,
            },
            timeout=5,
        )
        data = response.json()

        # Alpha Vantage returns {"data": [{"date": ..., "value": ...}, ...]}
        entries = data.get("data", [])
        if not entries:
            return None

        latest_value = entries[0].get("value")
        if latest_value and latest_value != ".":
            return round(float(latest_value), 2)

        return None

    except Exception:
        return None


# Aggregator 
def get_market_data(commodity_dependencies: list[str] | None = None) -> dict:
    """
    Fetches live FX rates + commodity prices for this
    company's specific dependencies.
    """
    data = {
        # Live FX rates
        "usd_inr": get_fx_rate("USD"),
        "eur_inr": get_fx_rate("EUR"),
        "cny_inr": get_fx_rate("CNY"),

        # Commodity prices 
        "commodities": {},
    }

    if commodity_dependencies:
        for commodity in commodity_dependencies:
            price = get_commodity_price(commodity)
            if price is not None:
                data["commodities"][commodity] = price
            # if None, just skip 

    return data