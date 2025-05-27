import altair as alt
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from streamlit import dataframe
from processing import preprocess_competition_data, preprocess_training_data, preprocess_athlete_names



def generate_competition_report(data, selected_athlete, output, selected_discipline):

    # ----------------------------------
    # -------- Data Filtering ----------
    # ----------------------------------

    # Filter data by athlete


    if selected_athlete == "All Athletes Combined":
        filtered_data = data[data['Final Position'] == 1]  # Use only data from winners
        filtered_data = filtered_data[filtered_data['Discipline'] == selected_discipline]
    else:
        filtered_data = data[data['Athlete UI'] == selected_athlete]

    # Filter data for results history
    result_history = filtered_data[
        ['Athlete UI', 'Event Name', 'Discipline', 'Qualifying Score', 'Qualifying Targets', 'Finals Score', 'Finals Targets', 'Last Day of Competition',
         'Domestic / International']]


    # Filter data for only competitions with a full qualifying round and sort by date
    qualifying_results = result_history[result_history['Qualifying Targets'] == 125]
    qualifying_competitions_by_date = qualifying_results.sort_values(by='Last Day of Competition')



    # -----------------------------------
    # ------- Data Calculations ---------
    # -----------------------------------

    #Calculate average from last 3 competitions
    average_last_3 = qualifying_competitions_by_date.tail(3)[['Qualifying Score', 'Qualifying Targets']].mean()
    average_last_3_text = f"Last 3 Comps: {average_last_3['Qualifying Score']:.2f} / {average_last_3['Qualifying Targets']:.2f}"

    #Calculate average from all competitions in the last 12 months
    one_year_ago = datetime.today() - timedelta(days=365)
    last_12_months = qualifying_competitions_by_date[qualifying_competitions_by_date['Last Day of Competition'] >= one_year_ago]
    average_12_months = last_12_months[['Qualifying Score', 'Qualifying Targets']].mean()
    average_12_months_text = f"Last 12 Months: {average_12_months['Qualifying Score']:.2f} / {average_12_months['Qualifying Targets']:.2f}"

    #Calculate average from all competitions in the last 24 months
    two_years_ago = datetime.today() - timedelta(days=730)
    last_24_months = qualifying_competitions_by_date[qualifying_competitions_by_date['Last Day of Competition'] >= two_years_ago]
    average_24_months = last_24_months[['Qualifying Score', 'Qualifying Targets']].mean()
    average_24_months_text = f"Last 24 Months: {average_24_months['Qualifying Score']:.2f} / {average_24_months['Qualifying Targets']:.2f}"

    #Calculate APS (average of highest three results from previous year and current year)
    def aps_score():
        current_year = datetime.now().year
        previous_year = current_year - 1
        aps_data = qualifying_results[
            (qualifying_results['Last Day of Competition'].dt.year.isin([current_year, previous_year]))
            ]
        top_scores = aps_data['Qualifying Score'].nlargest(3)

        # Return APS (average of top 3 scores)
        if len(top_scores) >= 1:
            aps_score_value = round(top_scores.mean(), 1)
            aps_score_text = f"APS: {aps_score_value}"
            return aps_score_text

        else:
            return "Not enough scores to calculate APS"


    #Calculate DB hit rate for last 12 months
    total_hits_12_months = last_12_months['Qualifying Score'].sum()
    total_targets_12_months = last_12_months['Qualifying Targets'].sum()
    qualifying_hit_rate = round(100*(total_hits_12_months / total_targets_12_months),1)
    qualifying_hit_rate_text = f"Double Barrel: {qualifying_hit_rate}%"

    # Generate SB chart for last 12 months
    total_misses_12_months = total_targets_12_months - total_hits_12_months
    db_hit_data = {'Hit': [total_hits_12_months],
                   'Miss': [total_misses_12_months]}
    db_chart_data = pd.DataFrame(data=db_hit_data, index=[''])

    #Calculate SB hit rate for last 12 months
    total_sb_hits_12_months = last_12_months['Finals Score'].sum()
    total_sb_targets_12_months = last_12_months['Finals Targets'].sum()
    finals_hit_rate = round(100*(total_sb_hits_12_months / total_sb_targets_12_months),1)
    finals_hit_rate_text = f"Single Barrel: {finals_hit_rate}%"

    #Generate SB chart for last 12 months
    total_sb_misses_12_months = total_sb_targets_12_months - total_sb_hits_12_months
    sb_hit_data = {'Hit': [total_sb_hits_12_months],
                   'Miss': [total_sb_misses_12_months]}
    sb_chart_data = pd.DataFrame(data=sb_hit_data, index=[''])

    # Add a new column for qualifying result and finals result that shows score/targets
    qualifying_competitions_by_date['Qualifying Result'] = qualifying_competitions_by_date['Qualifying Score'].astype(str) + " / " + data[
        'Qualifying Targets'].astype(str)
    qualifying_competitions_by_date['Finals Result'] = qualifying_competitions_by_date['Finals Score'].astype(str) + " / " + data[
        'Finals Targets'].astype(str)

    # Generate tables for last 3 domestic competition results
    domestic_results = qualifying_competitions_by_date[qualifying_competitions_by_date['Domestic / International'] == 'Domestic']
    domestic_display= domestic_results[['Event Name', 'Qualifying Result', 'Finals Result']]

    # Generate tables for last 3 international competition results
    international_results = qualifying_competitions_by_date[qualifying_competitions_by_date['Domestic / International'] == 'International']
    international_display= international_results[['Event Name', 'Qualifying Result', 'Finals Result']]



    # --------------------------------------
    # ---------- Function outputs ----------
    # --------------------------------------

    # When info is requested

    if output == "info":
        if selected_athlete == "All Athletes Combined":
            st.write(f"Results for top ranked {selected_discipline} athlete after final")

    elif output == "recent_results":
        st.subheader("Last 5 Competition Results")
        st.write('Domestic')
        st.dataframe(domestic_display.tail(5).reset_index(drop=True), hide_index=True)
        st.write('International')
        st.dataframe(international_display.tail(5).reset_index(drop=True), hide_index=True)

    # When avg_performance is requested

    elif output == "avg_performance":
        st.subheader('125 in Competition')
        st.write(aps_score())
        st.write(average_last_3_text)
        st.write(average_12_months_text)
        st.write(average_24_months_text)
        st.subheader('12-month Hit Rate')
        st.write(qualifying_hit_rate_text)
        st.bar_chart(
            db_chart_data,
            color=["#eab464ff", "#dcccbbff"],
            horizontal="true"
        )
        st.write(finals_hit_rate_text)
        st.bar_chart(
            sb_chart_data,
            color=["#eab464ff", "#dcccbbff"],
            horizontal="true"
        )
        # TODO st.write('12 months shoot offs: xx%')

    #Function output when 'output' is an invalid request

    else:
        st.warning("Error: competition report, output request failed.")








