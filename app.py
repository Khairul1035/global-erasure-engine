import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

st.set_page_config(page_title="GLOBAL ERASURE ENGINE", layout="wide")
st.title("🌐 THE GLOBAL ERASURE ENGINE")
st.markdown("### Strategic Intelligence: US/Israel vs Iran - Global Impact Analysis")

@st.cache_data(ttl=60)
def get_world_proxies():
    tickers = {"Energy": "BZ=F", "Defense": "ITA", "USD_Strength": "DX-Y.NYB"}
    return {name: yf.Ticker(sym).history(period="1d", interval="1m")['Close'].iloc[-1] for name, sym in tickers.items()}

market_data = get_world_proxies()
df_world = px.data.gapminder().query("year == 2007")
countries = df_world['country'].unique()
risk_multiplier = (market_data['Energy'] / 80) + (market_data['USD_Strength'] / 100)

world_risk_data = pd.DataFrame({
    'Country': countries,
    'Risk_Index': [min(100, (risk_multiplier * 35) + (hash(c) % 40)) for c in countries],
    'Neural_Despair': [min(100, (risk_multiplier * 25) + (hash(c) % 50)) for c in countries],
    'Sovereign_Erosion': [min(100, (risk_multiplier * 15) + (hash(c) % 30)) for c in countries]
})

st.subheader("🌍 Interactive Conflict Dependency Map (Click any country)")
fig = px.choropleth(world_risk_data, locations="Country", locationmode='country names',
                    color="Risk_Index", hover_name="Country",
                    hover_data=["Neural_Despair", "Sovereign_Erosion"],
                    color_continuous_scale=px.colors.sequential.YlOrRd, template="plotly_dark")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
selected_country = st.selectbox("🔍 Select a country for a Strategic Audit:", sorted(countries))
res = world_risk_data[world_risk_data['Country'] == selected_country].iloc[0]

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(f"{selected_country} Risk Index", f"{res['Risk_Index']:.1f}%")
with c2:
    st.metric("Neural Despair Index", f"{res['Neural_Despair']:.1f} Hz")
with c3:
    st.metric("Sovereign Integrity", f"{100 - res['Sovereign_Erosion']:.1f}%")

st.info(f"**Strategist Briefing:** Global conflict volatility is currently eroding the institutional integrity of {selected_country}. High neural despair indicates rising cognitive fatigue in the population.")
