import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import numpy as np

# ==========================================
# 1. UI CONFIGURATION (SOFT THEME)
# ==========================================
st.set_page_config(page_title="WAR INVOICE ENGINE V8", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F4F7F9; }
    h1, h2, h3, h4, p, span, label { color: #1A1A1A !important; }
    
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        text-align: center;
    }

    .receipt-container { 
        font-family: 'Courier New', Courier, monospace; 
        color: #000000 !important; 
        background-color: #ffffff !important; 
        padding: 30px; 
        border: 2px solid #000; 
        box-shadow: 12px 12px 0px #CBD5E0;
    }

    .analysis-box {
        background-color: #EBF4FF;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3182CE;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. REAL-TIME DATA & INTELLIGENCE ENGINE
# ==========================================
@st.cache_data(ttl=600)
def fetch_live_market():
    try:
        # Fetching Live Data
        oil_data = yf.Ticker("BZ=F").history(period="1d")
        usd_data = yf.Ticker("DX-Y.NYB").history(period="1d")
        
        oil_price = oil_data['Close'].iloc[-1]
        usd_index = usd_data['Close'].iloc[-1]
        
        # Calculate changes
        oil_change = ((oil_price - oil_data['Open'].iloc[-1]) / oil_data['Open'].iloc[-1]) * 100
        return {"Oil": round(oil_price, 2), "USD": round(usd_index, 2), "Oil_Change": round(oil_change, 2)}
    except:
        # Fallback if Yahoo Finance API fails
        return {"Oil": 85.50, "USD": 104.10, "Oil_Change": 1.2}

def get_country_intelligence(country_name, mkt_data, escalation_level):
    """The brain of the dashboard: Generates specific data per country."""
    
    # Mapping country types
    oil_exporters = ["Saudi Arabia", "Iran", "Iraq", "United Arab Emirates", "Kuwait", "Norway", "Canada", "United States", "Malaysia"]
    conflict_zone = ["Iran", "Israel", "Jordan", "Lebanon", "Syria", "Egypt", "Iraq"]
    
    # Base Multipliers based on Escalation
    esc_mult = {"Peace": 0.1, "Localized": 1.0, "High Tension": 2.5, "Regional War": 5.0, "Total War": 10.0}[escalation_level]
    
    # 1. Energy Impact
    if country_name in oil_exporters:
        energy_impact = (mkt_data['Oil'] - 75) * 0.2 * esc_mult # Benefit/Low tax for exporters
        econ_type = "Net Exporter (Resilient)"
    else:
        energy_impact = (mkt_data['Oil'] - 75) * 1.5 * esc_mult # High tax for importers
        econ_type = "Net Importer (Vulnerable)"
        
    # 2. Sovereignty/Geopolitical Risk
    if country_name in conflict_zone:
        geo_risk = 85 * (esc_mult / 2)
        proximity = "High (Conflict Epicenter)"
    else:
        geo_risk = 20 * esc_mult
        proximity = "Moderate (Supply Chain Link)"
        
    # 3. Specific Analysis Text
    if country_name == "Iran":
        analysis = "Direct kinetic risk. Sanctions-driven currency volatility is the primary 'War Tax' on citizens."
    elif country_name == "Malaysia":
        analysis = "Strategic trade vulnerability. Despite being an oil exporter, high reliance on global electronics supply chains creates industrial fragility."
    elif country_name in oil_exporters:
        analysis = "Economic buffer exists due to energy exports, but fiscal sovereignty is threatened by global USD hegemony."
    else:
        analysis = "Severe purchasing power erosion. National reserves are being depleted to subsidize energy and food imports."

    return {
        "energy": round(energy_impact, 2),
        "geo": round(geo_risk, 2),
        "type": econ_type,
        "proximity": proximity,
        "analysis": analysis
    }

# Load Data
mkt = fetch_live_market()
world_df = px.data.gapminder().query("year == 2007")
country_list = sorted(world_df['country'].unique())

# ==========================================
# 3. DASHBOARD LAYOUT
# ==========================================
st.title("🌐 GLOBAL WAR INVOICE ENGINE")
st.markdown("##### *Strategic Intelligence Audit: Real-Time Sovereignty Loss Tracking*")

# Top Metrics Bar
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><h3>Live Brent Oil</h3><h2 style="color:#E53E3E">${mkt["Oil"]}</h2><p>{mkt["Oil_Change"]}% today</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><h3>USD Index (DXY)</h3><h2 style="color:#3182CE">{mkt["USD"]}</h2><p>Currency Hegemony</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><h3>Escalation</h3><h2 style="color:#DD6B20">{st.sidebar.select_slider("Conflict Level", options=["Peace", "Localized", "High Tension", "Regional War", "Total War"], value="High Tension", key="esc_slider")}</h2><p>Risk Multiplier</p></div>', unsafe_allow_html=True)
with c4:
    selected_country = st.sidebar.selectbox("Target Country Audit:", country_list, index=country_list.index("Iran") if "Iran" in country_list else 0)
    st.markdown(f'<div class="metric-card"><h3>Auditing</h3><h2 style="color:#2D3748">{selected_country}</h2><p>Live Selection</p></div>', unsafe_allow_html=True)

# Process Intelligence for Selected Country
intel = get_country_intelligence(selected_country, mkt, st.session_state.esc_slider)

st.divider()

# ==========================================
# 4. MAP & INVOICE SECTION
# ==========================================
col_map, col_invoice = st.columns([2, 1])

with col_map:
    st.subheader("🌍 Global Risk Projection Map")
    # Dynamic Map Data
    map_data = world_df.copy()
    map_data['Risk_Index'] = map_data.apply(lambda x: get_country_intelligence(x['country'], mkt, st.session_state.esc_slider)['energy'], axis=1)
    
    fig = px.choropleth(
        map_data, locations="iso_alpha", color="Risk_Index",
        hover_name="country", color_continuous_scale="Reds",
        projection="natural earth", template="plotly_white"
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=500)
    st.plotly_chart(fig, use_container_width=True)

with col_invoice:
    st.markdown(f"""
    <div class="receipt-container">
        <center>
            <h2 style="margin:0;">WAR INVOICE</h2>
            <small>AUDIT ID: {np.random.randint(100000, 999999)}</small>
        </center>
        <hr style="border-top: 2px dashed #000;">
        <p><b>COUNTRY:</b> {selected_country.upper()}</p>
        <p><b>ECON TYPE:</b> {intel['type']}</p>
        <p><b>PROXIMITY:</b> {intel['proximity']}</p>
        <hr style="border-top: 1px dashed #000;">
        <p>1. ENERGY SURCHARGE .... +{intel['energy']}%</p>
        <p>2. FIAT DEVALUATION ... +{intel['geo']/2:.2f}%</p>
        <p>3. NEURAL PANIC LOAD .. {st.session_state.esc_slider.upper()}</p>
        <p>4. SUPPLY CHAIN TAX ... +{intel['geo']:.2f}%</p>
        <hr style="border-top: 1px dashed #000;">
        <center>
            <h3 style="margin:0;">TOTAL INTEGRITY LOSS</h3>
            <h1 style="color:#E53E3E; margin:0;">{intel['energy'] + intel['geo']:.1f}%</h1>
        </center>
        <hr style="border-top: 2px solid #000;">
        <center><small>Processed by AI Strategic Architect</small></center>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. STRATEGIC ANALYSIS
# ==========================================
st.divider()
st.subheader(f"📡 Strategist Analysis Briefing: {selected_country}")

a1, a2 = st.columns([2, 1])

with a1:
    st.markdown(f"""
    <div class="analysis-box">
        <h4>Executive Summary for {selected_country}:</h4>
        <p>Under the <b>{st.session_state.esc_slider}</b> scenario, the primary threat to {selected_country} is <b>{intel['analysis']}</b></p>
        <ul>
            <li><b>Hifz al-Mal (Wealth Integrity):</b> The citizens of {selected_country} are losing purchasing power via "Hidden War Taxes" embedded in fuel and imported goods.</li>
            <li><b>Sovereignty Alert:</b> High reliance on USD-denominated trade means national policy is currently dictated by external conflict volatility.</li>
            <li><b>Recommendation:</b> Shift towards bilateral trade agreements and localized energy production to mitigate the "Global War Invoice."</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with a2:
    # Risk Breakdown Chart
    categories = ['Energy', 'Currency', 'Geopolitics', 'Social']
    values = [intel['energy'], intel['geo']/2, intel['geo'], 20]
    
    fig_radar = go.Figure(data=go.Scatterpolar(
      r=values, theta=categories, fill='toself',
      line_color='#3182CE'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=300, margin=dict(t=20, b=20))
    st.plotly_chart(fig_radar, use_container_width=True)

st.caption("© 2026 | Developed by Mohd Khairul Ridhuan | Strategic Intelligence Unit | Version 8.0")
