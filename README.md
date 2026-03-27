# Context-Aware Multi-Agent Business Risk Intelligence System

A distributed, event-driven multi-agent platform that analyzes global economic, financial, regulatory, and geopolitical signals to generate company-specific business risk intelligence.

The system transforms unstructured business descriptions and real-world signals into structured risk assessments, impact estimates, and actionable insights using a coordinated set of specialized AI and deterministic agents.

Unlike typical AI applications, this system is designed as a decision intelligence engine, combining:

- LLM reasoning
- Deterministic risk models
- Real-time economic signals
- Multi-agent orchestration
- Explainable outputs

The result is a platform capable of On-demand analysis triggered by user input, risk monitoring for businesses.

---

## Core Idea

The system ingests real-world signals and evaluates how they impact a specific business.

Example signals include:

- Currency fluctuations
- Commodity price volatility
- Policy and regulatory changes
- Geopolitical disruptions
- Demand fluctuations
- Logistics risks

These signals are processed by specialized agents that evaluate risk from different perspectives and combine their insights into a coherent business risk assessment.

---

## Key Capabilities

### Context-Aware Business Understanding

The system interprets a business description and extracts operational exposures such as:

- Export markets
- Commodity dependencies
- Regulatory sensitivities
- Currency exposure
- Supply chain risks

### Multi-Agent Risk Analysis

Independent agents evaluate different categories of external risk:

- Currency volatility
- Commodity market exposure
- Demand shocks
- Regulatory risk
- Narrative signals from news

Each agent contributes structured risk signals.

### Business Impact Modeling

Signals are translated into real business consequences, including:

- Revenue pressure
- Cost increases
- Margin compression

### Risk Amplification Detection

Structural fragility signals such as:

- Single supplier dependency
- Lack of hedging
- Logistics chokepoints (Strait of Hormuz, Suez Canal)

are detected and used to adjust final risk scores. Each signal type contributes only once, with a maximum total boost of +0.30.

### Explainable Intelligence

The system produces interpretable outputs including:

- Risk score and confidence
- Driver explanations
- Agent contributions
- Business impact estimates
- Recommendations

---

## Example

**Input:**
```
We are a textile exporter dependent on US demand and imported dyes.
```

**Output:**
```
Risk Level  : Moderate-High
Confidence  : 0.72

Revenue impact : −5%
Cost pressure  : +3%
Margin impact  : −7%

Key Drivers:
  - USD/INR volatility
  - US demand slowdown
  - Commodity price fluctuations

Recommended Actions:
  - Hedge currency exposure
  - Adjust pricing strategy
  - Monitor demand indicators
```

---

## Multi-Agent System

The platform contains 8 specialized agents, each responsible for analyzing a different dimension of risk.

### Business Profile Agent
Extracts high-level company context from natural language input.

Example outputs:
- Industry classification
- Supply dependencies
- Export markets
- Operational exposures

### Exposure Mapping Agent
Transforms business context into structured exposure signals.

Example signals:
- Currency exposure
- Commodity dependencies
- Demand markets
- Regulatory risk
- Additional operational exposures (logistics routes, hedging status, geopolitical dependencies)

### Currency Risk Agent
Analyzes exposure to exchange-rate volatility using live FX rates (USD/INR, EUR/INR).

Signals evaluated:
- USD/INR volatility
- Cross-currency exposure by export market

### Commodity Risk Agent
Evaluates dependence on commodity markets using live prices where available, falling back to curated risk maps.

Examples:
- Crude oil
- Metals (copper, steel)
- Agricultural commodities (cotton, wheat)
- Chemicals and dyes

### Demand Risk Agent
Assesses market demand exposure based on:
- Export markets
- Industry sensitivity

Example signals:
- Global demand shifts
- Sector slowdowns
- Regional economic conditions

### Policy & Regulatory Agent
Analyzes regulatory sensitivity across industries and markets.

Examples include:
- Environmental regulation
- Healthcare compliance
- Trade policy

### Narrative Sentiment Agent
Processes filtered global news to detect:
- Geopolitical events
- Trade disruptions
- Commodity market shifts
- Macroeconomic signals

### Impact Translation Agent
Combines upstream signal scores to estimate:
- Revenue changes (%)
- Cost pressures (%)
- Margin impact (%)

This converts abstract risk signals into business-relevant financial outcomes.

---

## Risk Amplification Engine

Certain structural signals indicate system fragility and boost the base risk score beyond simple agent averages.

Examples:
- 100% supplier dependency → +0.15
- Absence of hedging → +0.10
- Single shipping route or logistics chokepoint → +0.10

Each signal type contributes only once. Total boost is capped at +0.30. Both the base score and amplified score are exposed in the output for transparency.

---

## Market Data Integration

The system integrates external economic signals including:

