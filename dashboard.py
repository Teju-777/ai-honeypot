
import streamlit as st
import pandas as pd
import json, os
import gspread
from google.oauth2 import service_account
import matplotlib.pyplot as plt
import pydeck as pdk

st.set_page_config(page_title="Honeypot Dashboard", layout="wide")

# Load Google Service Account credentials from environment
creds_dict = json.loads(os.environ["GOOGLE_CREDS"])
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)

client = gspread.authorize(creds)

# Replace with your actual Google Sheet URL
sheet_url = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID_HERE/edit#gid=0"
sheet = client.open_by_url(sheet_url).sheet1

# Load data into DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.dropna(subset=['timestamp'])

st.title("🛡️ AI-Powered Honeypot Dashboard")

# ---- Attacks Per Day ----
st.subheader("🚨 Attacks Per Day")
attacks_per_day = df['timestamp'].dt.date.value_counts().sort_index()
fig1, ax1 = plt.subplots()
attacks_per_day.plot(kind='bar', ax=ax1, color='salmon')
ax1.set_xlabel("Date")
ax1.set_ylabel("Number of Attacks")
st.pyplot(fig1)

# ---- Top Attacker IPs ----
st.subheader("🌍 Top 10 Attacker IPs")
top_ips = df['ip'].value_counts().head(10)
st.bar_chart(top_ips)

# ---- Common Usernames & Passwords ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Most Used Usernames")
    st.write(df['username'].value_counts().head(5))

with col2:
    st.subheader("🔐 Most Used Passwords")
    st.write(df['password'].value_counts().head(5))

# ---- Optional Geo Map (if lat/lon columns are available) ----
if 'lat' in df.columns and 'lon' in df.columns:
    st.subheader("📍 Attack Map (by IP location)")
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=df['lat'].mean(),
            longitude=df['lon'].mean(),
            zoom=3,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df.dropna(subset=['lat', 'lon']),
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=20000,
            ),
        ],
    ))
else:
    st.info("🗺️ Add 'lat' and 'lon' columns to enable geographic visualization.")
