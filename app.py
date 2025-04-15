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

    # Extract unique months from the "Monthly" column
    months = df['Monthly'].unique()

    # Initialize a new DataFrame to construct the desired output
    expense_accounts = df['Account'].unique()
    
    # Create an empty DataFrame for the output structure
    output_df = pd.DataFrame(columns=["Expense Account"] + list(months))
    
    # Fill in the "Expense Account" column with the unique account names
    output_df['Expense Account'] = list(expense_accounts) * len(df['Contact'].unique())

    # Loop through each account and its corresponding contact
    for idx, account in enumerate(expense_accounts):
        # Extract the rows corresponding to each account
        account_data = df[df['Account'] == account]
        
        for contact in account_data['Contact'].unique():
            # Filter data for the specific account and contact
            contact_data = account_data[account_data['Contact'] == contact]
            
            # Extract the expenses for each month
            expenses = contact_data.groupby('Monthly')['Gross (USD)'].sum()
            
            # Add the contact name in the second column (Contact)
            contact_expenses = [contact] + [expenses.get(month, 0) for month in months]
            
            # Append the contact data to the output DataFrame
            output_df.loc[len(output_df)] = contact_expenses
    
    # Replace NaN values with 0 or empty string for all columns
    output_df = output_df.fillna(0)  # or fillna("") if you prefer empty strings

    # Display the final table
    st.subheader("Formatted Expense Breakdown")
    st.write(output_df)

    # Option to download the formatted table as Excel
    output_file = "formatted_expense_breakdown.xlsx"
    
    # Save the DataFrame to an Excel file using the openpyxl engine
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        output_df.to_excel(writer, sheet_name="Breakdown", index=False)

    # Button to download the formatted table
    with open(output_file, "rb") as file:
        st.download_button("📥 Download Breakdown", file, file_name="formatted_expense_breakdown.xlsx")
