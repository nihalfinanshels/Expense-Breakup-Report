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

    # Clean the data (ensure columns are in correct format)
    # In this case, the columns are already months, so no date conversion is needed.
    
    # Fill missing values with 0 (if needed, you can modify this logic)
    df = df.fillna(0)

    # Organize the data into a pivot-like structure (if needed, adjust aggregation)
    # We will ensure the months stay as columns and Account + Contact as rows

    # Display the breakdown in the requested format
    breakdown_df = df.set_index(['Account', 'Contact'])

    st.subheader("Expense Breakdown by Contact and Month")
    st.write(breakdown_df)

    # Option to download the breakdown as Excel
    output = pd.ExcelWriter("expense_breakdown_pivot_format.xlsx", engine='xlsxwriter')
    breakdown_df.to_excel(output, sheet_name="Breakdown", index=True)
    output.save()

    # Button to download the breakdown
    with open("expense_breakdown_pivot_format.xlsx", "rb") as file:
        st.download_button("📥 Download Breakdown", file, file_name="expense_breakdown_pivot_format.xlsx")
