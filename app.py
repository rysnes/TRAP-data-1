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


# Function to generate training report
def generate_training_report(data, selected_date):
    if selected_date == "All Dates Combined":
        filtered_data = data  # Use all data
    else:
        filtered_data = data[data['Date'] == selected_date]

    # Split data into double barrel and single barrel
    double_barrel = filtered_data[filtered_data['SB'].isna()]
    single_barrel = filtered_data[filtered_data['SB'] == 'SB']

    # Double barrel accuracy
    first_barrel_hits = len(double_barrel[double_barrel['Hit'] == 1])
    second_barrel_hits = len(double_barrel[double_barrel['Hit'] == 2])
    total_double_barrel_shots = len(double_barrel)
    missed_first_barrel = total_double_barrel_shots - first_barrel_hits
    missed_second_barrel = total_double_barrel_shots - (first_barrel_hits + second_barrel_hits)
    first_barrel_accuracy = first_barrel_hits / total_double_barrel_shots if total_double_barrel_shots > 0 else 0
    second_barrel_accuracy = second_barrel_hits / missed_first_barrel if missed_first_barrel > 0 else 0
    double_barrel_accuracy = (first_barrel_hits + second_barrel_hits) / total_double_barrel_shots

    #Double barrel accuracy chart information
    DB_hit_data = {'Hits': [first_barrel_hits, second_barrel_hits],
                   'Misses': [missed_first_barrel, missed_second_barrel]}
    DB_chart_data = pd.DataFrame(data=DB_hit_data, index=['First Barrel', 'Second Barrel'])


    def DB_hit_by_station (station):
        DB_station = double_barrel[double_barrel['Station_no'] == station]
        DB_first_barrel_hits_by_station = len(DB_station [DB_station ['Hit'] == 1])
        DB_second_barrel_hits_by_station = len(DB_station [DB_station ['Hit'] == 2])
        DB_misses_by_station = len(DB_station [DB_station ['Hit'] == 0])

        data = {'Hit on First': DB_first_barrel_hits_by_station,
                'Hit on Second': DB_second_barrel_hits_by_station,
                'Miss': DB_misses_by_station}

        return data

    def DB_hit_by_direction (direction):
        Drills = double_barrel[
            (double_barrel['Drill'] == "25 Targets scored")
            ]
        total_count = len(Drills [Drills ['Drill'] == "25 Targets scored"])

        DB_Direction_Data = Drills[
            (Drills['Direction'] == direction)
            ]
        DB_second_barrel_hits_by_direction = len(DB_Direction_Data [DB_Direction_Data ['Hit'] == 2])
        DB_misses_by_direction = len(DB_Direction_Data [DB_Direction_Data ['Hit'] == 0])

        if direction == "L":
            DB_first_barrel_hits_by_direction = (10*total_count/25) - (DB_second_barrel_hits_by_direction + DB_misses_by_direction)

        elif direction == "R":
            DB_first_barrel_hits_by_direction = (10*total_count/25) - (DB_second_barrel_hits_by_direction + DB_misses_by_direction)

        elif direction == "S":
            DB_first_barrel_hits_by_direction = (5*total_count/25) - (DB_second_barrel_hits_by_direction + DB_misses_by_direction)

        data = {'Hit on First': DB_first_barrel_hits_by_direction,
                'Hit on Second': DB_second_barrel_hits_by_direction,
                'Miss': DB_misses_by_direction}

        return data

    DB_all_station_hits = pd.DataFrame(data=[DB_hit_by_station(1), DB_hit_by_station(2), DB_hit_by_station(3), DB_hit_by_station(4), DB_hit_by_station(5)], index=['Station 1', 'Station 2', 'Station 3', 'Station 4', 'Station 5'])
    DB_all_direction_hits = pd.DataFrame(data=[DB_hit_by_direction("L"), DB_hit_by_direction("S"), DB_hit_by_direction("R")], index=['Left', 'Straight', 'Right'])

    DB_all_station_hits_reset = DB_all_station_hits.reset_index().melt(id_vars=["index"], var_name="Hit Type", value_name="Count")
    DB_all_station_hits_reset = DB_all_station_hits_reset.rename(columns={"index": "Station"})
    DB_all_station_hits_reset_order = ["Hit on First", "Hit on Second", "Miss"]

    DB_all_station_hits_altair_chart = (
        alt.Chart(DB_all_station_hits_reset)
        .mark_bar()
        .encode(
            x=alt.X("Station:N", title=None),
            y=alt.Y("Count:Q", title=None, stack="zero"),  # Ensures stacking
            color=alt.Color(
                "Hit Type:N",
                scale=alt.Scale(domain=DB_all_station_hits_reset_order, range=["#eab464ff", "#a17e4aff", "#dcccbbff"]),
                legend=alt.Legend(title=None, orient="bottom")  # Moves legend to the bottom
            ),
            order=alt.Order("Hit Type", sort="ascending")
            # Custom order and colors
        )
    )
    DB_all_direction_hits_reset = DB_all_direction_hits.reset_index().melt(id_vars=["index"], var_name="Hit Type", value_name="Count")
    DB_all_direction_hits_reset = DB_all_direction_hits_reset.rename(columns={"index": "Direction"})
    DB_all_direction_hits_reset_order = ["Hit on First", "Hit on Second", "Miss"]

    DB_all_direction_hits_altair_chart = (
        alt.Chart(DB_all_direction_hits_reset)
        .mark_bar()
        .encode(
            x=alt.X("Direction:N", title=None, sort=["L", "S", "R"]),
            y=alt.Y("Count:Q", title=None, stack="zero"),  # Ensures stacking
            color=alt.Color(
                "Hit Type:N",
                scale=alt.Scale(domain=DB_all_direction_hits_reset_order, range=["#eab464ff", "#a17e4aff", "#dcccbbff"]),
                legend=alt.Legend(title=None, orient="bottom")  # Moves legend to the bottom
            ),
            order=alt.Order("Hit Type", sort="ascending")
            # Custom order and colors
        )
    )



    # Single barrel accuracy
    sb_hits = len(single_barrel[single_barrel['Hit'] == 1])
    total_sb_shots = len(single_barrel)
    sb_misses = total_sb_shots - sb_hits
    sb_accuracy = sb_hits / total_sb_shots if total_sb_shots > 0 else 0

    SB_hit_data = {'Hits': [sb_hits],
                   'Misses': [sb_misses]}
    SB_chart_data = pd.DataFrame(data=SB_hit_data, index=['First Barrel'])

    # Generate charts
    st.divider()
    st.header(selected_athlete + ", on " + str(selected_date))

    st.subheader("Double Barrel Accuracy - by barrel")
    st.write("The hit rate for all targets combined was " + str(round(100 * double_barrel_accuracy, 1)) + "%")
    st.bar_chart(
        DB_chart_data,
        color=["#eab464ff", "#dcccbbff"],
        horizontal="true"
    )


    st.subheader("Single Barrel Accuracy")
    st.write(selected_athlete + " hit " + str(round(100 * sb_accuracy, 1)) + "% of Targets.")
    st.bar_chart(
        SB_chart_data,
        color=["#eab464ff", "#dcccbbff"],
        horizontal="true"
    )

    st.divider()

    st.subheader("Double Barrel Accuracy - by station")

    st.altair_chart(DB_all_station_hits_altair_chart, use_container_width=True)

    st.subheader("Accuracy by Direction in Drill: 25 Targets DB Scored")

    st.altair_chart(DB_all_direction_hits_altair_chart, use_container_width=True)





