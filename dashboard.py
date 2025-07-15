import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Load data
sheet = client.open("Honeypot Logs").sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Preprocess
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

# UI
st.title("🛡️ AI Honeypot Dashboard")

st.metric("Total Attempts", len(df))
st.metric("Unique IPs", df["ip"].nunique())

# Line Chart: Attempts over Time
st.subheader("📆 Attacks Per Day")
daily = df.groupby("date").size()
st.line_chart(daily)

# Top IPs
st.subheader("🌐 Top Attacker IPs")
st.bar_chart(df["ip"].value_counts().head(10))

# Common Usernames
st.subheader("🧑‍💻 Common Usernames Tried")
st.bar_chart(df["username"].value_counts().head(10))

# Raw Logs
st.subheader("📝 Full Log")
st.dataframe(df.tail(10))
