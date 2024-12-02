import streamlit as st
import pandas as pd

individual_shots = pd.read_csv('data/training_shots.csv')

def hitrate(ath, hit):

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
    answer = hit_table.loc[:, ["Drill", "Athlete_Name", "Shot_no", "Station_no", "SB", "Hit", "Direction", "Comment"]]
    return answer

def score(ath):
    hit_table_hits = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit.isin([1,2]))]
    hit_table_misses = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit.isin([0]))]
    hit_table_total = individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit.isin([1,2,0]))]
    no_hits = hit_table_hits.shape[0]
    no_total = hit_table_total.shape[0]
    return ath + " hit " + str(no_hits) + " out of " + str(no_total)


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
st.dataframe(hitrate(a_n,s_i))



# TODO
    # create table for hit percentage
    # Columns: First shot, second shot, total hits, misses
    # Rows v1: L, R, S, all
    # Rows v2: Station 1, 2, 3, 4, 5, all

