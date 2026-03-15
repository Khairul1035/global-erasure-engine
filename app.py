import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import numpy as np

# ==========================================
# 1. HCI & BRANDING SETUP (SOFT THEME)
# ==========================================
st.set_page_config(page_title="GLOBAL WAR INVOICE", layout="wide")

# CSS untuk background lembut dan tulisan hitam
st.markdown("""
    <style>
    /* Background Utama - Soft Light Grey */
    .stApp {
        background-color: #F8F9FA;
    }
    
    /* Semua tulisan default jadi Hitam/Gelap */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #1A202C !important;
    }

    /* Metric Box - Putih bersih dengan border */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    [data-testid="stMetricValue"] {
        color: #2D3748 !important;
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        color: #4A5568 !important;
    }

    /* Receipt Box Styling - Putih Kertas & Tulisan Hitam Pekat */
    .receipt-container { 
        font-family: 'Courier New', Courier, monospace; 
        color: #000000 !important; 
        background-color: #ffffff !important; 
        padding: 30px; 
        border-radius: 5px; 
        border: 2px solid #1A202C; 
        box-shadow: 10px 10px 0px #CBD5E0;
        margin-top: 20px;
        min-height: 450px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #EDF2F7;
    }
    
    hr {
        border-top: 1px solid #CBD5E0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. DATA & LOGIC
# ==========================================
COUNTRY_PROFILES = {
    "Malaysia": {"type": "Net Exporter", "debt_risk": "Moderate", "proximity": "Medium", "usd_dep": 0.75},
    "United Kingdom": {"type": "Net Importer", "debt_risk": "Low", "proximity": "Low", "usd_dep": 0.50},
    "Jordan": {"type": "Net Importer", "debt_risk": "Critical", "proximity": "High", "usd_dep": 0.90},
    "Saudi Arabia": {"type": "Net Exporter", "debt_risk": "Low", "proximity": "High", "usd_dep": 0.80},
    "Germany": {"type": "Net Importer", "debt_risk": "Stable", "proximity": "Low", "usd_dep": 0.60},
    "Egypt": {"type": "Net Importer", "debt_risk": "Critical", "proximity": "High", "usd_dep": 0.85}
}

@st.cache_data(ttl=300)
def fetch_mkt():
    try:
        # Data simulasi jika yfinance lambat
        return {"Oil": 86.45, "USD": 104.12, "Panic": 2150}
    except:
        return {"Oil": 85.0, "USD": 104.0, "Panic": 2100.0}

mkt = fetch_mkt()

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:
    st.header("👤 Project Architect")
    st.markdown("""
    **Mohd Khairul Ridhuan**  
    *Expertise:*
    - Maqasid Shariah
    - Financial Criminology
    - Artificial Intelligence
    """)
    st.divider()
    st.header("⚙️ Parameters")
    escalation = st.select_slider("Conflict Escalation", 
                                  options=["Peace", "Localized", "High Tension", "Regional War", "Total War"],
                                  value="Localized")
    st.success("System: Ready")

# ==========================================
# 4. MAIN DASHBOARD
# ==========================================
st.title("🌐 THE GLOBAL WAR INVOICE")
st.markdown("### *Strategic Intelligence Dashboard*")

# Metrics
c1, c2, c3 = st.columns(3)
with c1: st.metric("Brent Oil", f"${mkt['Oil']}", escalation)
with c2: st.metric("USD Index", f"{mkt['USD']}", "Currency Risk")
with c3: st.metric("Neural Stress", f"{mkt['Panic']} Hz", "Market Volatility")

st.divider()

# Selection
st.subheader("📋 Comparative National Audit")
sel1, sel2, sel3 = st.columns(3)
with sel1: country1 = st.selectbox("Select Country A:", list(COUNTRY_PROFILES.keys()), index=0)
with sel2: country2 = st.selectbox("Select Country B:", list(COUNTRY_PROFILES.keys()), index=4)
with sel3: country3 = st.selectbox("Select Country C:", list(COUNTRY_PROFILES.keys()), index=3)

def generate_invoice(name, market, esc_level):
    profile = COUNTRY_PROFILES[name]
    esc_mod = {"Peace": 0.5, "Localized": 1.2, "High Tension": 2.5, "Regional War": 5.0, "Total War": 10.0}[esc_level]
    
    energy_tax = (market['Oil'] - 70) * (0.9 if profile["type"] == "Net Importer" else 0.2) * esc_mod
    inf_tax = (market['USD'] - 100) * profile["usd_dep"] * esc_mod
    
    st.markdown(f"""
    <div class="receipt-container">
        <center>
            <h2 style="color:black !important; margin-bottom:0;">OFFICIAL INVOICE</h2>
            <p style="color:black !important; margin-top:0;"><b>SOVEREIGNTY EROSION</b></p>
        </center>
        <hr style="border-top: 2px dashed black !important;">
        <p style="color:black !important;"><b>NATION:</b> {name.upper()}</p>
        <p style="color:black !important;"><b>TYPE:</b> {profile['type']}</p>
        <p style="color:black !important;"><b>DEBT RISK:</b> {profile['debt_risk']}</p>
        <hr style="border-top: 1px dashed black !important;">
        <p style="color:black !important;">1. ENERGY SURCHARGE ... +{energy_tax:.2f}%</p>
        <p style="color:black !important;">2. INFLATION TAX ...... +{inf_tax:.2f}%</p>
        <p style="color:black !important;">3. KINETIC RISK ....... {profile['proximity']}</p>
        <p style="color:black !important;">4. MAQASID INTEGRITY .. ERODING</p>
        <br><br>
        <hr style="border-top: 2px solid black !important;">
        <center>
            <b style="color:black !important;">TOTAL COST: NATION AT RISK</b><br>
            <small style="color:black !important;">"The price of global instability."</small>
        </center>
    </div>
    """, unsafe_allow_html=True)

# Output Invoices
res1, res2, res3 = st.columns(3)
with res1: generate_invoice(country1, mkt, escalation)
with res2: generate_invoice(country2, mkt, escalation)
with res3: generate_invoice(country3, mkt, escalation)

st.divider()
st.info(f"**Briefing:** At **{escalation}** level, {country1} experiences indirect fiscal 'theft' through supply chain disruption.")
