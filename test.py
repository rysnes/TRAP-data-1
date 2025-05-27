import altair as alt
import pandas as pd
import streamlit as st
from streamlit import dataframe


# Function to preprocess competition data
@st.cache_data
def preprocess_competition_data(file):
    data = pd.read_excel(file, sheet_name="Competition Data")
    data['Last Day of Competition'] = pd.to_datetime(data['Last Day of Competition'], errors='coerce')
    data['Qualifying Score'] = pd.to_numeric(data['Qualifying Score'], errors='coerce')
    data['Finals Score'] = pd.to_numeric(data['Finals Score'], errors='coerce')
    data['Place'] = pd.to_numeric(data['Place'], errors='coerce')
    data['Final Position'] = pd.to_numeric(data['Final Position'], errors='coerce')
    return data


# Function to preprocess training data
@st.cache_data
def preprocess_training_data(file):
    data = pd.read_excel(file, sheet_name="Training Data")
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    return data


# Function to preprocess athlete names
@st.cache_data
def preprocess_athlete_names(file):
    data = pd.read_excel(file, sheet_name="VIS Interest")
    return data


# Function to preprocess athlete data
@st.cache_data
def preprocess_athlete_data(file):
    data = pd.read_excel(file, sheet_name="Australian Athletes")
    data['Date Of Birth'] = pd.to_datetime(data['Date Of Birth'], errors='coerce')
    return data


uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx", "xlsm"])
athlete_names = preprocess_athlete_names(uploaded_file)
athlete_data = preprocess_athlete_data(uploaded_file)
training_data = preprocess_training_data(uploaded_file)
competition_data = preprocess_competition_data(uploaded_file)

athletes = athlete_names['Athlete Name'].dropna().drop_duplicates(keep='first')
athlete_selection_options = ["All Athletes Combined"] + list(athletes)
selected_athlete = st.sidebar.selectbox("Choose an Athlete", athlete_selection_options)


# Layout (3x2 Grid)
col1, col2 = st.columns(2)

with col1:
    st.header(f" {selected_athlete}")

with col2:
    st.write(f"**Date Of Birth:** {athlete_data['Date Of Birth'].values[0]}")
    st.write(f"**Category:** {athlete_data['Category'].values[0]}")

# Row 2: Competition Performance
col1, col2 = st.columns(2)

with col1:
    st.header("Competition Performance")
    st.metric("Last 3 Competitions", athlete_data["AvgScore_3"].values[0])
    st.metric("Last 12 Months", athlete_data["AvgScore_12"].values[0])
    st.metric("Last 24 Months", athlete_data["AvgScore_24"].values[0])

with col2:
    st.header("Recent Competition History")
    st.dataframe(athlete_data[["Event", "QualifyingScore", "FinalScore"]])

# Row 3: Training Performance
col1, col2 = st.columns(2)

with col1:
    st.header("Training Performance")
    st.bar_chart(athlete_data[["DoubleBarrel_Acc", "SingleBarrel_Acc"]])

with col2:
    st.header("Accuracy by Target Direction")
    st.line_chart(athlete_data[["TargetDirection", "Accuracy"]])
