import streamlit as st
import plotly.graph_objects as go

# ==============================
# Page config
# ==============================
st.set_page_config(
    page_title="Province Map Visualization",
    page_icon="🗺️",
    layout="centered"
)

# ==============================
# Title
# ==============================
st.title("🗺️ Province Map Visualization")

st.markdown(
    """
    Select a province and multiple cities to display a map of their connections.
    Each line represents a connection between cities within that province.
    """
)

# ==============================
# Data provinsi dan kota (dengan latitude & longitude)
# ==============================
province_cities = {
    "West Java": {
        "Bandung": (-6.9175, 107.6191),
        "Bogor": (-6.5975, 106.8066),
        "Depok": (-6.4025, 106.7944),
        "Bekasi": (-6.234, 107.0057),
        "Cimahi": (-6.8996, 107.5422),
        "Sukabumi": (-6.9233, 106.9297),
        "Cirebon": (-6.732, 108.552)
    },
    "Banten": {
        "Serang": (-6.1203, 106.1506),
        "Tangerang": (-6.178, 106.6315),
        "Cilegon": (-5.999, 105.964),
        "Pandeglang": (-6.769, 105.866),
        "Lebak": (-6.500, 106.000)
    },
    "Jakarta": {
        "Central Jakarta": (-6.1862, 106.8283),
        "West Jakarta": (-6.1744, 106.7794),
        "South Jakarta": (-6.2564, 106.8456),
        "East Jakarta": (-6.2389, 106.8956),
        "North Jakarta": (-6.1213, 106.865)
    },
    "Central Java": {
        "Semarang": (-6.9667, 110.4167),
        "Surakarta": (-7.5667, 110.8167),
        "Magelang": (-7.4681, 110.2155),
        "Purwokerto": (-7.434, 109.233),
        "Tegal": (-6.8697, 109.1389)
    },
    "East Java": {
        "Surabaya": (-7.2458, 112.7378),
        "Malang": (-7.9811, 112.6308),
        "Kediri": (-7.8533, 112.0019),
        "Madiun": (-7.6347, 111.5164),
        "Blitar": (-8.0917, 112.1517),
        "Pasuruan": (-7.6481, 112.9108)
    },
    "DI Yogyakarta": {
        "Yogyakarta": (-7.7956, 110.3695),
        "Sleman": (-7.7196, 110.4074),
        "Bantul": (-7.9455, 110.3230),
        "Gunungkidul": (-8.0256, 110.6126),
        "Kulon Progo": (-7.7975, 110.0942)
    }
}

# ==============================
# Pilih provinsi & kota
# ==============================
province = st.selectbox("Select a province:", list(province_cities.keys()))
selected_cities = st.multiselect(
    "Select cities to show:",
    options=list(province_cities[province].keys()),
    default=[list(province_cities[province].keys())[0]]
)

# ==============================
# Generate map
# ==============================
if st.button("Generate Map"):
    if len(selected_cities) < 2:
        st.warning("Select at least two cities to visualize connections 💡")
    else:
        # Koordinat untuk map
        lats = [province_cities[province][city][0] for city in selected_cities]
        lons = [province_cities[province][city][1] for city in selected_cities]

        # Buat garis koneksi antar kota
        edge_traces = []
        for i in range(len(selected_cities)-1):
            for j in range(i+1, len(selected_cities)):
                edge_traces.append(
                    go.Scattermapbox(
                        lat=[lats[i], lats[j]],
                        lon=[lons[i], lons[j]],
                        mode='lines',
                        line=dict(width=1, color="#000000"),
                        hoverinfo='none'
                    )
                )

        # Buat titik kota pakai marker 📍
        node_trace = go.Scattermapbox(
            lat=lats,
            lon=lons,
            mode='markers+text',
            marker=go.scattermapbox.Marker(
                size=10,
                color="#ff80b3"
            ),
            text=[f"📍 {city}" for city in selected_cities],
            textposition="top right",
            hoverinfo='text'
        )

        # Gabungkan semua
        fig = go.Figure(data=edge_traces + [node_trace])
        fig.update_layout(
            mapbox_style="open-street-map",  # bisa ganti ke 'carto-darkmatter' untuk map gelap
            mapbox_zoom=6,
            mapbox_center={"lat": sum(lats)/len(lats), "lon": sum(lons)/len(lons)},
            margin={"l":0,"r":0,"t":50,"b":0},
            title=f"City Connections in {province}",
            title_x=0.5
        )

        st.plotly_chart(fig, use_container_width=True)

        # Success message pink
        st.markdown(f"""
            <div style="
                background-color: #ffe6f0;
                color: #cc0066;
                padding: 12px;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 16px;">
                (/≧▽≦)/ Successfully generated a city connection map with {len(selected_cities)} cities in {province}!
            </div>
        """, unsafe_allow_html=True)