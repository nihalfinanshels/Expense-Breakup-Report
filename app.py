import streamlit as st
import pandas as pd

st.title("📊 Expense Breakdown by Account, Contact, and Month")

# Upload the file
uploaded_file = st.file_uploader("Upload your Expense Excel file", type=["xlsx"])

if uploaded_file:
    # Read the file
    df = pd.read_excel(uploaded_file)
    
    # Display raw data
    st.subheader("Original Data")
    st.write(df)

    # Extract unique months from the column names (excluding 'Account' and 'Contact')
    months = df.columns[2:]  # Skip 'Account' and 'Contact' columns
    expense_accounts = df['Account'].unique()

    # Initialize an empty list to store the formatted rows for the output
    formatted_rows = []

    # Loop through each expense account and its corresponding contacts
    for account in expense_accounts:
        account_data = df[df['Account'] == account]

        for contact in account_data['Contact'].unique():
            # Filter data for the specific account and contact
            contact_data = account_data[account_data['Contact'] == contact]
            
            # Calculate the sum of expenses for each month for the current contact
            monthly_expenses = [contact_data[month].sum() if month in contact_data.columns else 0 for month in months]

            # Add the account name, contact name, and monthly sums to the formatted rows list
            formatted_rows.append([account, contact] + monthly_expenses)
    
    # Create a new DataFrame from the formatted rows
    formatted_df = pd.DataFrame(formatted_rows, columns=["Expense Account", "Contact"] + list(months))

    # Display the final formatted table
    st.subheader("Formatted Expense Breakdown")
    st.write(formatted_df)

    # Option to download the formatted table as Excel
    output_file = "formatted_expense_breakdown.xlsx"
    
    # Save the DataFrame to an Excel file using the openpyxl engine
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        formatted_df.to_excel(writer, sheet_name="Breakdown", index=False)

    # Button to download the formatted table
    with open(output_file, "rb") as file:
        st.download_button("📥 Download Breakdown", file, file_name="formatted_expense_breakdown.xlsx")
