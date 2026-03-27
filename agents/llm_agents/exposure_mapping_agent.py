import json

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)

prompt = PromptTemplate(
    input_variables=["business_profile"],
    template="""
You are an economic risk intelligence system specializing in Indian businesses.
Analyze the business profile and identify all economic exposures.
Return ONLY valid JSON with no extra text, no markdown, no backticks.

Schema:
{{
  "currency_exposure": boolean,
  "commodity_dependencies": [list of raw materials or energy inputs],
  "demand_markets": [list of export or revenue markets],
  "regulatory_risk": boolean,
  "additional_exposures": [
    {{
      "type": "short_category",
      "description": "short explanation"
    }}
  ]
}}

Detection rules — extract ALL that apply:
- Import dependencies (raw materials, components, energy)
- Export market concentration (single market = higher risk)
- Currency exposure (USD, EUR, CNY transactions without hedging)
- Commodity price sensitivity (oil, metals, chemicals, agriculture)
- Supply chain concentration (single supplier, single region)
- Logistics route risk (Strait of Hormuz, Suez Canal, sea freight, and many otherimportant routes)
- Geopolitical dependencies (China, Middle East, US trade relations, eurpoe, economic crises, tarifs)
- Regulatory exposure (pharma, energy, chemicals, food = high)
- Hedging status (no hedging = higher currency and commodity risk)
- If uncertain about a field, leave it empty rather than guessing.

Business profile:
{business_profile}
""",
)


def normalize_exposures(exposures: dict) -> dict:
    """Ensures all expected fields exist with safe defaults."""
    exposures.setdefault("currency_exposure", False)
    exposures.setdefault("commodity_dependencies", [])
    exposures.setdefault("demand_markets", [])
    exposures.setdefault("regulatory_risk", False)
    exposures.setdefault("additional_exposures", [])
    return exposures


def run(state) -> dict:
    profile = state.business_profile

    if not profile:
        return {
            "risk_score": 0.0,
            "confidence": 0.0,
            "reasoning": "No business profile available for exposure mapping.",
            "metadata": {},
        }

    chain = prompt | llm
    response = chain.invoke({"business_profile": json.dumps(profile)})

    try:
        exposures = json.loads(response.content)
    except (json.JSONDecodeError, AttributeError):
        exposures = {}

    exposures = normalize_exposures(exposures)

    additional = exposures.get("additional_exposures", [])
    additional_summary = (
        ", ".join(e.get("type", "") for e in additional) if additional else "none"
    )

    return {
        "risk_score": 0.5,
        "confidence": 0.7,
        "reasoning": (
            f"Exposures identified — "
            f"currency: {exposures['currency_exposure']}, "
            f"regulatory: {exposures['regulatory_risk']}, "
            f"commodities: {exposures['commodity_dependencies']}, "
            f"additional: {additional_summary}"
        ),
        "metadata": exposures,
    }