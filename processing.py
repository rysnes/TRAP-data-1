import pandas as pd
import streamlit as st

# Function to preprocess competition data
@st.cache_data
def preprocess_competition_data(file):
    data = pd.read_excel(file, sheet_name="Competition Data")
    data['Last Day of Competition'] = pd.to_datetime(data['Last Day of Competition'], errors='coerce')
    data['Qualifying Score'] = pd.to_numeric(data['Qualifying Score'], errors='coerce')
    data['Qualifying Targets'] = pd.to_numeric(data['Qualifying Targets'], errors='coerce')
    data['Finals Score'] = pd.to_numeric(data['Finals Score'], errors='coerce')
    data['Finals Targets'] = pd.to_numeric(data['Finals Targets'], errors='coerce')
    data['Place'] = pd.to_numeric(data['Place'], errors='coerce')
    data['Final Position'] = pd.to_numeric(data['Final Position'], errors='coerce')
    return data


# Function to preprocess training data
@st.cache_data
def preprocess_training_data(file):
    data = pd.read_excel(file, sheet_name="Training Data")
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Shot Timing'] = pd.to_numeric(data['Shot Timing'], errors='coerce')

    return data


# Function to preprocess athlete names
@st.cache_data
def preprocess_athlete_names(file):
    data = pd.read_excel(file, sheet_name="VIS Interest")
    return data

