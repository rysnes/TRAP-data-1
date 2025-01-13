import streamlit as st
import pandas as pd



def training_page(training_data):


    individual_shots = training_data

    def comp_scores(competition_data):
        data = competition_data

        return data

    def totalTargets(ath):
        shot_table = individual_shots.loc[individual_shots.Athlete_Name == ath]
        no_total_targets = shot_table.shape[0]

        return no_total_targets

    def totalHitsOnFirst(ath):
        hit_table_firsts = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit.isin([1]))]
        no_hits_firsts = hit_table_firsts.shape[0]

        return no_hits_firsts

    def singleBarrelTargets(ath):
        shot_table_sb = individual_shots.loc[
            (individual_shots.Athlete_Name == ath) & (individual_shots.SB.isin(["SB"]))]
        no_total_sb = shot_table_sb.shape[0]

        return no_total_sb

    def doubleBarrelTargets(ath):
        no_total_db = totalTargets(ath) - singleBarrelTargets(ath)

        return no_total_db

    def totalHitsOnSingleBarrel(ath):
        hit_table_sb = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.SB.isin(["SB"])) & (individual_shots.Hit.isin([1]))]
        no_total_hits_sb = hit_table_sb.shape[0]

        return no_total_hits_sb

    def totalMissesOnSingleBarrel(ath):
        no_total_sb_misses = singleBarrelTargets(ath) - totalHitsOnSingleBarrel(ath)

        return no_total_sb_misses

    def totalHitsOnSecond(ath):
        hit_table_seconds = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit.isin([2]))]
        no_hits_seconds = hit_table_seconds.shape[0]

        return no_hits_seconds

    def doubleBarrelHitsOnFirst(ath):
        no_db_hits_on_first = totalHitsOnFirst(ath) - totalHitsOnSingleBarrel(ath)

        return no_db_hits_on_first

    def doubleBarrelMissesOnFirst(ath):
        no_db_misses_on_first = doubleBarrelTargets(ath) - doubleBarrelHitsOnFirst(ath)

        return no_db_misses_on_first

    def totalMissesOnSecond(ath):
        no_misses_seconds = doubleBarrelMissesOnFirst(ath) - totalHitsOnSecond(ath)

        return no_misses_seconds

    def totalHits(ath):
        hit_table_hits = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit.isin([1, 2]))]
        no_total_hits = hit_table_hits.shape[0]

        return no_total_hits

    def totalDBHits(ath):
        no_total_hits_DB = doubleBarrelHitsOnFirst(ath) + totalHitsOnSecond(ath)

        return no_total_hits_DB

    def doubleBarrelAccuray(ath):
        percentage_DB = totalDBHits(ath) / doubleBarrelTargets(ath)

        return percentage_DB

    def totalMisses(ath):
        hit_table_misses = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit.isin([0]))]
        no_total_misses = hit_table_misses.shape[0]

        return no_total_misses

    def firstShotAccuracy(ath):
        percentage_firsts = totalHitsOnFirst(ath) / totalTargets(ath)

        return percentage_firsts

    def doubleBarrelFirstShotAccuracy(ath):
        percentage = doubleBarrelHitsOnFirst(ath) / doubleBarrelTargets(ath)

        return percentage

    def secondShotAccuracy(ath):
        percentage_seconds = totalHitsOnSecond(ath) / doubleBarrelMissesOnFirst(ath)

        return percentage_seconds

    def firstShotMisses(ath):
        no_firsts_misses = totalTargets(ath) - totalHitsOnFirst(ath)

        return no_firsts_misses

    def singleBarrelAccuracy(ath):
        percentage_sb = totalHitsOnSingleBarrel(ath) / singleBarrelTargets(ath)

        return percentage_sb

    # Competition

    def comp_totalTargets(ath):
        score_table = comp_scores.loc[
            (comp_scores.Athlete_UI == ath) & (comp_scores.Qualifying_Targets.notna())
            ]
        no_total_targets = score_table.Qualifying_Targets.sum()

        return no_total_targets

    def compFinal_totalTargets(ath):
        score_table = comp_scores.loc[
            (comp_scores.Athlete_UI == ath) & (comp_scores.Finals_Targets.notna())
            ]
        no_finals_targets = score_table.Finals_Targets.sum()

        return no_finals_targets

    def comp_totalTargetsHit(ath):
        score_table = comp_scores.loc[
            (comp_scores.Athlete_UI == ath) & (comp_scores.Qualifying_Targets.notna())
            ]
        no_total_targets = score_table.Qualifying_Score.sum()

        return no_total_targets

    def compFinal_totalTargetsHit(ath):
        score_table = comp_scores.loc[
            (comp_scores.Athlete_UI == ath) & (comp_scores.Finals_Targets.notna())
            ]
        no_total_targets = score_table.Finals_Score.sum()

        return no_total_targets

    def comp_totalTargetsMissed(ath):
        no_comp_misses = comp_totalTargets(ath) - comp_totalTargetsHit(ath)

        return no_comp_misses

    def compFinal_totalTargetsMissed(ath):
        no_comp_misses = compFinal_totalTargets(ath) - compFinal_totalTargetsHit(ath)

        return no_comp_misses

    def comp_accuracy(ath):
        percentage_comp = comp_totalTargetsHit(ath) / comp_totalTargets(ath)

        return percentage_comp

    def compFinal_accuracy(ath):
        percentage_comp = compFinal_totalTargetsHit(ath) / compFinal_totalTargets(ath)

        return percentage_comp


    def hitTable(ath, hit):

        if hit == "Firsts":
            hit = 1
        if hit == "Seconds":
            hit = 2
        if hit == "Misses":
            hit = 0
        if hit == "Seconds and Misses":
            hit = 3
        if hit == "All":
            hit = 4

        if hit == 3:
            hit_table = individual_shots.loc[
                (individual_shots.Athlete_Name == ath) & (individual_shots.Hit.isin([0, 2]))]
        elif hit == 4:
            hit_table = individual_shots.loc[individual_shots.Athlete_Name == ath]
        else:
            hit_table = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit == hit)]

        hit_table_display = hit_table.loc[:,
                            ["Drill", "Athlete_Name", "Shot_no", "Station_no", "SB", "Hit", "Direction", "Comment"]]
        return hit_table_display

    def score(ath):
        return "Shot at " + str(totalTargets(ath)) + " targets, in total, and hit " + str(totalHits(ath)) + ""

    def printDoubleBarrelCount(ath):
        percentshown = round(100 * doubleBarrelAccuray(ath), 1)
        return str(percentshown) + "%"

    def printDoubleBarrelFirstAccuracy(ath):
        percentshown = round(100 * doubleBarrelFirstShotAccuracy(ath), 1)
        return "First Barrel Accuracy:  " + str(percentshown) + "%"

    def printDoubleBarrelSecondAccuracy(ath):
        percentshown = round(100 * secondShotAccuracy(ath), 1)
        return "Second Barrel Accuracy:  " + str(percentshown) + "%"

    def printSingleBarrelCount(ath):
        return str(singleBarrelTargets(ath)) + " targets were shot at with a single barrel loaded"

    def printSingleBarrelAccuracy(ath):
        percentshown = round(100 * singleBarrelAccuracy(ath), 1)
        return str(percentshown) + "%"

    name_list = individual_shots.Athlete_Name.drop_duplicates(keep='first')

    # streamlit code for a webpage


    a_n = st.selectbox("Choose an athlete", name_list)
    st.header("Training Report:  " + str(a_n))
    st.write(score(a_n))

    #s_i = st.selectbox("Hit information to show", ["Firsts", "Seconds", "Misses", "Seconds and Misses", "All"]
    #st.dataframe(hitTable(a_n, s_i))

    print(a_n)
    def doubleBarrelHitChartData(ath):
        d = {'Hits': [doubleBarrelHitsOnFirst(ath), totalHitsOnSecond(ath)],
             'Misses': [doubleBarrelMissesOnFirst(ath), totalMissesOnSecond(ath)]}
        hit_chart_data = pd.DataFrame(data=d, index=['First Barrel', 'Second Barrel'])
        return hit_chart_data

    def singleBarrelHitChartData(ath):
        d = {'Hits': [totalHitsOnSingleBarrel(ath), 0], 'Misses': [totalMissesOnSingleBarrel(ath), 0]}
        sb_hit_chart_data = pd.DataFrame(data=d, index=['First Barrel', 'Second Barrel'])
        return sb_hit_chart_data

    # Data frames to trouble shoot data displayed in bar charts
    # st.dataframe(doubleBarrelHitChartData(a_n))
    # st.dataframe(singleBarrelHitChartData(a_n))

    st.write("*These statistics assume that all recorded shots are shot with a double barrel and hit with the first barrel, unless otherwise noted. If the data is incorrectly recorded, the statistics may overestimate first barrel accuracy*")

    st.header("Double Barrel Accuracy:  " + printDoubleBarrelCount(a_n))
    st.write(str(doubleBarrelTargets(a_n)) + " targets were shot at with a double barrel loaded.")
    st.write(printDoubleBarrelFirstAccuracy(a_n))
    st.write(printDoubleBarrelSecondAccuracy(a_n))

    st.bar_chart(
        doubleBarrelHitChartData(a_n),
        color=["#eab464ff", "#dcccbbff"],
        horizontal="true"
    )

    st.header("Single Barrel Accuracy:  " + printSingleBarrelAccuracy(a_n))
    st.write(printSingleBarrelCount(a_n))

    st.bar_chart(
        singleBarrelHitChartData(a_n),
        color=["#eab464ff", "#dcccbbff"],
        horizontal="true"
    )

    #TODO
    # add date ranges to comp and training
    # create table for hit percentage LRS
    # Columns: First shot, second shot, total hits, misses
    # Rows v1: L, R, S, all
    # Rows v2: Station 1, 2, 3, 4, 5, all