- Foreign exchange rates (USD/INR, EUR/INR, CNY/INR) 
- Commodity prices (oil, copper, wheat, cotton, gold, natural gas) 

Market data is fetched dynamically after exposure mapping, only for the specific commodities this company depends on, and injected into the risk pipeline before signal agents run.

---

## Global News Intelligence

The system ingests global news from sources including:

- Economic Times, Mint, Business Standard (India business)
- RBI (monetary policy)
- Reuters Markets and Business (global signals)
- OilPrice.com (energy commodities)
- WTO News (trade policy)
- Hellenic Shipping News (logistics and freight)

Articles are keyword-filtered for economic relevance and converted into structured events analyzed by the narrative agent.

---

## Observability Layer

The system includes a custom AgentMonitor layer that tracks:

- Agent execution order
- Risk score per agent
- Reasoning outputs
- Confidence values
- Execution timestamps
- Error flags for failed agents

This enables debugging, traceability, and explainability of the full risk pipeline. Logs are exposed via FastAPI endpoints and visible in the developer-facing frontend.

---

## Technology Stack

### Backend
- Python 3.10+
- FastAPI

### AI / Agent Framework
- LangChain
- LangGraph
- Groq LLM API (llama-3.3-70b-versatile)

### Data Processing
- feedparser (RSS news ingestion)
- Pydantic v2 (state validation)

### Observability
- Custom AgentMonitor layer
- FastAPI observability endpoints

### Frontend
- Next.js 14
- Tailwind CSS
- Chart.js (risk visualizations)
- IBM Plex Mono / Sans (typography)

The frontend is split into two purpose-built dashboards, each served as a separate route:

**Business Dashboard** (`/`) — designed for business users and decision makers.

- Natural language input field for describing the organisation — prompts the user to include industry, markets, currencies, supply chain, and regulatory exposure for maximum accuracy
- Animated risk gauge (SVG semicircle, 0–100) that reflects the overall composite risk score with color coding: green for low, amber for moderate, red for high
- Risk score and confidence cards with live progress bars
- AI explanation card summarising the primary risk drivers in plain English
- Agent Risk Contributions chart — horizontal bar chart comparing each agent's individual risk score and confidence side by side
- Precautions & Mitigation panel — risk-level-aware action list that adapts based on whether the result is Low, Moderate, Moderate-High, or High
- Recommended Actions list returned directly from the backend
- Agent Detail View — expandable cards per agent showing risk score, confidence, reasoning, and a visual risk bar
- Hover tooltips on every section explaining what each component measures and how to interpret it

**Agent Monitor** (`/monitor`) — designed for developers and system debugging.

- Summary stat cards — total agents run, average risk score, average confidence, highest risk agent
- Agent Execution Flow graph — an n8n-style SVG pipeline diagram showing all 8 agents as connected nodes with bezier edges and directional arrows. Executed agents glow in their risk color; unexecuted agents are dimmed. Solid edges indicate completed execution paths; dashed edges indicate paths not taken
- Risk vs Confidence Radar — spider chart comparing all agents across both dimensions simultaneously
- Agent Conflict Analysis panel — automatically detects and flags any two agents whose risk scores diverge by 25% or more, showing the delta and the agents involved
- Low confidence warning — automatically surfaces if any agent reports confidence below 50%, identifying the agent and suggesting what additional detail to include in the company description
- Agent Output Panels — one expandable card per agent showing risk score, confidence, reasoning text, progress bar, and expandable metadata      (markets, commodities, revenue impact percentages, etc.)

---

## Key Engineering Concepts Demonstrated

- Multi-agent system design
- Distributed decision pipelines
- Hybrid AI architecture (LLM + deterministic models)
- Event-driven data ingestion
- Stateful graph orchestration with LangGraph
- Explainable AI systems
- Economic signal processing
- Observability for AI pipelines
- Immutable state management with Pydantic v2

---

## Positioning

This system can be positioned as a:

**Multi-Agent Decision Intelligence Platform for Business Risk Monitoring**

It moves beyond simple AI models by combining structured economic reasoning, real-world signals, and explainable risk analysis into a continuously running intelligence system.

---

## Deployment

The system is deployed across two platforms:

- **Backend (FastAPI)** 
- **Frontend (Next.js)** 

### Backend (Render)

- **Runtime:** Python 3.10+
- **Start Command:** `uvicorn api.main:app --host 0.0.0.0 --port 8000`

Set the following environment variables in Render:
```
GROQ_API_KEY=your_groq_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

### Frontend (Vercel)

- **Root Directory:** `frontend`
- **Framework:** Next.js 

## Future Improvements

Possible future enhancements include:

- Real-time event streaming
- Supply chain risk agents
- Geopolitical risk modeling
- Reinforcement learning for dynamic agent trust weighting
- LangSmith integration for full LLM observability
- Historical risk trend tracking

---