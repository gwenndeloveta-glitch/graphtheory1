import streamlit as st
import plotly.graph_objects as go
from math import radians, cos, sin, sqrt, atan2

# ==============================
# Page config
# ==============================
st.set_page_config(
    page_title="West Java Interactive Map",
    page_icon="🗺️",
    layout="centered"
)

st.title("🗺️ West Java City Connection Map")
st.markdown(
    "Select an origin and destination below, then click 'Generate Map' to highlight the connection."
)

# ==============================
# West Java city data
# ==============================
province_cities = {
    "Bandung": (-6.9175, 107.6191),
    "Bogor": (-6.5975, 106.8066),
    "Depok": (-6.4025, 106.7944),
    "Bekasi": (-6.234, 107.0057),
    "Cimahi": (-6.8996, 107.5422),
    "Sukabumi": (-6.9233, 106.9297),
    "Cirebon": (-6.732, 108.552)
}

cities = list(province_cities.keys())

# ==============================
# Distance calculation function
# ==============================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# ==============================
# Select origin & destination
# ==============================
col1, col2 = st.columns(2)
with col1:
    origin = st.selectbox("Select Origin City:", cities)
with col2:
    destination = st.selectbox("Select Destination City:", [c for c in cities if c != origin])

# ==============================
# Button to generate map
# ==============================
if st.button("Generate Map"):

    # Hitung jarak
    distance = haversine(province_cities[origin][0], province_cities[origin][1],
                         province_cities[destination][0], province_cities[destination][1])

    # ==============================
    # Generate map
    # ==============================
    lats = [province_cities[city][0] for city in cities]
    lons = [province_cities[city][1] for city in cities]

    edge_traces = []
    for i in range(len(cities)-1):
        for j in range(i+1, len(cities)):
            city1, city2 = cities[i], cities[j]
            color = "#9a0000" if (city1 == origin and city2 == destination) or (city1 == destination and city2 == origin) else "#000000"
            edge_traces.append(
                go.Scattermapbox(
                    lat=[province_cities[city1][0], province_cities[city2][0]],
                    lon=[province_cities[city1][1], province_cities[city2][1]],
                    mode='lines',
                    line=dict(width=2, color=color),
                    hoverinfo='text',
                    text=f"{city1} → {city2}: {haversine(province_cities[city1][0], province_cities[city1][1], province_cities[city2][0], province_cities[city2][1]):.2f} km",
                    showlegend=False
                )
            )

    # Marker kota
    node_trace = go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='markers+text',
        marker=go.scattermapbox.Marker(size=10, color="#ff80b3"),
        text=[f"📍 {city}" for city in cities],
        textposition="top right",
        hoverinfo='text',
        showlegend=False
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=7,
        mapbox_center={"lat": sum(lats)/len(lats), "lon": sum(lons)/len(lons)},
        margin={"l":0,"r":0,"t":0,"b":0},
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # Separate success message
    # ==============================
    st.markdown(f"""
        <div style="
            background-color: #ffe6f0;
            color: #cc0066;
            padding: 12px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 16px;">
            (/≧▽≦)/ Successfully generated a city connection map with {len(cities)} cities in West Java!
        </div>
    """, unsafe_allow_html=True)

    # ==============================
    # Add space between boxes
    # ==============================
    st.markdown("<br>", unsafe_allow_html=True)

    # ==============================
    # Separate distance box
    # ==============================
    st.markdown(f"""
        <div style="
            background-color: #ffe6f0;
            color: #9a0000;
            padding: 12px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            font-size: 16px;">
            Distance from {origin} to {destination} is {distance:.2f} km
        </div>
    """, unsafe_allow_html=True)
