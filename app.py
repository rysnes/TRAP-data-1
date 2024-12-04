import streamlit as st
from formulas import *

individual_shots = pd.read_csv('data/training_shots.csv')


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
        hit_table = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit.isin([0,2]))]
    elif hit == 4:
        hit_table = individual_shots.loc[individual_shots.Athlete_Name == ath]
    else:
        hit_table = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit == hit)]
    hit_table_display = hit_table.loc[:, ["Drill", "Athlete_Name", "Shot_no", "Station_no", "SB", "Hit", "Direction", "Comment"]]
    return hit_table_display

def score(ath):
    return ath + " hit " + str(totalHits(ath)) + " out of " + str(totalTargets(ath))

def printDoubleBarrelCount(ath):
    return ath + " shot at " + str(doubleBarrelTargets(ath)) + " targets with a double barrel"

def printDoubleBarrelFirstAccuracy(ath):
    percentshown = round(100 * doubleBarrelFirstShotAccuracy(ath),1)
    return "First Barrel Accuracy:  " + str(percentshown) + "%"

def printDoubleBarrelSecondAccuracy(ath):
    percentshown = round(100 *secondShotAccuracy(ath),1)
    return "Second Barrel Accuracy:  " + str(percentshown) + "%"

def printSingleBarrelCount(ath):
    return ath + " shot at " + str(singleBarrelTargets(ath)) + " targets with a single barrel"

def printSingleBarrelAccuracy(ath):
    percentshown = round(100 *singleBarrelAccuracy(ath),1)
    return "With an accuracy of:  " + str(percentshown) + "%"


name_list = individual_shots.Athlete_Name.drop_duplicates(keep='first')


# streamlit code for a webpage

st.header("Shot Info")

a_n = st.selectbox("Choose an athlete", name_list)

s_i = st.selectbox("Hit information to show", ["Firsts", "Seconds", "Misses", "Seconds and Misses", "All"])


# ath = Athlete_Name case sensitve as entered in csv.
# hit = the hit type you want information about
# if hit = 3, all 2nd's and misses will be shown

#python only
#hitrate("Gab", 3)
# score("Gab")


#streamlit
st.write(score(a_n))
st.dataframe(hitTable(a_n,s_i))

def doubleBarrelHitChartData(ath):
    d = {'Hits': [doubleBarrelHitsOnFirst(ath), totalHitsOnSecond(ath)], 'Misses': [doubleBarrelMissesOnFirst(ath), totalMissesOnSecond(ath)]}
    hit_chart_data = pd.DataFrame(data = d, index = ['First Barrel', 'Second Barrel'])
    return hit_chart_data

def singleBarrelHitChartData(ath):
    d = {'Hits': [totalHitsOnSingleBarrel(ath), 0], 'Misses': [totalMissesOnSingleBarrel(ath), 0]}
    sb_hit_chart_data = pd.DataFrame(data = d, index = ['First Barrel', 'Second Barrel'])
    return sb_hit_chart_data

#Data frames to trouble shoot data displayed in bar charts
    #st.dataframe(doubleBarrelHitChartData(a_n))
    #st.dataframe(singleBarrelHitChartData(a_n))

st.header("Accuracy on double barrel targets")
st.write(printDoubleBarrelCount(a_n))
st.write(printDoubleBarrelFirstAccuracy(a_n))
st.write(printDoubleBarrelSecondAccuracy(a_n))

st.bar_chart(
    doubleBarrelHitChartData(a_n),
    color = ["#eab464ff", "#dcccbbff"],
    horizontal = "true"
    )

st.header("Accuracy on single barrel targets")
st.write(printSingleBarrelCount(a_n))
st.write(printSingleBarrelAccuracy(a_n))

st.bar_chart(
    singleBarrelHitChartData(a_n),
    color = ["#eab464ff", "#dcccbbff"],
    horizontal = "true"
    )

# TODO
    # create table for hit percentage LRS
    # Columns: First shot, second shot, total hits, misses
    # Rows v1: L, R, S, all
    # Rows v2: Station 1, 2, 3, 4, 5, all

