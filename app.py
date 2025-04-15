import streamlit as st
import pandas as pd

st.title("📊 Expense Breakdown by Contact and Month")

# Upload the file
uploaded_file = st.file_uploader("Upload your Expense Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Display raw data
    st.subheader("Original Data")
    st.write(df)

    # Clean the data (ensure 'Date' is in datetime format)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert Date to datetime

    # Extract Month from the 'Date' column
    df['Month'] = df['Date'].dt.to_period('M')  # Get month-year period (e.g., 'Dec-2024')

    # Pivot the data: Expenses (rows), Contacts (columns), Values (Gross USD)
    pivot_df = df.pivot_table(
        index=['Account'], 
        columns=['Contact', 'Month'], 
        values='Gross (USD)', 
        aggfunc='sum', 
        fill_value=0
    )

    # Display the pivot table (Expense types vs Contacts with the respective monthly values)
    st.subheader("Expense Breakdown by Contact and Month")
    st.write(pivot_df)

    # Option to download the pivot table as Excel
    output = pd.ExcelWriter("expense_breakdown_pivot.xlsx", engine='xlsxwriter')
    pivot_df.to_excel(output, sheet_name="Breakdown", index=True)
    output.save()

    # Button to download the breakdown
    with open("expense_breakdown_pivot.xlsx", "rb") as file:
        st.download_button("📥 Download Breakdown", file, file_name="expense_breakdown_pivot.xlsx")
