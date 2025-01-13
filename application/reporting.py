import streamlit as st
import pandas as pd

from application.training import training_page

def app():
    st.title("Report from Excel")
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx", "xlsm"])

    if uploaded_file is not None:
        try:
            individual_shots = pd.read_excel(uploaded_file, sheet_name="Training Data")

            return training_page(individual_shots)

        except Exception as e:
            st.error(f"Error loading data: {e}")

