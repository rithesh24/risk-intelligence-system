import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    model_kwargs={"response_format": {"type": "json_object"}},
    timeout=15,
    max_retries=1,
)

prompt = PromptTemplate(
    input_variables=["company_description"],
    template="""
You are an economic intelligence system.
Extract a structured business profile from the description.
Return ONLY valid JSON with no extra text, no markdown, no backticks.

Fields required:
- industry
- export_markets
- key_dependencies
- exposure_types

Company description:
{company_description}
""",
)


def run(state):
    description = state.company_input

    chain = prompt | llm
    response = chain.invoke({"company_description": description})

    try:
        profile = json.loads(response.content)
    except (json.JSONDecodeError, AttributeError):
        profile = {
            "industry": "unknown",
            "export_markets": [],
            "key_dependencies": [],
            "exposure_types": [],
        }

    
    return {
        "risk_score": 0.5,
        "confidence": 0.7,
        "reasoning": summarize_profile(profile),
        "metadata": profile,
    }


def summarize_profile(profile: dict) -> str:
    industry = profile.get("industry") or "an unclassified"
    markets = profile.get("export_markets") or []
    dependencies = profile.get("key_dependencies") or []

    parts = [f"This business operates in the {industry} industry."]

    if markets:
        parts.append(
            f"It sells into {', '.join(markets)}, so revenue is tied to demand "
            "and economic conditions in those markets."
        )

    if dependencies:
        parts.append(
            f"It relies on {', '.join(dependencies)}, which creates supply and "
            "cost exposures worth tracking."
        )

    return " ".join(parts)