def generate_training_report(data, selected_athlete, selected_date, output):


    # ----------------------------------
    # -------- Data Filtering ----------
    # ----------------------------------

    # Filter data by athlete and Date

    if selected_date == "All Dates Combined":
        if selected_athlete == "All Athletes Combined":
            filtered_data = data  # No filtering, include all data
        else:
            filtered_data = data[data['Athlete_Name'] == selected_athlete]
    else:
        if selected_athlete == "All Athletes Combined":
            filtered_data = data[data['Date'] == selected_date]
        else:
            filtered_data = data[
                (data['Date'] == selected_date) &
                (data['Athlete_Name'] == selected_athlete)]



    # -----------------------------------
    # ------- Data Calculations ---------
    # -----------------------------------

    # Only run calculations if there is data to work with

    if not filtered_data.empty:
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
        #DB_hit_data = {'Hits': [first_barrel_hits, second_barrel_hits],
        #               'Misses': [missed_first_barrel, missed_second_barrel]}
        #DB_chart_data = pd.DataFrame(data=DB_hit_data, index=['B1', 'B2'])



        DB_hit_data = {'B1 Hit': [first_barrel_hits],
                       'B2 Hit': [second_barrel_hits],
                       'Miss': [missed_second_barrel]}
        DB_chart_data = pd.DataFrame(data=DB_hit_data, index=[''])

        DB_chart_data_altair_chart = (
            alt.Chart(DB_chart_data)
            .mark_bar()
            .encode(
                x=alt.X("Value:Q", title="Value"),
                y=alt.Y("Category:N", title="Category", sort="-x"),  # Horizontal Bars
                color=alt.Color(
                    "Legend:N",  # Replace with a meaningful column for legend grouping
                    scale=alt.Scale(range=["#eab464", "#a17e4a", "#dcccbb"])
                )
            )
            .properties(width=600, height=400)
            .configure_legend(orient="top")  # Move legend to the top
        )




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
            .properties(height=250)
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
            .properties(height=250)
        )

        # Build heatmap

        dummy_timing_data = pd.DataFrame({
            'X': ['Left', 'Left', 'Left', 'Straight', 'Straight', 'Straight', 'Right', 'Right', 'Right'],
            'Y': ['Low', 'Mid', 'High', 'Low', 'Mid', 'High', 'Low', 'Mid', 'High'],
            'Value': ['', 0.5, 1, 0.4, '', 0.6, 0.9, 0.8, 0.7]
        })
        dummy_timing_data['Value'] = pd.to_numeric(dummy_timing_data['Value'], errors='coerce').fillna(-0.01)

        # Create an Altair heatmap
        heatmap = alt.Chart(dummy_timing_data).mark_rect().encode(
            x=alt.X('X:N', title=None, sort=["Left", "Straight", "Right"]),
            y=alt.Y('Y:N', title=None, sort=["High", "Mid", "Low"]),
            color=alt.Color('Value:Q',
                            scale=alt.Scale(
                                domain=[-0.01, 0, 0.2, 0.8, 1],  # Add -1 for the special color
                                range=["#dcccbbff", "#70490f", "#70490f", "#eab464", "#e49d35"]  # Color for NaN (-1) and Intensity colors
                            ),
                            title="Hit rate").legend(values=[0.0, 1.0]),
            #legend=alt.Legend(title="Intensity", values=[0.2, 0.5, 1.0]),  # Explicit legend values
            tooltip=['X', 'Y', 'Value']
        ).properties(
            width=400,
            height=300
        )



        # Assess shot timing
        def timing_by_direction(direction):
            shots_with_timing_data = double_barrel.dropna(subset=['Shot Timing'])
            data = shots_with_timing_data[shots_with_timing_data['Direction'] == direction]
            avg_timing = data['Shot Timing'].mean().round(2)
            stdev_timing = data['Shot Timing'].std().round(2)
            data_text_output = f"Shot timing ({str(direction)}): {avg_timing} +/- {stdev_timing} seconds"

            return data_text_output



        # Single barrel accuracy
        sb_hits = len(single_barrel[single_barrel['Hit'] == 1])
        total_sb_shots = len(single_barrel)
        sb_misses = total_sb_shots - sb_hits
        sb_accuracy = sb_hits / total_sb_shots if total_sb_shots > 0 else 0

        SB_hit_data = {'B1 Hit': [sb_hits],
                       'Miss': [sb_misses]}
        SB_chart_data = pd.DataFrame(data=SB_hit_data, index=[''])

        # Generate charts

        # -------------------------------------
        # ------------- OUTPUTS ---------------
        # -------------------------------------



        if output == "session_info":
            # Find session name for that training day
            session_name = filtered_data['Event/Camp'].dropna().drop_duplicates(keep='first')

            maximum_events = 4  # Set max number of events to display

            # Truncate the list if it's too long
            if len(session_name) > maximum_events:
                session_list = ", ".join(session_name[:maximum_events]) + "..."
            else:
                session_list = ", ".join(session_name)

            # Output the list of sessions that training data will be calculated from
            st.write(f"Events/Camps on this date: {session_list}")



        elif output == "barrel_accuracy":
            st.subheader("Training Hit Rate")
            st.write("Double Barrel: " + str(round(100 * double_barrel_accuracy, 1)) + "%")
            st.bar_chart(
                DB_chart_data,
                color=["#eab464ff", "#a17e4aff", "#dcccbbff"],
                horizontal="true"
            )
            st.write("Single Barrel: " + str(round(100 * sb_accuracy, 1)) + "%")
            st.bar_chart(
                SB_chart_data,
                color=["#eab464ff", "#dcccbbff"],
                horizontal="true"
            )


        elif output == "shot_timing":
            st.subheader("Shot timing")
            st.write('"Shot timing" refers to the time between "pull" and the first gunshot')
            st.write(timing_by_direction('L'))
            st.write(timing_by_direction('S'))
            st.write(timing_by_direction('R'))


        elif output == "station_and_direction":
            st.subheader("DB targets per station")
            st.altair_chart(DB_all_station_hits_altair_chart, use_container_width=True)
            st.subheader("DB targets per direction")
            st.altair_chart(DB_all_direction_hits_altair_chart, use_container_width=True)

        elif output == "station":
            st.subheader("DB targets per station")
            st.altair_chart(DB_all_station_hits_altair_chart, use_container_width=True)

        elif output == "direction":
            st.subheader("DB targets per direction")
            st.altair_chart(DB_all_direction_hits_altair_chart, use_container_width=True)

        elif output == "trajectory":
            st.subheader("Target trajectory heatmap")
            st.write('Currently this is dummy data')
            st.altair_chart(heatmap, use_container_width=True)

        else:
            st.warning("Error: training report, output request failed.")




    # -------------------------------------
    # ----- No Data: No Calculation -------
    # -------------------------------------

    else:
        if selected_date == "All Dates Combined":
            st.warning(f"No training data found for {selected_athlete} across all dates.")
        else:
            st.warning(f"No training data found for {selected_athlete} on {selected_date.strftime('%d-%m-%Y')}.")






def DB_accuracy():
    DB_hit_data = {'B1 Hit': [first_barrel_hits],
                   'B2 Hit': [second_barrel_hits],
                   'Miss': [missed_second_barrel]}
    DB_chart_data = pd.DataFrame(data=DB_hit_data, index=[''])

    return DB_chart_data

