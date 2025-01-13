import streamlit as st
import pandas as pd
from formulas import *


def competition_page():
    st.title("Competitions")

    #comp_scores = pd.read_csv('data/comp_scores.csv')

    st.header("Competition History")

    scores_AUS = comp_scores.loc[(comp_scores.Country == 'AUS')]
    name_list = scores_AUS.Athlete_UI.drop_duplicates(keep='first')
    #name_list = comp_scores.Athlete_UI.drop_duplicates(keep='first')

    def resultsTable(ath,info):
        if info == "Qualifying":
            show_table = comp_scores.loc[
            (comp_scores.Athlete_UI == ath) & (comp_scores.Qualifying_Targets.notna())
            ]

            resultsTable_display = show_table.loc[:, ["Athlete_UI", "Country", "Discipline", "Event Name", "Domestic / International",
                                                      "Qualifying_Score", "Qualifying_Targets", "Place", "Round 1",
                                                      "Round 2", "Round 3", "Round 4", "Round 5"]]


        elif info == "Final":
            show_table = comp_scores.loc[
                (comp_scores.Athlete_UI == ath) & (comp_scores.Finals_Targets.notna())
                ]

            resultsTable_display = show_table.loc[:, ["Athlete_UI", "Country", "Discipline", "Event Name", "Domestic / International",
                                                      "Qualifying_Score", "Qualifying_Targets", "Finals_Score", "Finals_Targets", "Final Position"]]

        return resultsTable_display

    a_n = st.selectbox("Choose an athlete",name_list)
    info_disp = st.selectbox("Display",["Qualifying", "Final"])
    st.dataframe(resultsTable(a_n,info_disp))

    def print_total_qualifying_targets(ath):
        return ath + " shot at " + str(comp_totalTargets(ath)) + " targets with a double barrel"

    def print_total_finals_targets(ath):
        return ath + " shot at " + str(compFinal_totalTargets(ath)) + " targets with a single barrel"

    def print_total_qualifying_targets_hit(ath):
        return ath + " hit " + str(comp_totalTargetsHit(ath)) + " of those targets"

    def print_total_finals_targets_hit(ath):
        return ath + " hit " + str(compFinal_totalTargetsHit(ath)) + " of those targets"


    def comp_doubleBarrelHitChartData(ath):
        d = {'Hits': [comp_totalTargetsHit(ath)],
             'Misses': [comp_totalTargetsMissed(ath)]}
        hit_chart_data = pd.DataFrame(data=d, index=['Qualifying Shots'])
        return hit_chart_data

    def comp_singleBarrelHitChartData(ath):
        d = {'Hits': [compFinal_totalTargetsHit(ath)],
             'Misses': [compFinal_totalTargetsMissed(ath)]}
        hit_chart_data = pd.DataFrame(data=d, index=['Qualifying Shots'])
        return hit_chart_data

    def printCompAccuracy(ath):
        percentshown = round(100 * comp_accuracy(ath), 1)
        return "Accuracy:  " + str(percentshown) + "%"

    def printCompFinalsAccuracy(ath):
        percentshown = round(100 * compFinal_accuracy(ath), 1)
        return "Accuracy:  " + str(percentshown) + "%"

    st.header("Total Targets - Qualifying")
    st.write(print_total_qualifying_targets(a_n))
    st.write(print_total_qualifying_targets_hit(a_n))
    st.write(printCompAccuracy(a_n))

    st.bar_chart(
        comp_doubleBarrelHitChartData(a_n),
        color=["#eab464ff", "#dcccbbff"],
        horizontal="true"
    )


    st.header("Total Targets - Final")
    st.write(print_total_finals_targets(a_n))
    st.write(print_total_finals_targets_hit(a_n))
    st.write(printCompFinalsAccuracy(a_n))

    st.bar_chart(
        comp_singleBarrelHitChartData(a_n),
        color=["#eab464ff", "#dcccbbff"],
        horizontal="true"
    )

    #TODO
    # add date ranges to comp and training

if __name__ == "__main__":
    app()