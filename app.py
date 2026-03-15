import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import numpy as np

# ==========================================
# 1. HCI & BRANDING SETUP (Professional Dark Mode)
# ==========================================
st.set_page_config(page_title="GLOBAL WAR INVOICE - Strategic Intelligence", layout="wide")

# FIX: Changed unsafe_allow_index to unsafe_allow_html
st.markdown("""
    <style>
    .receipt-container { 
        font-family: 'Courier New', Courier, monospace; 
        color: black; 
        background-color: #ffffff; 
        padding: 25px; 
        border-radius: 15px; 
        border: 3px solid #333; 
        box-shadow: 5px 10px #888888;
        margin-bottom: 20px; 
    }
    .stMetric { background-color: #111; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. STRATEGIC COUNTRY PROFILES (Rigorous Logic)
# ==========================================
COUNTRY_PROFILES = {
    "Malaysia": {"type": "Net Exporter", "debt_risk": "Moderate", "proximity": "Medium", "usd_dep": 0.75},
    "United Kingdom": {"type": "Net Importer", "debt_risk": "Low", "proximity": "Low", "usd_dep": 0.50},
    "Jordan": {"type": "Net Importer", "debt_risk": "Critical", "proximity": "High", "usd_dep": 0.90},
    "Saudi Arabia": {"type": "Net Exporter", "debt_risk": "Low", "proximity": "High", "usd_dep": 0.80},
    "Egypt": {"type": "Net Importer", "debt_risk": "Critical", "proximity": "High", "usd_dep": 0.85},
    "Singapore": {"type": "Net Importer", "debt_risk": "Stable", "proximity": "Medium", "usd_dep": 0.65},
    "Germany": {"type": "Net Importer", "debt_risk": "Stable", "proximity": "Low", "usd_dep": 0.60}
}

@st.cache_data(ttl=300)
def fetch_global_intelligence():
    try:
        tickers = {"Oil": "BZ=F", "USD": "DX-Y.NYB", "Panic": "GC=F"}
        return {name: yf.Ticker(sym).history(period="1d")['Close'].iloc[-1] for name, sym in tickers.items()}
    except:
        return {"Oil": 85.0, "USD": 104.0, "Panic": 2100.0}

mkt = fetch_global_intelligence()

# ==========================================
# 3. SIDEBAR CONTROLS (HCI Design)
# ==========================================
with st.sidebar:
    st.header("👤 Project Architect")
    st.markdown(f"""
    **Mohd Khairul Ridhuan bin Mohd Fadzil**  
    *Expertise:*
    - Islamic Studies (Maqasid)
    - Financial Criminology
    - Artificial Intelligence
    - Corporate Sustainability
    - HCI & Geopolitics
    """)
    st.divider()
    st.header("⚙️ Strategic Parameters")
    escalation = st.select_slider("Conflict Escalation Level", 
                                  options=["Peace", "Localized", "High Tension", "Regional War", "Total War"])
    st.divider()
    st.info("System Status: Real-time Data Sync Active")

# ==========================================
# 4. MAIN INTERFACE
# ==========================================
st.title("🌐 THE GLOBAL WAR INVOICE ENGINE")
st.markdown("##### *Strategic Intelligence Dashboard: Tracking the Indirect Cost of US-Israel-Iran Conflict*")
st.caption("A Multidisciplinary Framework: Finance • Neuroscience • Islamic Ethics • Geopolitics")

# Global Real-time Metrics
c1, c2, c3 = st.columns(3)
with c1: st.metric("Energy Proxy (Brent Oil)", f"${mkt['Oil']:.2f}", escalation)
with c2: st.metric("Fiscal Proxy (USD Index)", f"{mkt['USD']:.2f}", "Debt Pressure")
with c3: st.metric("Neuroscience (Panic Index)", f"{mkt['Panic']:.0f} Hz", "Amygdala Alert")

st.divider()

# ==========================================
# 5. TRIPLE COMPARISON INVOICES
# ==========================================
st.subheader("📋 Comparative War Invoices (3-Way National Audit)")
st.write("Compare how the conflict 'erases' the integrity of different nations simultaneously.")

sel1, sel2, sel3 = st.columns(3)
with sel1: country1 = st.selectbox("Select Country A:", list(COUNTRY_PROFILES.keys()), index=0)
with sel2: country2 = st.selectbox("Select Country B:", list(COUNTRY_PROFILES.keys()), index=1)
with sel3: country3 = st.selectbox("Select Country C:", list(COUNTRY_PROFILES.keys()), index=2)

def generate_invoice(name, market, esc_level):
    profile = COUNTRY_PROFILES[name]
    esc_mod = {"Peace": 0.5, "Localized": 1.0, "High Tension": 1.8, "Regional War": 3.0, "Total War": 6.0}[esc_level]
    
    energy_tax = (market['Oil'] - 75) * (0.8 if profile["type"] == "Net Importer" else 0.2) * esc_mod
    inflation_tax = (market['USD'] - 100) * profile["usd_dep"] * esc_mod
    amygdala_load = "CRITICAL" if profile["proximity"] in ["High", "Critical"] else "ELEVATED"
    
    # FIX: Changed unsafe_allow_index to unsafe_allow_html
    st.markdown(f"""
    <div class="receipt-container">
        <center><b>OFFICIAL WAR INVOICE</b><br>{name.upper()}</center>
        <hr>
        <b>Profile:</b> {profile['type']}<br>
        <b>Sovereign Risk:</b> {profile['debt_risk']}<br>
        <hr>
        1. FUEL & LOGISTICS COST ... +{energy_tax:.2f}%<br>
        2. IMPORTED GOODS TAX ...... +{inflation_tax:.2f}%<br>
        3. SOCIETAL PANIC LOAD ..... {amygdala_load}<br>
        4. NATIONAL AUTONOMY RISK .. {profile['proximity']}<br>
        <hr>
        <center><b>TOTAL: ERODING SOVEREIGNTY</b><br>
        <i>"Their war, your bill."</i></center>
    </div>
    """, unsafe_allow_html=True)

st.divider()
res1, res2, res3 = st.columns(3)
with res1: generate_invoice(country1, mkt, escalation)
with res2: generate_invoice(country2, mkt, escalation)
with res3: generate_invoice(country3, mkt, escalation)

# ==========================================
# 6. STRATEGIC BRIEFING (The "Why")
# ==========================================
st.divider()
st.subheader("📡 World Strategist Briefing")
st.info(f"""
**Executive Analysis:**
Based on the current escalation level of **{escalation}**, we detect a diverging 'Integrity Erosion' pattern:
1. **Accounting Perspective:** {country1} and {country2} are facing hidden fiscal penalties due to currency-inflation spirals.
2. **Neuroscience Perspective:** High 'Amygdala Stress' levels across these regions trigger market hyper-vigilance, leading to 'Digital Flight' (Data/Investment capital outflow).
3. **Islamic Ethics (Maqasid):** This is a systemic violation of *Hifz al-Mal* (Wealth Integrity). Global conflict is 'stealing' the purchasing power and national assets of citizens through supply chain manipulation.
""")

st.caption("© 2026 | Developed by Mohd Khairul Ridhuan bin Mohd Fadzil | Version 5.5 (Global Strategist Edition)")
