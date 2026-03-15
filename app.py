import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="THE EMPTY PLATE INDEX", layout="centered")

# 2. Styling (HCI - Make it look clean and impactful)
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    .plate-container {
        background-color: white;
        padding: 50px;
        border-radius: 50%;
        border: 10px solid #DEE2E6;
        width: 350px;
        height: 350px;
        margin: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .food-icon { font-size: 60px; margin: 10px; }
    h1, h2, h3 { color: #212529; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Fetching (Rigorous Real-time)
@st.cache_data(ttl=3600)
def get_live_data():
    # ZW=F (Wheat), ZC=F (Corn)
    tickers = {"Wheat": "ZW=F", "Corn": "ZC=F"}
    results = {}
    for name, sym in tickers.items():
        try:
            val = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
            results[name] = val
        except:
            results[name] = 600.0 # Fallback
    return results

data = get_live_data()
base_wheat = 550.0 # Price in peaceful times
base_corn = 450.0

# 4. Sidebar - The Strategy Control
st.sidebar.header("🌍 War Scenario")
war_tension = st.sidebar.select_slider(
    "Conflict Escalation (US/Israel vs Iran)",
    options=["Peace", "Tension", "Sanctions", "Blockade", "Total War"]
)

# Multiplier Logic
multiplier = {"Peace": 1.0, "Tension": 1.2, "Sanctions": 1.5, "Blockade": 2.0, "Total War": 3.0}[war_tension]

# Calculate portion size (Visual Erasure)
wheat_size = max(0.1, (base_wheat / data['Wheat']) / multiplier)
corn_size = max(0.1, (base_corn / data['Corn']) / multiplier)

# 5. UI Display
st.title("🍽️ THE EMPTY PLATE INDEX")
st.markdown("### *Module: The Empty Plate Index*")
st.write("Tracking how geopolitical conflict 'erases' food security in real-time.")

st.divider()

# The Visual Plate
st.markdown(f"""
    <div class="plate-container">
        <div class="food-icon" style="opacity: {wheat_size}; transform: scale({wheat_size});">🍞</div>
        <div class="food-icon" style="opacity: {corn_size}; transform: scale({corn_size});">🍗</div>
        <p style="color: grey; font-size: 12px;">Portion Capacity</p>
    </div>
    """, unsafe_allow_html=True)

total_loss = int((1 - ((wheat_size + corn_size) / 2)) * 100)
st.markdown(f"## **{total_loss}%** of your meal has been 'erased'")

# 6. Strategist Insight
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.info("**Why Bread?**\n\nBlockades in the Middle East stop fertilizer flow (Urea). No fertilizer = No Wheat.")
with col2:
    st.warning("**Why Chicken?**\n\nCorn is the primary animal feed. When war spikes shipping costs, the price of meat explodes.")

st.caption("Data: Live CBOT Commodities | Architect: Mohd Khairul Ridhuan")
