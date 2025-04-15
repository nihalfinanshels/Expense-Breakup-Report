import streamlit as st
import pandas as pd

st.title("📊 Expense Breakdown by Contact and Period")

# Upload the file
uploaded_file = st.file_uploader("Upload your Expense Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Display raw data
    st.subheader("Original Data")
    st.write(df)

    # Clean the data (if necessary)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Ensure 'Date' is a datetime object

    # Organizing data by Contact and Period (Weekly/Monthly)
    # Aggregating by Contact and Period to generate the breakdown
    breakdown = df.groupby(['Contact', 'Weekly', 'Monthly']).agg({
        'Account': 'first',  # Assuming each expense type is unique per Contact and Period
        'Gross (USD)': 'sum',  # Summing Gross (USD) per contact and period
        'FACTOR': 'mean',  # Averaging the FACTOR (if needed, you can sum or perform other operations)
    }).reset_index()

    # Display the summary table
    st.subheader("Expense Breakdown")
    st.write(breakdown)

    # Option to download the breakdown as Excel
    output = pd.ExcelWriter("expense_breakdown.xlsx", engine='xlsxwriter')
    breakdown.to_excel(output, sheet_name="Breakdown", index=False)
    output.save()

    # Button to download the breakdown
    with open("expense_breakdown.xlsx", "rb") as file:
        st.download_button("📥 Download Breakdown", file, file_name="expense_breakdown.xlsx")
