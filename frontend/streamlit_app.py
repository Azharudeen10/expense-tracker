import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://localhost:5000"

st.title("💸 Expense Tracker")

with st.form("expense_form"):
    amount_str = st.text_input("Amount")  # blank input
    category = st.selectbox("Category", ["Food","Transport","Entertainment","Household","Dress","Health","Others"])
    date = st.date_input("Date")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if not amount_str or not category or not date:
            st.error("All fields required.")
        else:
            try:
                amount = int(amount_str)
                if amount < 0:
                    st.error("Amount cannot be negative.")
                else:
                    data = {"amount": amount, "category": category, "date": str(date)}
                    res = requests.post(f"{API_URL}/add_expense", json=data)
                    if res.status_code == 200:
                        st.success("Expense added successfully!")
                    else:
                        st.error("Failed to add expense.")
            except ValueError:
                st.error("Amount must be a valid number.")


st.header("📊 Expense Summary")

response = requests.get(f"{API_URL}/summary")
if response.status_code == 200:
    summary_data = response.json()
    if summary_data:
        df_summary = pd.DataFrame(summary_data)
        df_summary['amount'] = pd.to_numeric(df_summary['amount'])
        fig = px.pie(df_summary, values='amount', names='category', title='Spending by Category', hole=0.4)
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig)
        st.dataframe(df_summary)
    else:
        st.write("No expenses found.")
        
else:
    st.error("Failed to fetch expense summary.")