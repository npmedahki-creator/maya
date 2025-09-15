import streamlit as st
import pandas as pd
from datetime import datetime
import openpyxl

FILE_PATH = "insurance1_data.xlsx"

# --- Title ---
st.title("Almedahki Broker Insurance")

# --- Sidebar Input Form ---
st.sidebar.header("Daily Report")

date = st.sidebar.date_input("Date", datetime.today().date())
company = st.sidebar.selectbox("Insurance Company", 
                               ["General Takaful", "Doha Islamic", "Misr Insurance", "Doha Commission"])
branch = st.sidebar.selectbox("Branch", ["Madinat Khalifa", "Sanaiya", "Misamir"])
amtbranch = st.sidebar.number_input(f"{branch} Amount", min_value=0.0, step=0.01)
amthealth = st.sidebar.number_input("Health Insurance", min_value=0.0, step=0.01)
amtextend = st.sidebar.number_input("Extend/Other", min_value=0.0, step=0.01)
amtheadoff = st.sidebar.number_input("From H.O.", min_value=0.0, step=0.01)
amtcancel = st.sidebar.number_input("Cancel Policy", min_value=0.0, step=0.01)

if st.sidebar.button("Submit"):
    total_amount = amtbranch + amthealth + amtextend + amtheadoff - amtcancel

    # नयाँ डेटा तयार
    new_data = {
        "Date": [date],
        "Madinat Khalifa": [amtbranch if branch == "Madinat Khalifa" else 0],
        "Sanaiya": [amtbranch if branch == "Sanaiya" else 0],
        "Misamir": [amtbranch if branch == "Misamir" else 0],
        "Health": [amthealth],
        "Extend": [amtextend],
        "Head Office": [amtheadoff],
        "Cancel": [amtcancel],
        "Total": [total_amount]
    }
    df_new = pd.DataFrame(new_data)

    try:
        # पुरानो डेटा पढ्ने (कम्पनीको sheet बाट)
        df_old = pd.read_excel(FILE_PATH, sheet_name=company)
        df = pd.concat([df_old, df_new], ignore_index=True)
    except FileNotFoundError:
        df = df_new

    # Excel मा लेख्ने
    with pd.ExcelWriter(FILE_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=company, index=False)

    st.sidebar.success(f"✅ Data Saved Successfully to {company} sheet!")

# --- Display Data ---
st.subheader("📅 Daily Records")
try:
    df = pd.read_excel(FILE_PATH, sheet_name=company)
    st.dataframe(df)

    # Summary
    st.subheader(f"📌 Summary for {company}")
    summary = df.groupby("Date")["Total"].sum().reset_index()
    st.table(summary)

    st.subheader("💰 Total Collection")
    st.success(f"QAR {df['Total'].sum():,.2f}")

except FileNotFoundError:
    st.info("No records found yet. Please add some entries.")




