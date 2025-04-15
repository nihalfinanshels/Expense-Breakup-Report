import streamlit as st
import pandas as pd

st.title("📊 Expense Breakdown by Contact and Month")

# Upload the file
uploaded_file = st.file_uploader("Upload your Expense Excel file", type=["xlsx"])

if uploaded_file:
    # Read the file
    df = pd.read_excel(uploaded_file)
    
    # Display raw data
    st.subheader("Original Data")
    st.write(df)

    # Clean the data: Replace NaN values with 0 and ensure columns have appropriate types
    df = df.fillna(0)  # Replace NaN values with 0
    
    # Ensure numeric columns are properly cast to numeric types (where applicable)
    df['Apr-2025'] = pd.to_numeric(df['Apr-2025'], errors='coerce').fillna(0)
    df['Mar-2025'] = pd.to_numeric(df['Mar-2025'], errors='coerce').fillna(0)
    df['Feb-2025'] = pd.to_numeric(df['Feb-2025'], errors='coerce').fillna(0)
    df['Jan-2025'] = pd.to_numeric(df['Jan-2025'], errors='coerce').fillna(0)
    df['Dec-2024'] = pd.to_numeric(df['Dec-2024'], errors='coerce').fillna(0)

    # Organize the data into a pivot-like structure (if needed, adjust aggregation)
    breakdown_df = df.set_index(['Account', 'Contact'])

    # Display the cleaned breakdown
    st.subheader("Expense Breakdown by Contact and Month")
    st.write(breakdown_df)

    # Option to download the breakdown as Excel
    output = pd.ExcelWriter("expense_breakdown_pivot_format.xlsx", engine='xlsxwriter')
    breakdown_df.to_excel(output, sheet_name="Breakdown", index=True)
    output.save()

    # Button to download the breakdown
    with open("expense_breakdown_pivot_format.xlsx", "rb") as file:
        st.download_button("📥 Download Breakdown", file, file_name="expense_breakdown_pivot_format.xlsx")
