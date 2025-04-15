import streamlit as st
import pandas as pd

st.title("📊 Expense Guide Breakdown")

# Upload file
uploaded_file = st.file_uploader("Upload your Expense Excel file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Make sure date column is datetime type
    df['Date'] = pd.to_datetime(df['Date'])

    # Add month and week columns
    df['Month'] = df['Date'].dt.to_period('M')
    df['Week'] = df['Date'].dt.to_period('W')

    st.subheader("Original Data")
    st.write(df)

    # Monthly Summary
    monthly_summary = df.groupby('Month')["Gross (USD)"].sum().reset_index()
    monthly_summary.columns = ["Month", "Total Gross (USD)"]

    st.subheader("📅 Monthly Summary")
    st.write(monthly_summary)

    # Weekly Summary
    weekly_summary = df.groupby('Week')["Gross (USD)"].sum().reset_index()
    weekly_summary.columns = ["Week", "Total Gross (USD)"]

    st.subheader("🗓️ Weekly Summary")
    st.write(weekly_summary)

    # Download outputs
    output = pd.ExcelWriter("expense_breakdown.xlsx", engine='xlsxwriter')
    df.to_excel(output, sheet_name="Original", index=False)
    monthly_summary.to_excel(output, sheet_name="Monthly Summary", index=False)
    weekly_summary.to_excel(output, sheet_name="Weekly Summary", index=False)
    output.save()

    with open("expense_breakdown.xlsx", "rb") as file:
        st.download_button("📥 Download Breakdown", file, file_name="expense_breakdown.xlsx")
