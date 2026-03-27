"""
Central Knowledge Base for Risk Intelligence System.

Contains industry, market, and commodity risk knowledge
used by signal agents.
"""

# Industry Risk Knowledge


INDUSTRY_RISK_MAP = {
    # Healthcare & Life Sciences
    "pharmaceutical": 0.75,
    "biotech": 0.75,
    "medical devices": 0.65,
    "healthcare": 0.55,
    "diagnostics": 0.6,
    "clinical research": 0.65,
 
    # Energy & Resources
    "petrochemical": 0.8,
    "energy": 0.8,
    "oil": 0.85,
    "oil and gas": 0.85,
    "natural gas": 0.8,
    "coal": 0.85,
    "renewable energy": 0.5,
    "solar": 0.5,
    "wind energy": 0.5,
    "nuclear": 0.75,
    "mining": 0.75,
 
    # Chemicals & Materials
    "chemicals": 0.7,
    "specialty chemicals": 0.7,
    "agrochemicals": 0.72,
    "fertilizers": 0.68,
    "plastics": 0.65,
    "rubber": 0.6,
 
    # Manufacturing & Industrial
    "automobile": 0.7,
    "automotive components": 0.68,
    "electronics": 0.6,
    "semiconductors": 0.7,
    "industrial machinery": 0.65,
    "heavy machinery": 0.7,
    "aerospace": 0.75,
    "defense": 0.65,
    "shipbuilding": 0.72,
    "construction": 0.75,
    "steel": 0.72,
    "aluminium": 0.68,
    "cement": 0.65,
 
    # Consumer & Retail
    "textile": 0.65,
    "apparel": 0.6,
    "footwear": 0.58,
    "food": 0.35,
    "food processing": 0.4,
    "beverages": 0.38,
    "consumer goods": 0.45,
    "retail": 0.45,
    "e-commerce": 0.4,
    "luxury goods": 0.55,
 
    # Technology & Services
    "technology": 0.5,
    "software": 0.4,
    "it services": 0.45,
    "fintech": 0.6,
    "telecommunications": 0.55,
    "media": 0.5,
    "edtech": 0.4,
 
    # Finance & Professional Services
    "banking": 0.65,
    "insurance": 0.55,
    "financial services": 0.6,
    "real estate": 0.65,
    "logistics": 0.6,
    "shipping": 0.65,
    "aviation": 0.72,
 
    # Agriculture
    "agriculture": 0.6,
    "aquaculture": 0.58,
    "forestry": 0.55,
}


COMMODITY_CATEGORY_MAP = {
    # Energy
    "crude oil": "energy",
    "oil": "energy",
    "petroleum": "energy",
    "natural gas": "energy",
    "lng": "energy",
    "coal": "energy",
    "diesel": "energy",
    "jet fuel": "energy",
    "gasoline": "energy",
    "kerosene": "energy",

    # Agriculture
    "cotton": "agriculture",
    "wheat": "agriculture",
    "soy": "agriculture",
    "soybeans": "agriculture",
    "corn": "agriculture",
    "maize": "agriculture",
    "rice": "agriculture",
    "sugar": "agriculture",
    "coffee": "agriculture",
    "cocoa": "agriculture",
    "palm oil": "agriculture",
    "rubber": "agriculture",
    "timber": "agriculture",
    "tea": "agriculture",
    "tobacco": "agriculture",
    "jute": "agriculture",
    "spices": "agriculture",

    # Metals
    "copper": "metals",
    "steel": "metals",
    "iron ore": "metals",
    "aluminium": "metals",
    "aluminum": "metals",
    "zinc": "metals",
    "lead": "metals",
    "nickel": "metals",
    "tin": "metals",
    "tungsten": "metals",
    "cobalt": "metals",
    "lithium": "metals",
    "manganese": "metals",
    "titanium": "metals",
    "chromium": "metals",
    "molybdenum": "metals",

    # Precious Metals
    "gold": "precious metals",
    "silver": "precious metals",
    "platinum": "precious metals",
    "palladium": "precious metals",
    "rhodium": "precious metals",

    # Rare Earths
    "rare earth metals": "rare earths",
    "rare earths": "rare earths",
    "neodymium": "rare earths",
    "dysprosium": "rare earths",
    "cerium": "rare earths",
    "lanthanum": "rare earths",
    "yttrium": "rare earths",

    # Chemicals
    "chemicals": "chemicals",
    "specialty chemicals": "chemicals",
    "dyes": "chemicals",
    "fertilizers": "chemicals",
    "urea": "chemicals",
    "ammonia": "chemicals",
    "ethylene": "chemicals",
    "methanol": "chemicals",
    "polymers": "chemicals",
    "plastics": "chemicals",
    "solvents": "chemicals",
    "resins": "chemicals",
    "acids": "chemicals",
    "agrochemicals": "chemicals",
    "pesticides": "chemicals",

    # Pharmaceuticals
    "active pharmaceutical ingredients": "pharmaceuticals",
    "apis": "pharmaceuticals",
    "excipients": "pharmaceuticals",
    "biologics": "pharmaceuticals",
    "vaccines": "pharmaceuticals",
    "generics": "pharmaceuticals",

    # Technology
    "semiconductors": "technology",
    "chips": "technology",
    "silicon": "technology",
    "polysilicon": "technology",
    "printed circuit boards": "technology",
    "pcbs": "technology",
    "displays": "technology",
    "batteries": "technology",
    "lithium ion batteries": "technology",

    # Industrials
    "steel pipes": "industrials",
    "machinery parts": "industrials",
    "bearings": "industrials",
    "industrial gases": "industrials",
    "hydraulic fluids": "industrials",
    "lubricants": "industrials",
    "packaging": "industrials",
    "glass": "industrials",
    "ceramics": "industrials",
    "cement": "industrials",
}



