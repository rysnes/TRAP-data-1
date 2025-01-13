import pandas as pd


#comp_scores = pd.read_csv('data/comp_scores.csv')


#Training


def shots():
    data = individual_shots

    return data

def comp_scores(competition_data):
    data = competition_data

    return data


def totalTargets(ath):
    shot_table = shots.loc[shots.Athlete_Name == ath]
    no_total_targets = shot_table.shape[0]

    return no_total_targets


def totalHitsOnFirst(ath):
    hit_table_firsts = shots.loc[(shots.Athlete_Name == ath) & (shots.Hit.isin([1]))]
    no_hits_firsts = hit_table_firsts.shape[0]

    return no_hits_firsts

def singleBarrelTargets(ath):
    shot_table_sb = shots.loc[
        (shots.Athlete_Name == ath) & (shots.SB.isin(["SB"]))]
    no_total_sb = shot_table_sb.shape[0]

    return no_total_sb

def doubleBarrelTargets(ath):
    no_total_db = totalTargets(ath) - singleBarrelTargets(ath)

    return no_total_db


def totalHitsOnSingleBarrel(ath):
    hit_table_sb = shots.loc[(shots.Athlete_Name == ath) & (shots.SB.isin(["SB"])) & (shots.Hit.isin([1]))]
    no_total_hits_sb = hit_table_sb.shape[0]

    return no_total_hits_sb

def totalMissesOnSingleBarrel(ath):
    no_total_sb_misses = singleBarrelTargets(ath) - totalHitsOnSingleBarrel(ath)

    return no_total_sb_misses

def totalHitsOnSecond(ath):
    hit_table_seconds = shots.loc[(shots.Athlete_Name == ath) & (shots.Hit.isin([2]))]
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
    hit_table_hits= shots.loc[(shots.Athlete_Name == ath) & (shots.Hit.isin([1,2]))]
    no_total_hits= hit_table_hits.shape[0]

    return no_total_hits


def totalDBHits(ath):
    no_total_hits_DB = doubleBarrelHitsOnFirst(ath) + totalHitsOnSecond(ath)

    return no_total_hits_DB

def doubleBarrelAccuray(ath):
    percentage_DB = totalDBHits(ath) / doubleBarrelTargets(ath)

    return percentage_DB


def totalMisses(ath):
    hit_table_misses = shots.loc[(shots.Athlete_Name == ath) & (shots.Hit.isin([0]))]
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



#Commpetition

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
    percentage_comp= comp_totalTargetsHit(ath) / comp_totalTargets(ath)

    return percentage_comp

def compFinal_accuracy(ath):
    percentage_comp= compFinal_totalTargetsHit(ath) / compFinal_totalTargets(ath)

    return percentage_comp

