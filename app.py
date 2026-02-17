import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

# -----------------------------
# CUSTOM CSS (Admin Style)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
.sidebar .sidebar-content {
    background-color: #111827;
}
.kpi-card {
    padding: 20px;
    border-radius: 10px;
    color: white;
}
.blue { background-color: #3b82f6; }
.green { background-color: #10b981; }
.orange { background-color: #f59e0b; }
.red { background-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGIN
# -----------------------------
def login():
    st.title("🔐 Admin Login")
    user = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pwd == "aimart2026":
            st.session_state.auth = True
        else:
            st.error("Invalid Credentials")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    login()
    st.stop()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("AI MART")
st.sidebar.markdown("### Navigation")
menu = st.sidebar.radio("", ["Dashboard", "Sales Entry"])

# -----------------------------
# DASHBOARD
# -----------------------------
if menu == "Dashboard":

    st.title("📊 Dashboard Overview")

    # Sample KPI Data
    total_orders = 150
    bounce_rate = 53
    registrations = 44
    visitors = 65

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="kpi-card blue"><h2>{total_orders}</h2><p>New Orders</p></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="kpi-card green"><h2>{bounce_rate}%</h2><p>Bounce Rate</p></div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="kpi-card orange"><h2>{registrations}</h2><p>User Registrations</p></div>', unsafe_allow_html=True)

    with col4:
        st.markdown(f'<div class="kpi-card red"><h2>{visitors}</h2><p>Unique Visitors</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Sales Graph
    months = ["Jan","Feb","Mar","Apr","May","Jun"]
    sales1 = [30, 45, 40, 25, 80, 35]
    sales2 = [60, 55, 75, 78, 52, 48]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=sales1, mode='lines', name='2023'))
    fig.add_trace(go.Scatter(x=months, y=sales2, mode='lines', name='2024'))

    fig.update_layout(title="Sales Value",
                      template="plotly_white",
                      height=400)

    left, right = st.columns([2,1])

    with left:
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("### Sales Summary")
        st.write("Visitors: 1,230")
        st.write("Online: 842")
        st.write("Sales: 523")

# -----------------------------
# SALES ENTRY PAGE
# -----------------------------
if menu == "Sales Entry":

    st.title("📈 Sales Input & Prediction")

    year = st.number_input("Enter Year", min_value=2000, max_value=2100)

    months = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]

    sales = []

    st.markdown("### Enter Monthly Sales")

    cols = st.columns(4)

    for i, m in enumerate(months):
        with cols[i % 4]:
            sales.append(st.number_input(m, key=m))

    if st.button("Analyze"):

        total_sales = sum(sales)
        best_month = months[sales.index(max(sales))]

        st.markdown("### Results")
        st.write("Total Sales:", total_sales)
        st.write("Best Month:", best_month)

        # Prediction
        X = np.array(range(1,13)).reshape(-1,1)
        model = LinearRegression()
        model.fit(X, np.array(sales))

        future = model.predict(np.array(range(13,25)).reshape(-1,1))

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
    x=list(range(1,13)),
    y=sales,
    name="Actual",
    mode="lines+markers"
))

fig2.add_trace(go.Scatter(
    x=list(range(13,25)),
    y=list(future),
    name="Predicted",
    mode="lines+markers"
))

        st.plotly_chart(fig2, use_container_width=True)