# policy/regulatory sensitivity
INDUSTRY_POLICY_RISK = {
    # Healthcare & Life Sciences
    "pharmaceutical": 0.85,
    "biotech": 0.82,
    "medical devices": 0.78,
    "healthcare": 0.7,
    "diagnostics": 0.72,
    "clinical research": 0.75,
 
    # Energy & Resources
    "petrochemical": 0.78,
    "energy": 0.82,
    "oil": 0.82,
    "oil and gas": 0.82,
    "natural gas": 0.8,
    "coal": 0.88,           # high due to ESG/carbon regulation
    "renewable energy": 0.55,
    "solar": 0.5,
    "wind energy": 0.5,
    "nuclear": 0.9,         # highest regulatory burden
    "mining": 0.78,
 
    # Chemicals & Materials
    "chemicals": 0.72,
    "specialty chemicals": 0.7,
    "agrochemicals": 0.75,
    "fertilizers": 0.68,
    "plastics": 0.7,        # ESG/plastic regulation rising
    "rubber": 0.55,
 
    # Manufacturing & Industrial
    "automobile": 0.68,
    "automotive components": 0.65,
    "electronics": 0.62,
    "semiconductors": 0.75, # export controls, CHIPS act
    "industrial machinery": 0.6,
    "heavy machinery": 0.65,
    "aerospace": 0.82,
    "defense": 0.88,
    "shipbuilding": 0.68,
    "construction": 0.72,
    "steel": 0.7,
    "aluminium": 0.65,
    "cement": 0.68,
 
    # Consumer & Retail
    "textile": 0.6,
    "apparel": 0.55,
    "footwear": 0.52,
    "food": 0.58,
    "food processing": 0.6,
    "beverages": 0.55,
    "consumer goods": 0.48,
    "retail": 0.45,
    "e-commerce": 0.5,
    "luxury goods": 0.5,
 
    # Technology & Services
    "technology": 0.55,
    "software": 0.45,
    "it services": 0.48,
    "fintech": 0.75,        # heavy financial regulation
    "telecommunications": 0.65,
    "media": 0.55,
    "edtech": 0.45,
 
    # Finance & Professional Services
    "banking": 0.8,
    "insurance": 0.72,
    "financial services": 0.75,
    "real estate": 0.62,
    "logistics": 0.55,
    "shipping": 0.65,
    "aviation": 0.78,
 
    # Agriculture
    "agriculture": 0.6,
    "aquaculture": 0.58,
    "forestry": 0.6,
}





# Market Risk Knowledge

