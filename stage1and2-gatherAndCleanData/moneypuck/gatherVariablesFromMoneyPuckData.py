import pandas as pd 

allshots2023 = pd.read_csv("moneypuckData/gameLevelData/shots_2023.csv")

# get reg season only
regularSeason = allshots2023[allshots2023['isPlayoffGame'] == 0]

# Full strength: 5-on-5, no penalties, no empty net
fullStrength = regularSeason[
    (regularSeason['awaySkatersOnIce'] == 5) &
    (regularSeason['homeSkatersOnIce'] == 5) &
    (regularSeason['homeEmptyNet'] == 0) &
    (regularSeason['awayEmptyNet'] == 0) &
    (regularSeason['homePenalty1TimeLeft'] == 0) &
    (regularSeason['awayPenalty1TimeLeft'] == 0)
]

# get shots on goal
shotsOnGoal = fullStrength[fullStrength['shotWasOnGoal'] == 1]

# get all shots on goal

allShotsOnGoal = regularSeason[regularSeason['shotWasOnGoal']==1]

# home shots (5on5)
homeShots5on5 = (
    shotsOnGoal[shotsOnGoal['isHomeTeam'] == 1]
    .groupby('game_id')['shotID']
    .nunique()
    .reset_index(name='homeTeamShotsOnGoal5on5')
)

# away shots (5on5)
awayShots5on5 = (
    shotsOnGoal[shotsOnGoal['isHomeTeam'] == 0]
    .groupby('game_id')['shotID']
    .nunique()
    .reset_index(name='awayTeamShotsOnGoal5on5')
)

# home shots (all)
homeShotsAll = (
    allShotsOnGoal[allShotsOnGoal['isHomeTeam'] == 1]
    .groupby('game_id')['shotID']
    .nunique()
    .reset_index(name='homeTeamShotsOnGoalAll')
)

# away shots (all)
awayShotsAll = (
    allShotsOnGoal[allShotsOnGoal['isHomeTeam'] == 0]
    .groupby('game_id')['shotID']
    .nunique()
    .reset_index(name='awayTeamShotsOnGoalAll')
)

result = pd.merge(homeShots5on5, awayShots5on5, on='game_id')
result = pd.merge(result, homeShotsAll, on='game_id')
result = pd.merge(result, awayShotsAll, on='game_id')

# add team codes
result = pd.merge(result, allshots2023[['game_id', 'homeTeamCode', 'awayTeamCode']].drop_duplicates(), on='game_id')

# get defender shots 
# hypothesis: more defender shots are taken by teams that shoot more, as it is a low percentage shot and typically possession is lost after

defender_shots = shotsOnGoal[shotsOnGoal['playerPositionThatDidEvent'] == 'D']

# home defender shots
home_defender_shots = (
    defender_shots[defender_shots['isHomeTeam'] == 1]
    .groupby('game_id')['shotID']
    .nunique()
    .reset_index(name='homeDefenderShots')
)

# away defender shots 
away_defender_shots = (
    defender_shots[defender_shots['isHomeTeam'] == 0]
    .groupby('game_id')['shotID']
    .nunique()
    .reset_index(name='awayDefenderShots')
)

# merge defender shots
result = pd.merge(result, home_defender_shots, on='game_id', how='left')
result = pd.merge(result, away_defender_shots, on='game_id', how='left')

# fill nan values
result['homeDefenderShots'] = result['homeDefenderShots'].fillna(0)
result['awayDefenderShots'] = result['awayDefenderShots'].fillna(0)

# filter by longshots
# 41.34feet threshold calculated as the distance from the goalline to the top of the faceoff dot
# measurements from: https://en.wikipedia.org/wiki/Ice_hockey_rink
# hypothesis: teams that take more long shots will shoot more in general, similar to hypothesis for defender shot ratio

long_shots = shotsOnGoal[shotsOnGoal['arenaAdjustedShotDistance'] > 41.34]

# home team long shots
home_long_shots = (
    long_shots[long_shots['isHomeTeam'] == 1]
    .groupby('game_id')['shotID']
    .nunique()
    .reset_index(name='homeLongShots')
)

# away team long shots
away_long_shots = (
    long_shots[long_shots['isHomeTeam'] == 0]
    .groupby('game_id')['shotID']
    .nunique()
    .reset_index(name='awayLongShots')
)

# merge long shots
result = pd.merge(result, home_long_shots, on='game_id', how='left')
result = pd.merge(result, away_long_shots, on='game_id', how='left')

# fill nan values
result['homeLongShots'] = result['homeLongShots'].fillna(0)
result['awayLongShots'] = result['awayLongShots'].fillna(0)

# teams that get more 'tip' shots shoot less in general, because tipping the puck requires set up in the zone, and getting a cycle going often, which takes time

# relevant shot types found in moneypuck data
shot_types = ['WRIST', 'SLAP', 'SNAP', 'BACK', 'TIP']

for shot_type in shot_types:
    # get shot type
    shot_type_data = shotsOnGoal[shotsOnGoal['shotType'] == shot_type]
    
    # get shot count for home
    home_shot_type = (
        shot_type_data[shot_type_data['isHomeTeam'] == 1]
        .groupby('game_id')['shotID']
        .nunique()
        .reset_index(name=f'home{shot_type}Shots')
    )
    
    # get shot count for away
    away_shot_type = (
        shot_type_data[shot_type_data['isHomeTeam'] == 0]
        .groupby('game_id')['shotID']
        .nunique()
        .reset_index(name=f'away{shot_type}Shots')
    )
    
    # merge
    result = pd.merge(result, home_shot_type, on='game_id', how='left')
    result = pd.merge(result, away_shot_type, on='game_id', how='left')
    
    # fill nan values
    result[f'home{shot_type}Shots'] = result[f'home{shot_type}Shots'].fillna(0)
    result[f'away{shot_type}Shots'] = result[f'away{shot_type}Shots'].fillna(0)

# hypothesis: more rebound shots are a result of teams taking low percentage shots? which would maybe be teams that shoot more in general

# filter for rebound shots (defined as shots taken within 3 shots from the last one measured)
rebound_shots = shotsOnGoal[shotsOnGoal['shotRebound'] == 1]

# calc home rebound shots
home_rebound_shots = (
    rebound_shots[rebound_shots['isHomeTeam'] == 1]
    .groupby('game_id')['shotID']
    .nunique()
    .reset_index(name='homeReboundShots')
)

# calc away rebound shots
away_rebound_shots = (
    rebound_shots[rebound_shots['isHomeTeam'] == 0]
    .groupby('game_id')['shotID']
    .nunique()
    .reset_index(name='awayReboundShots')
)

# merge
result = pd.merge(result, home_rebound_shots, on='game_id', how='left')
result = pd.merge(result, away_rebound_shots, on='game_id', how='left')

#fill nan
result['homeReboundShots'] = result['homeReboundShots'].fillna(0)
result['awayReboundShots'] = result['awayReboundShots'].fillna(0)

#rename categories for clarity
#https://pandas.pydata.org/pandas-docs/version/0.19/generated/pandas.DataFrame.rename.html
#https://stackoverflow.com/questions/16770227/how-can-i-change-name-of-arbitrary-columns-in-pandas-df-using-lambda-function
result.rename(columns=lambda x: x.replace("BACK", "BACKHAND"), inplace=True)

# save to csv
result.to_csv("stage1and2-gatherAndCleanData/moneypuck/VariablesFromMoneyPuck.csv", index=False)

