import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import numpy as np

# ==========================================
# 1. SETTING THEME & UI (SOFT & CLEAN)
# ==========================================
st.set_page_config(page_title="GLOBAL WAR INVOICE V7", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F0F2F6; }
    h1, h2, h3, p, span, label, .stSelectbox label { color: #1A1A1A !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Card Styling */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        text-align: center;
    }
    
    /* Receipt Styling */
    .receipt-container { 
        font-family: 'Courier New', Courier, monospace; 
        color: #000000 !important; 
        background-color: #ffffff !important; 
        padding: 25px; 
        border: 2px solid #333; 
        box-shadow: 8px 8px 0px #A0AEC0;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. GLOBAL DATA ENGINE
# ==========================================
@st.cache_data
def get_world_data():
    # Menggunakan senarai negara standard dari Plotly
    df = px.data.gapminder().query("year == 2007")
    countries = df['country'].unique()
    return countries

def calculate_risk_score(region, escalation_level):
    # Logik risiko berdasarkan wilayah (Simulasi)
    base_scores = {
        'Asia': 40, 'Europe': 30, 'Africa': 50, 
        'Americas': 25, 'Oceania': 20, 'Middle East': 85
    }
    esc_mult = {"Peace": 0.2, "Localized": 1.0, "High Tension": 1.8, "Regional War": 3.5, "Total War": 7.0}
    return base_scores.get(region, 30) * esc_mult[escalation_level]

# Fetch Real-time Market Data
@st.cache_data(ttl=300)
def fetch_market():
    try:
        oil = yf.Ticker("BZ=F").history(period="1d")['Close'].iloc[-1]
        usd = yf.Ticker("DX-Y.NYB").history(period="1d")['Close'].iloc[-1]
        return {"Oil": round(oil, 2), "USD": round(usd, 2)}
    except:
        return {"Oil": 86.50, "USD": 104.20}

mkt = fetch_market()
all_countries = get_world_data()

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.header("👤 Strategic Architect")
    st.write("**Mohd Khairul Ridhuan**")
    st.divider()
    
    st.subheader("⚙️ Global Scenario")
    escalation = st.select_slider(
        "Tahap Eskalasi Konflik",
        options=["Peace", "Localized", "High Tension", "Regional War", "Total War"],
        value="Localized"
    )
    
    st.divider()
    selected_country = st.selectbox("Cari Negara Spesifik:", sorted(all_countries), index=83) # Default: Malaysia
    st.info("Peta dan invois akan berubah secara automatik apabila parameter diubah.")

# ==========================================
# 4. INTERACTIVE VISUALIZATION (MAP)
# ==========================================
st.title("🌐 GLOBAL WAR INVOICE ENGINE")
st.markdown("##### *Sistem Pemantauan Integriti Kedaulatan Negara (Versi Global)*")

# Row 1: Market Metrics
c1, c2, c3 = st.columns(3)
with c1: 
    st.markdown(f'<div class="metric-card"><h3>Harga Minyak</h3><h2>${mkt["Oil"]}</h2><p>Brent Crude</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><h3>Indeks Dolar</h3><h2>{mkt["USD"]}</h2><p>USD Dominance</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><h3>Escalation</h3><h2>{escalation}</h2><p>Conflict Level</p></div>', unsafe_allow_html=True)

st.write("---")

# Row 2: World Risk Map
st.subheader("🗺️ Global Risk Projection Map")
# Generate data untuk peta
map_data = px.data.gapminder().query("year == 2007")
map_data['Risk_Impact'] = map_data.apply(lambda row: calculate_risk_score(row['continent'], escalation), axis=1)

fig = px.choropleth(
    map_data, 
    locations="iso_alpha",
    color="Risk_Impact",
    hover_name="country",
    color_continuous_scale="Reds",
    projection="natural earth",
    title=f"Unjuran Impak Ekonomi Global pada tahap: {escalation}"
)
fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 5. DYNAMIC WAR INVOICE
# ==========================================
st.divider()
st.subheader(f"📋 War Invoice: {selected_country}")

col_left, col_right = st.columns([1, 2])

with col_left:
    # Logic Invois
    esc_val = {"Peace": 0.5, "Localized": 1.5, "High Tension": 3.0, "Regional War": 6.0, "Total War": 12.0}[escalation]
    energy_tax = (mkt['Oil'] - 70) * esc_val * 0.5
    currency_loss = (mkt['USD'] - 100) * esc_val * 0.8
    total_erosion = energy_tax + currency_loss

    st.markdown(f"""
    <div class="receipt-container">
        <center>
            <h2 style="color:black;">WAR INVOICE</h2>
            <p style="color:black;">Audit No: #{np.random.randint(100000, 999999)}</p>
        </center>
        <hr style="border-top: 2px dashed black;">
        <p style="color:black;"><b>NEGARA:</b> {selected_country.upper()}</p>
        <p style="color:black;"><b>STATUS:</b> SOVEREIGN ENTITY</p>
        <hr style="border-top: 1px dashed black;">
        <p style="color:black;">KOS TENAGA (HIDDEN) ... +{energy_tax:.2f}%</p>
        <p style="color:black;">KEHILANGAN FIAT ...... +{currency_loss:.2f}%</p>
        <p style="color:black;">TEKANAN SOSIAL ....... {escalation.upper()}</p>
        <hr style="border-top: 1px dashed black;">
        <h3 style="color:black; text-align:center;">HIFZ AL-MAL EROSION:</h3>
        <h2 style="color:red; text-align:center;">{total_erosion:.2f}%</h2>
        <hr style="border-top: 2px solid black;">
        <center><small style="color:black;">Generated by Mohd Khairul Ridhuan Intelligence Engine</small></center>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.write("### Strategist Analysis")
    st.info(f"""
    **Analisis untuk {selected_country}:**
    1. **Impak Ekonomi:** Pada tahap **{escalation}**, {selected_country} terpaksa membayar "cukai perang tersembunyi" sebanyak {total_erosion:.2f}% akibat kenaikan kos logistik global.
    2. **Kedaulatan (Maqasid):** Pelanggaran prinsip *Hifz al-Mal* berlaku kerana kuasa beli rakyat semakin mengecil tanpa peperangan fizikal di tanah air sendiri.
    3. **Tindakan Strategik:** Disyorkan untuk mempelbagaikan rizab mata wang dan mengurangkan kebergantungan kepada rantaian bekalan yang dikawal oleh kuasa besar.
    """)
    
    # Chart Trend Ringkas
    chart_data = pd.DataFrame({
        'Kategori': ['Tenaga', 'Matawang', 'Sosial', 'Makanan'],
        'Tahap Risiko': [energy_tax, currency_loss, esc_val*10, esc_val*15]
    })
    fig_bar = px.bar(chart_data, x='Kategori', y='Tahap Risiko', color='Kategori', color_discrete_sequence=px.colors.sequential.Reds_r)
    st.plotly_chart(fig_bar, use_container_width=True)

st.caption("© 2026 | Mohd Khairul Ridhuan | Strategic Geopolitical Auditor")
