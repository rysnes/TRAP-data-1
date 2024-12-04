import pandas as pd
individual_shots = pd.read_csv('data/training_shots.csv')

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
    hit_table_hits= individual_shots.loc[(individual_shots.Athlete_Name == ath) & (individual_shots.Hit.isin([1,2]))]
    no_total_hits= hit_table_hits.shape[0]

    return no_total_hits

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