MARKET_RISK_MAP = {
    # Major Economies
    "US": 0.65,
    "USA": 0.65,
    "United States": 0.65,
    "EU": 0.6,
    "Europe": 0.6,
    "Eurozone": 0.6,
    "UK": 0.62,
    "Germany": 0.55,
    "France": 0.55,
    "Italy": 0.62,
    "Spain": 0.6,
 
    # Asia Pacific
    "China": 0.72,
    "Japan": 0.5,
    "South Korea": 0.55,
    "Taiwan": 0.65,         
    "India": 0.48,
    "Southeast Asia": 0.55,
    "Vietnam": 0.52,
    "Indonesia": 0.55,
    "Thailand": 0.52,
    "Malaysia": 0.5,
    "Philippines": 0.55,
    "Australia": 0.42,
 
    # Middle East & Africa
    "Middle East": 0.58,
    "Saudi Arabia": 0.6,
    "UAE": 0.52,
    "Iran": 0.85,          
    "Africa": 0.65,
    "South Africa": 0.6,
    "Nigeria": 0.68,
 
    # Americas
    "Brazil": 0.65,
    "Mexico": 0.6,
    "Latin America": 0.65,
    "Canada": 0.42,
 
    # Eastern Europe / Central Asia
    "Russia": 0.88,         
    "Ukraine": 0.9,
    "Eastern Europe": 0.6,
    "Turkey": 0.7,
}




MARKET_POLICY_RISK = {
    "US": 0.65,
    "USA": 0.65,
    "United States": 0.65,
    "EU": 0.68,
    "Europe": 0.68,
    "Eurozone": 0.65,
    "UK": 0.65,             # post-Brexit complexity
    "Germany": 0.58,
    "France": 0.6,
    "Italy": 0.62,
    "Spain": 0.6,
 
    "China": 0.75,
    "Japan": 0.52,
    "South Korea": 0.55,
    "Taiwan": 0.72,
    "India": 0.55,
    "Southeast Asia": 0.52,
    "Vietnam": 0.5,
    "Indonesia": 0.55,
    "Thailand": 0.5,
    "Malaysia": 0.48,
    "Philippines": 0.55,
    "Australia": 0.45,
 
    "Middle East": 0.62,
    "Saudi Arabia": 0.65,
    "UAE": 0.55,
    "Iran": 0.92,
    "Africa": 0.65,
    "South Africa": 0.62,
    "Nigeria": 0.7,
 
    "Brazil": 0.68,
    "Mexico": 0.62,
    "Latin America": 0.65,
    "Canada": 0.45,
 
    "Russia": 0.92,
    "Ukraine": 0.92,
    "Eastern Europe": 0.62,
    "Turkey": 0.72,
}





# Commodity Risk Knowledge

COMMODITY_RISK_MAP = {
     # Energy
    "crude oil": 0.88,
    "oil": 0.88,
    "natural gas": 0.82,
    "lng": 0.8,
    "coal": 0.75,
    "petroleum": 0.85,
    "diesel": 0.78,
    "jet fuel": 0.78,
 
    # Metals & Mining
    "steel": 0.65,
    "iron ore": 0.65,
    "copper": 0.68,
    "aluminium": 0.65,
    "aluminum": 0.65,
    "nickel": 0.72,
    "lithium": 0.78,        # EV demand surge
    "cobalt": 0.78,
    "rare earth metals": 0.82,
    "rare earths": 0.82,
    "gold": 0.55,
    "silver": 0.6,
    "platinum": 0.65,
    "palladium": 0.72,
    "zinc": 0.62,
    "lead": 0.6,
    "tin": 0.65,
    "tungsten": 0.72,
 
    # Agricultural
    "wheat": 0.72,
    "corn": 0.7,
    "soybeans": 0.68,
    "rice": 0.62,
    "sugar": 0.65,
    "coffee": 0.68,
    "cocoa": 0.65,
    "cotton": 0.72,
    "palm oil": 0.68,
    "rubber": 0.62,
    "timber": 0.58,
 
    # Chemicals & Industrial
    "chemicals": 0.72,
    "specialty chemicals": 0.7,
    "fertilizers": 0.72,
    "urea": 0.7,
    "ammonia": 0.68,
    "ethylene": 0.7,
    "polymers": 0.65,
    "plastics": 0.62,
    "solvents": 0.6,
 
    # Pharmaceuticals / APIs
    "active pharmaceutical ingredients": 0.75,
    "apis": 0.75,
    "excipients": 0.6,
 
    # Technology / Semiconductors
    "semiconductors": 0.82,
    "chips": 0.82,
    "silicon": 0.7,
    "polysilicon": 0.72,
}





# category fallback
CATEGORY_RISK_MAP = {
    "energy": 0.82,
    "agriculture": 0.68,
    "metals": 0.68,
    "precious metals": 0.6,
    "chemicals": 0.72,
    "technology": 0.65,
    "pharmaceuticals": 0.72,
    "industrials": 0.65,
}