# Main application
st.title("Shotgun Data Analysis")

# Page selector
page = st.sidebar.selectbox("Select Page", ["Competition Analysis", "Training Analysis"])

uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx", "xlsm"])

if uploaded_file:
    if page == "Competition Analysis":
        # Competition analysis
        data = preprocess_competition_data(uploaded_file)

        disciplines = data['Discipline'].dropna().unique()
        event_types = data['Domestic / International'].dropna().str.strip().unique()

        discipline = st.sidebar.selectbox("Select Discipline", sorted(disciplines))
        event_type = st.sidebar.selectbox("Select Event Type", sorted(event_types))
        start_year = st.sidebar.slider("Start Year", int(data['Last Day of Competition'].dt.year.min()),
                                       int(data['Last Day of Competition'].dt.year.max()), 2020)
        end_year = st.sidebar.slider("End Year", start_year, int(data['Last Day of Competition'].dt.year.max()), 2024)


        def average_scores_by_place(data, discipline, start_year, end_year, event_type):
            filtered_data = data[
                (data['Discipline'] == discipline) &
                (data['Domestic / International'].str.strip() == event_type) &
                (data['Last Day of Competition'].dt.year >= start_year) &
                (data['Last Day of Competition'].dt.year <= end_year)
                ]
            results = (
                filtered_data.groupby('Place')['Qualifying Score']
                .mean()
                .reindex(range(1, 7), fill_value=None)
                .to_dict()
            )
            finals_results = (
                filtered_data.groupby('Final Position')['Finals Score']
                .mean()
                .reindex(range(1, 7), fill_value=None)
                .to_dict()
            )
            return {place: {'Qualifying Score': results.get(place), 'Finals Score': finals_results.get(place)} for place
                    in range(1, 7)}


        if st.sidebar.button("Analyze"):
            results = average_scores_by_place(data, discipline, start_year, end_year, event_type)

            st.header(f"Average Scores for {discipline} ({event_type}) from {start_year} to {end_year}")

            for place, scores in results.items():
                st.subheader(f"Place {place}")
                st.write(f"Qualifying Score: {scores['Qualifying Score']:.2f}" if pd.notna(
                    scores['Qualifying Score']) else "Qualifying Score: N/A")
                st.write(f"Finals Score: {scores['Finals Score']:.2f}" if pd.notna(
                    scores['Finals Score']) else "Finals Score: N/A")



    elif page == "Training Analysis":

        # Training analysis
        training_data = preprocess_training_data(uploaded_file)

        # Ensure the 'Date' column is in datetime format
        training_data['Date'] = pd.to_datetime(training_data['Date'], errors='coerce')

        # Get unique dates and athletes from the training data
        date_list = pd.to_datetime(training_data['Date'].dropna().drop_duplicates(keep='first'))

        athletes = training_data['Athlete_Name'].dropna().drop_duplicates(keep='first')

        # Sidebar selection for date and athlete

        date_selection_options = ["All Dates Combined"] + list(date_list)
        selected_date = st.sidebar.selectbox(
            "Choose a Training Date",
            date_selection_options,
            format_func=lambda x: x.strftime('%d-%m-%Y') if isinstance(x, pd.Timestamp) else x
        )

        athlete_selection_options = ["All Athletes Combined"] + list(athletes)
        selected_athlete = st.sidebar.selectbox("Choose an Athlete", athlete_selection_options)

        # Filter and analyze the data
        if selected_date == "All Dates Combined":
            if selected_athlete == "All Athletes Combined":
                filtered_data = training_data  # No filtering, include all data
            else:
                filtered_data = training_data[training_data['Athlete_Name'] == selected_athlete]
        else:
            if selected_athlete == "All Athletes Combined":
                filtered_data = training_data[training_data['Date'] == selected_date]
            else:
                filtered_data = training_data[
                    (training_data['Date'] == selected_date) &
                    (training_data['Athlete_Name'] == selected_athlete)
                    ]

        if not filtered_data.empty:
            generate_training_report(filtered_data, selected_date)
        else:
            if selected_date == "All Dates Combined":
                st.warning(f"No training data found for {selected_athlete} across all dates.")
            else:
                st.warning(f"No training data found for {selected_athlete} on {selected_date.strftime('%d-%m-%Y')}.")



else:
    st.info("Please upload an Excel file to proceed.")
