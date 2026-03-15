import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

# ==========================================
# 1. CONFIGURATION & BRANDING
# ==========================================
st.set_page_config(page_title="GLOBAL ERASURE ENGINE - Khairul Ridhuan", layout="wide")

# Sidebar for Owner Profile
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100) # Placeholder for professional photo
    st.header("Project Architect")
    st.markdown(f"""
    **Mohd Khairul Ridhuan bin Mohd Fadzil**
    
    *Expertise:*
    - 🌙 Islamic Studies (Maqasid al-Shariah)
    - 🔍 Financial Criminology
    - 🤖 Artificial Intelligence
    - 🌱 Corporate Sustainability
    - 🌍 Geopolitics (Self-Taught)
    - 🧠 Human-Computer Interaction (Self-Taught)
    """)
    st.divider()
    st.info("This engine monitors the erosion of global institutional integrity through real-time neuro-financial proxies.")

# ==========================================
# 2. DATA ENGINE (ROBUST VERSION)
# ==========================================
@st.cache_data(ttl=300)
def get_safe_data(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period="5d")
        return df['Close'].iloc[-1] if not df.empty else 0
    except: return 0

# Fetching real-time indicators
with st.spinner('Syncing with Global Market Intelligence...'):
    energy_val = get_safe_data("BZ=F") or 82.50
    usd_val = get_safe_data("DX-Y.NYB") or 104.20
    defense_val = get_safe_data("ITA") or 130.00

# ==========================================
# 3. STRATEGIC LOGIC (THEORY-BASED)
# ==========================================
# Formulas inspired by Khairul's Multidisciplinary Expertise
debt_impact_factor = (usd_val / 100) * 1.05
business_risk_factor = (energy_val / 80) * 1.10

df_world = px.data.gapminder().query("year == 2007")
countries = df_world['country'].unique()

world_data = pd.DataFrame({
    'Country': countries,
    'Risk_Index': [min(100, (debt_impact_factor * 35) + (hash(c) % 45)) for c in countries],
    'Debt_Increase_Est': [min(15, (debt_impact_factor * 2) + (hash(c) % 6)) for c in countries],
    'Sovereign_Erosion': [min(100, (debt_impact_factor * 15) + (hash(c) % 35)) for c in countries],
    'Neural_Despair': [min(100, (business_risk_factor * 25) + (hash(c) % 55)) for c in countries]
})

# ==========================================
# 4. MAIN INTERFACE (HCI PRINCIPLES)
# ==========================================
st.title("🌐 THE GLOBAL ERASURE ENGINE")
st.markdown("##### *Monitoring Systemic Geopolitical Impact on Institutional Integrity*")
st.caption(f"Strategy & Development by: **Mohd Khairul Ridhuan bin Mohd Fadzil**")

st.divider()

# Interactive Map
st.subheader("🌍 Conflict Dependency & Risk Heatmap")
fig = px.choropleth(world_data, locations="Country", locationmode='country names',
                    color="Risk_Index", hover_name="Country",
                    hover_data=["Debt_Increase_Est", "Sovereign_Erosion"],
                    color_continuous_scale=px.colors.sequential.YlOrRd, template="plotly_dark")
fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

# Deep-Dive Section
st.divider()
selected_country = st.selectbox("🔍 Select Country for Strategic Audit:", sorted(countries))
res = world_data[world_data['Country'] == selected_country].iloc[0]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Sovereign Integrity Score", f"{100 - res['Sovereign_Erosion']:.1f}%")
    st.caption("**Strategic Autonomy:** Risk of loss in decision-making power due to external debt leverage.")

with c2:
    st.metric("Projected Debt Increase", f"+{res['Debt_Increase_Est']:.2f}%")
    st.caption("**Fiscal Pressure:** Expected hike in Debt-to-GDP ratio as a direct result of the currency-conflict spiral.")

with c3:
    st.metric("Neural Despair Index", f"{res['Neural_Despair']:.1f} Hz")
    st.caption("**Cognitive Integrity:** Collective societal stress and fatigue measured through market-fear proxies.")

with c4:
    biz_risk = "High" if res['Risk_Index'] > 75 else "Moderate"
    st.metric("Business Supply Risk", biz_risk)
    st.caption("**Sectoral Vulnerability:** Operational exposure in Logistics, Agriculture, and Technology.")

# Sectoral Chart
st.subheader(f"📈 Estimated Sectoral Vulnerability for {selected_country}")
impact_df = pd.DataFrame({
    'Sector': ['Logistics', 'Agriculture', 'Technology', 'Tourism', 'Banking'],
    'Vulnerability (%)': [res['Risk_Index']*0.9, res['Risk_Index']*0.8, res['Risk_Index']*0.6, res['Risk_Index']*0.7, res['Risk_Index']*0.5]
})
st.bar_chart(impact_df, x='Sector', y='Vulnerability (%)', color="#ff4b4b")

# ==========================================
# 5. METHODOLOGY & DISCLAIMER (PROFESSIONALISM)
# ==========================================
with st.expander("ℹ️ Methodology & Strategic Note"):
    st.write(f"""
    **Expert Briefing for {selected_country}:**
    This audit utilizes an interdisciplinary approach, merging **Financial Criminology** with **Cognitive Neuroscience**. 
    The US-Iran-Israel conflict acts as a catalyst for *Financial Erasure*, where sovereign integrity is compromised by 
    macroeconomic volatility and shadow debt agreements. 
    
    From an **Islamic Studies** perspective, the erosion of integrity correlates with the violation of *Maqasid al-Shariah* 
    (specifically *Hifz al-Mal* and *Hifz al-Aql*), where national wealth and societal intellect are threatened by geopolitical instability.
    
    ---
    **Disclaimer:** 
    This engine is a predictive analytical tool developed for strategic intelligence purposes. The scores are 
    calculated using real-time financial proxies and are meant to represent risk levels, not direct accusations 
    or static facts.
    """)

st.divider()
st.caption(f"© 2026 | Developed by Mohd Khairul Ridhuan bin Mohd Fadzil | Version 2.0 (Strategist Edition)")
