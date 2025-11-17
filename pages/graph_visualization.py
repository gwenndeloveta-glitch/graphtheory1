import streamlit as st
import networkx as nx
import plotly.graph_objects as go

st.set_page_config(page_title="Graph Visualization", page_icon="(∩^o^)⊃━☆", layout="centered")

st.title("(∩^o^)⊃━☆ Graph Visualization")

# Input jumlah node & edges
num_nodes = st.number_input("Enter the number of nodes:", min_value=1, value=5, step=1)
num_edges = st.number_input("Enter the number of edges:", min_value=0, value=4, step=1)

# Tombol untuk generate graph
if st.button("Generate Graph"):
    # Buat graph acak
    G = nx.gnm_random_graph(num_nodes, num_edges)

    # Posisi node untuk visualisasi
    pos = nx.spring_layout(G, seed=42)

    # Dapatkan koordinat node dan edge
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    # Gambar edge
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color="#000000"),
        hoverinfo="none",
        mode="lines"
    )

    # Node data
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        hoverinfo="text",
        text=[str(i) for i in G.nodes()],
        textposition="top center",
        marker=dict(
            showscale=True,
            colorscale=[ [0, "#ffffff"], [1, "#ffc7de"] ],
            color=[G.degree(n) for n in G.nodes()],
            size=20,
            colorbar=dict(
                thickness=10,
                title=dict(text="Node Degree", side="right"),
                xanchor="left"
            ),
            line_width=2
        )
    )

    # Hover info tiap node
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_text.append(f"Node {node}: Degree {len(adjacencies[1])}")
    node_trace.text = node_text

    # Layout plotly
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode="closest",
            margin=dict(b=0, l=0, r=0, t=30),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
    f"""
    <div style="
        background-color: #ffe6f0;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        color: #cc0066;
        font-weight: bold;
        font-size: 16px;">
        (/≧▽≦)/ Graph with {num_nodes} nodes and {num_edges} edges generated successfully!
    </div>
    """,
    unsafe_allow_html=True
)