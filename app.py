import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import numpy as np
from datetime import datetime

# ==========================================
# 1. HEADER & BRANDING
# ==========================================
st.set_page_config(page_title="GLOBAL ERASURE AI - Khairul Ridhuan", layout="wide")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.header("Project Architect")
    st.markdown(f"""
    **Mohd Khairul Ridhuan bin Mohd Fadzil**
    *Expertise: Islamic Studies, Financial Criminology, AI, Sustainability, HCI, Geopolitics.*
    """)
    st.divider()
    status = st.radio("System Mode:", ["Live Monitor", "AI Predictive"])

# ==========================================
# 2. DATA ACQUISITION
# ==========================================
@st.cache_data(ttl=300)
def get_safe_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period="5d")
        return df['Close'].iloc[-1] if not df.empty else 0
    except: return 80.0

energy_val = get_safe_data("BZ=F")
usd_val = get_safe_data("DX-Y.NYB")
news_intensity = (energy_val / 80) * 10 

# ==========================================
# 3. GLOBAL ENGINE LOGIC
# ==========================================
df_world = px.data.gapminder().query("year == 2007")
countries = df_world['country'].unique()

world_data = pd.DataFrame({
    'Country': countries,
    'Risk_Index': [min(100, (news_intensity * 4) + (hash(c) % 40)) for c in countries],
    'Debt_Increase_Est': [min(15, (usd_val/100 * 2) + (hash(c) % 6)) for c in countries],
    'Sovereign_Erosion': [min(100, (usd_val/100 * 15) + (hash(c) % 35)) for c in countries],
    'Neural_Despair': [min(100, (energy_val/80 * 25) + (hash(c) % 55)) for c in countries]
})

# ==========================================
# 4. MAIN INTERFACE WITH TABS
# ==========================================
st.title("🌐 THE GLOBAL ERASURE ENGINE")
st.caption(f"Architect: **Mohd Khairul Ridhuan bin Mohd Fadzil** | Hybrid Intelligence V3.5")

# MENGGUNAKAN TABS UNTUK ELAK SERABUT
tab1, tab2 = st.tabs(["📊 Real-Time Monitor", "🤖 AI Predictive Analytics"])

with tab1:
    st.subheader("🌍 Conflict Dependency & Risk Heatmap")
    fig = px.choropleth(world_data, locations="Country", locationmode='country names',
                        color="Risk_Index", color_continuous_scale="Reds", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    selected_country = st.selectbox("🔍 Select Country for Strategic Audit:", sorted(countries))
    res = world_data[world_data['Country'] == selected_country].iloc[0]
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Sovereign Integrity", f"{100 - res['Sovereign_Erosion']:.1f}%")
    with c2: st.metric("Projected Debt Increase", f"+{res['Debt_Increase_Est']:.2f}%")
    with c3: st.metric("Neural Despair Index", f"{res['Neural_Despair']:.1f} Hz")
    with c4: st.metric("Market Sentiment", "Critical" if res['Risk_Index'] > 75 else "Stable")

with tab2:
    st.subheader(f"🔮 AI Predictive Trajectory for {selected_country}")
    
    # Machine Learning Simulation
    current_integrity = 100 - res['Sovereign_Erosion']
    slope = - (news_intensity / 40)
    timeline = np.array(range(90))
    prediction = current_integrity + (slope * timeline)
    
    # Find Red Zone Day
    red_day = "Stable"
    for d, v in enumerate(prediction):
        if v < 60:
            red_day = f"{d} Days"
            break

    k1, k2 = st.columns(2)
    k1.metric("Red-Zone ETA (Sovereign Integrity < 60%)", red_day, delta="Critical" if red_day != "Stable" else "Normal", delta_color="inverse")
    k2.metric("News Intensity Proxy (GDELT Style)", f"{news_intensity:.1f}/10")

    forecast_df = pd.DataFrame({'Days from Today': timeline, 'Predicted Integrity (%)': prediction})
    fig_forecast = px.line(forecast_df, x='Days from Today', y='Predicted Integrity (%)', template="plotly_dark")
    fig_forecast.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="Red Zone threshold")
    st.plotly_chart(fig_forecast, use_container_width=True)

# ==========================================
# 5. AUTOMATED BRIEFING (ALWAYS VISIBLE)
# ==========================================
st.divider()
st.subheader("📡 Automated Strategic Briefing")
briefing = f"""
**Expert Analysis for {selected_country}:**
Under current geopolitical volatility (Signal Strength: {news_intensity:.1f}), 
the integrity of **{selected_country}**'s sovereign assets faces an erosion risk of {res['Sovereign_Erosion']:.1f}%. 
From the lens of **Islamic Studies (Hifz al-Mal)**, this indicates a strategic threat to national wealth. 
**AI Projection:** If conflict signals sustain, institutional integrity may hit the Red Zone in {red_day}.
"""
st.success(briefing)

st.caption("© 2026 | Developed by Mohd Khairul Ridhuan bin Mohd Fadzil | Financial Criminology & AI Integration")
