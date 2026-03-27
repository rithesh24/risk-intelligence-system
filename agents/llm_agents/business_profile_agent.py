import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
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
        "reasoning": f"Business profile extracted for industry: {profile.get('industry', 'unknown')}",
        "metadata": profile,
    }