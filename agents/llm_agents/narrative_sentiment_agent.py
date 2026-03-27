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
    input_variables=["context", "news"],
    template="""
You are an economic risk analysis system specializing in Indian businesses.
Using the company context and news events, determine whether the news creates business risk.
Return ONLY valid JSON with no extra text, no markdown, no backticks.

{{
  "sentiment": "positive | neutral | negative",
  "risk_score": float between 0 and 1,
  "signal_type": "currency | commodity | demand | policy | geopolitics | logistics",
  "reasoning": "short explanation of why this news creates or reduces risk"
}}

Scoring rules:
- 0.0–0.3: news is positive or irrelevant to the business
- 0.3–0.6: mild indirect risk, monitor closely
- 0.6–0.8: direct risk to revenue, cost, or operations
- 0.8–1.0: severe risk — supply disruption, sanctions, demand collapse, price spike

Company context:
{context}

Relevant news:
{news}
""",
)


def extract_context(state) -> list[str]:
    """Builds keyword context from business profile and exposures."""
    exposures = state.exposures
    profile = state.business_profile
    keywords = []

    if profile.get("industry"):
        keywords.append(profile["industry"])

    keywords.extend(exposures.get("commodity_dependencies", []))
    keywords.extend(exposures.get("demand_markets", []))

    for item in exposures.get("additional_exposures", []):
        if isinstance(item, dict):
            keywords.append(item.get("description", ""))

    return [k for k in keywords if k]  


def filter_relevant_news(events, keywords) -> list:
    """Returns only news events that mention at least one keyword."""
    if not keywords:
        return events  

    relevant = []
    for event in events:
        text = (event.title + " " + event.summary).lower()
        if any(word.lower() in text for word in keywords):
            relevant.append(event)

    return relevant


def run(state) -> dict:
    events = getattr(state, "news_events", [])

    if not events:
        return {
            "risk_score": 0.5,
            "confidence": 0.3,
            "reasoning": "No news events available for narrative analysis",
            "metadata": {"sentiment": "neutral", "signal_type": "unknown"},
        }

    keywords = extract_context(state)
    relevant_events = filter_relevant_news(events, keywords)

    if not relevant_events:
        return {
            "risk_score": 0.5,
            "confidence": 0.4,
            "reasoning": "No relevant news signals detected for this business profile",
            "metadata": {"sentiment": "neutral", "signal_type": "unknown"},
        }

    news_text = "\n".join(
        f"- {event.title}: {event.summary}"
        for event in relevant_events[:5]
    )

    chain = prompt | llm
    response = chain.invoke({
        "context": json.dumps(keywords),  
        "news": news_text,
    })

    try:
        result = json.loads(response.content)
        risk_score = float(result.get("risk_score", 0.5))
        risk_score = max(0.0, min(1.0, risk_score))  
    except (json.JSONDecodeError, AttributeError, ValueError):
        result = {
            "sentiment": "neutral",
            "risk_score": 0.5,
            "reasoning": "Unable to parse narrative signal",
            "signal_type": "unknown",
        }
        risk_score = 0.5

    return {
        "risk_score": risk_score,
        "confidence": 0.7,
        "reasoning": (
            f"Narrative signal ({result.get('signal_type', 'unknown')}): "
            f"{result.get('sentiment', 'neutral')} — {result.get('reasoning', '')}"
        ),
        "metadata": {
            "sentiment": result.get("sentiment", "neutral"),
            "signal_type": result.get("signal_type", "unknown"),
            "news_count": len(relevant_events[:5]),
            "keywords_matched": len(keywords),
        },
    }