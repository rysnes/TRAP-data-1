import altair as alt
import pandas as pd
import streamlit as st
from streamlit import dataframe
from processing import preprocess_competition_data, preprocess_training_data, preprocess_athlete_names
from charts import DB_accuracy, generate_training_report, generate_competition_report

#Page config
st.set_page_config(layout="wide")

st.markdown(
            """
            <style>
                .stColumn {
                    border-left: 1px solid #eab464ff;
                    padding-left: 6px;
                    margin-left: -6px;
                    border-top: 1px solid #eab464ff;
                }
                
                @media (max-width: 20px) { /* Change this value to control when columns stack */
                    .st-emotion-cache-1y4p8pa { /* Streamlit's column container class */
                        flex-direction: column !important;
                    }
                }
            </style>
            """,
            unsafe_allow_html=True
        )

#Title and Upload
st.subheader("Shotgun Data Analysis")
uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx", "xlsm"])


if uploaded_file:
    #Prepare data
    athlete_names = preprocess_athlete_names(uploaded_file)
    competition_data = preprocess_competition_data(uploaded_file)
    training_data = preprocess_training_data(uploaded_file)
    athletes = athlete_names['Athlete Name'].dropna().drop_duplicates(keep='first')

    # Sidebar selection for athlete
    athlete_selection_options = ["All Athletes Combined"] + list(athletes)
    selected_athlete = st.sidebar.selectbox("Choose an Athlete", athlete_selection_options)

    if selected_athlete == "All Athletes Combined":
        # discipline_options = list(competition_data['Discipline'].dropna().drop_duplicates(keep='first'))
        discipline_options = list(['Trap Men', 'Trap Women'])
        selected_discipline = st.sidebar.selectbox(
            'When "All Athletes Combined" is selected, please also choose a discipline to filter competition benchmarks',
            discipline_options)
    else: selected_discipline = 0

    #Page start
    st.title(f'{selected_athlete}')
    # st.write("Age: xx")
    # st.write("Categorisation: xxxxxxxxxxxxxxxxxxxxxx")
    st.divider()
    st.header('Competition Performance')
    st.write("Results from competitions with 125 targets in qualifying")
    generate_competition_report(competition_data, selected_athlete, "info", selected_discipline)

    #Build Column Layout
    left_col, right_col = st.columns([1, 2])  # 33%:67% ratio (1+2=3 total parts)

    with left_col:
        generate_competition_report(competition_data, selected_athlete, "avg_performance", selected_discipline)


    with right_col:

        generate_competition_report(competition_data, selected_athlete, "recent_results", selected_discipline)


    # Training page section

    st.divider()
    st.header("Training Performance")

    # Get unique dates and athletes from the training data
    date_list = pd.to_datetime(training_data['Date'].dropna().drop_duplicates(keep='first'))

    # Selection for date and athlete
    date_selection_options = ["All Dates Combined"] + list(date_list)
    selected_date = st.selectbox(
        "Choose a Training Date",
        date_selection_options,
        format_func=lambda x: x.strftime('%d-%m-%Y') if isinstance(x, pd.Timestamp) else x
    )

    generate_training_report(training_data, selected_athlete, selected_date, "session_info")

    #Build columns

    left_col, right_col = st.columns([1, 2])  # 33%:67% ratio (1+2=3 total parts)

    with left_col:
        generate_training_report(training_data, selected_athlete, selected_date, "barrel_accuracy")
        generate_training_report(training_data, selected_athlete, selected_date, "shot_timing")

    with right_col:

        # Build columns
        #sub_left_col, sub_right_col = st.columns([1, 1])  # 33%:67% ratio (1+2=3 total parts)
        #with sub_left_col:
        #    generate_training_report(training_data, selected_athlete, selected_date, "station")
        #with sub_right_col:
        #            generate_training_report(training_data, selected_athlete, selected_date, "direction")

        generate_training_report(training_data, selected_athlete, selected_date, "station_and_direction")
        generate_training_report(training_data, selected_athlete, selected_date, "trajectory")


else:
    st.info("Please upload an Excel file to proceed.")


