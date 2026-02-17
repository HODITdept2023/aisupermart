import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# ----------------------------
# LOGIN SYSTEM
# ----------------------------

def login():
    st.title("🔐 AI MART Admin Login")

    username = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "aimart2026":
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid Credentials")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()

# ----------------------------
# DASHBOARD
# ----------------------------

st.title("🛒 AI MART Sales Dashboard")

year = st.number_input("Enter Year", min_value=2000, max_value=2100, step=1)

months = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]

st.subheader("📊 Enter Monthly Data")

sales = []
stock = []
profit = []
expenses = []
customers = []
discount = []

for m in months:
    st.markdown(f"### {m}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sales.append(st.number_input(f"{m} Sales", key=f"s_{m}"))
        stock.append(st.number_input(f"{m} Stock", key=f"st_{m}"))
        
    with col2:
        profit.append(st.number_input(f"{m} Profit", key=f"p_{m}"))
        expenses.append(st.number_input(f"{m} Expenses", key=f"e_{m}"))
        
    with col3:
        customers.append(st.number_input(f"{m} Customers", key=f"c_{m}"))
        discount.append(st.number_input(f"{m} Discount %", key=f"d_{m}"))

# ----------------------------
# ANALYZE BUTTON
# ----------------------------

if st.button("📈 Analyze & Predict"):

    data = pd.DataFrame({
        "Month": months,
        "Sales": sales,
        "Stock": stock,
        "Profit": profit,
        "Expenses": expenses,
        "Customers": customers,
        "Discount_%": discount
    })

    st.subheader("📋 Dataset")
    st.dataframe(data)

    total_sales = sum(sales)
    total_profit = sum(profit)
    total_expenses = sum(expenses)

    best_month = months[sales.index(max(sales))]
    worst_month = months[sales.index(min(sales))]

    st.subheader("📊 Yearly Summary")
    st.write("Total Sales:", total_sales)
    st.write("Total Profit:", total_profit)
    st.write("Total Expenses:", total_expenses)
    st.write("Best Month:", best_month)
    st.write("Worst Month:", worst_month)

    # Prediction
    X = np.array(range(1,13)).reshape(-1,1)
    y = np.array(sales)

    model = LinearRegression()
    model.fit(X,y)

    next_month = model.predict([[13]])[0]
    future = model.predict(np.array(range(13,25)).reshape(-1,1))

    st.subheader("🔮 Predictions")
    st.write("Predicted Next Month Sales:", round(next_month,2))
    st.write("Predicted Next Year Sales:", round(sum(future),2))

    # Graphs
    st.subheader("📈 Sales Trend")
    fig1 = plt.figure()
    plt.plot(months, sales)
    st.pyplot(fig1)

    st.subheader("💰 Profit vs Expenses")
    fig2 = plt.figure()
    plt.plot(months, profit)
    plt.plot(months, expenses)
    st.pyplot(fig2)

    st.subheader("📊 Forecast")
    fig3 = plt.figure()
    plt.plot(range(1,13), sales)
    plt.plot(range(13,25), future, linestyle="dashed")
    st.pyplot(fig3)

    # Insights
    st.subheader("💡 Business Insights")

    if total_profit < total_expenses:
        st.warning("Expenses are higher than profit.")
    if np.mean(discount) > 20:
        st.info("High discount strategy detected.")
    if np.mean(customers) < 400:
        st.warning("Low customer engagement.")
