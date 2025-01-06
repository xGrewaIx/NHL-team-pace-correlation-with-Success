import pandas as pd

# shot data
shotData = pd.read_csv('stage1and2-gatherAndCleanData/moneypuck/VariablesFromMoneyPuck.csv')

# get all teama codes
teams = shotData['homeTeamCode'].unique()

# dataframe to hold all data
seasonAveragesColNames = [
    'team', 'for_avg_shots_on_goal_5on5', 'for_avg_shots_on_goal_all', 'for_avg_defender_shots', 'for_avg_long_shots', 
    'for_avg_WRIST_shots', 'for_avg_SLAP_shots', 'for_avg_SNAP_shots', 'for_avg_BACKHAND_shots', 'for_avg_TIP_shots', 
    'for_avg_rebound_shots', 'opponent_avg_shots_on_goal_5on5', 'opponent_avg_shots_on_goal_all', 'opponent_avg_defender_shots',
    'opponent_avg_long_shots', 'opponent_avg_WRIST_shots', 'opponent_avg_SLAP_shots', 'opponent_avg_SNAP_shots',
    'opponent_avg_BACKHAND_shots', 'opponent_avg_TIP_shots', 'opponent_avg_rebound_shots'
]

season_averages = pd.DataFrame(columns=seasonAveragesColNames)

# get season averages by looping through each team
for team in teams:
    # get games where team is listed as home or away
    home_team_data = shotData[shotData['homeTeamCode'] == team]
    away_team_data = shotData[shotData['awayTeamCode'] == team]
    
    # get the 'for' statistics 
    total_shots_on_goal_5on5_for = home_team_data['homeTeamShotsOnGoal5on5'].sum() + away_team_data['awayTeamShotsOnGoal5on5'].sum()
    total_shots_on_goal_all_for = home_team_data['homeTeamShotsOnGoalAll'].sum() + away_team_data['awayTeamShotsOnGoalAll'].sum()
    total_defender_shots_for = home_team_data['homeDefenderShots'].sum() + away_team_data['awayDefenderShots'].sum()
    total_long_shots_for = home_team_data['homeLongShots'].sum() + away_team_data['awayLongShots'].sum()
    total_WRIST_shots_for = home_team_data['homeWRISTShots'].sum() + away_team_data['awayWRISTShots'].sum()
    total_SLAP_shots_for = home_team_data['homeSLAPShots'].sum() + away_team_data['awaySLAPShots'].sum()
    total_SNAP_shots_for = home_team_data['homeSNAPShots'].sum() + away_team_data['awaySNAPShots'].sum()
    total_BACKHAND_shots_for = home_team_data['homeBACKHANDShots'].sum() + away_team_data['awayBACKHANDShots'].sum()
    total_TIP_shots_for = home_team_data['homeTIPShots'].sum() + away_team_data['awayTIPShots'].sum()
    total_rebound_shots_for = home_team_data['homeReboundShots'].sum() + away_team_data['awayReboundShots'].sum()

    # get the opponent's statistics
    total_shots_on_goal_5on5_against = away_team_data['homeTeamShotsOnGoal5on5'].sum() + home_team_data['awayTeamShotsOnGoal5on5'].sum()
    total_shots_on_goal_all_against = away_team_data['homeTeamShotsOnGoalAll'].sum() + home_team_data['awayTeamShotsOnGoalAll'].sum()
    total_defender_shots_against = away_team_data['homeDefenderShots'].sum() + home_team_data['awayDefenderShots'].sum()
    total_long_shots_against = away_team_data['homeLongShots'].sum() + home_team_data['awayLongShots'].sum()
    total_WRIST_shots_against = away_team_data['homeWRISTShots'].sum() + home_team_data['awayWRISTShots'].sum()
    total_SLAP_shots_against = away_team_data['homeSLAPShots'].sum() + home_team_data['awaySLAPShots'].sum()
    total_SNAP_shots_against = away_team_data['homeSNAPShots'].sum() + home_team_data['awaySNAPShots'].sum()
    total_BACKHAND_shots_against = away_team_data['homeBACKHANDShots'].sum() + home_team_data['awayBACKHANDShots'].sum()
    total_TIP_shots_against = away_team_data['homeTIPShots'].sum() + home_team_data['awayTIPShots'].sum()
    total_rebound_shots_against = away_team_data['homeReboundShots'].sum() + home_team_data['awayReboundShots'].sum()

    # get average, 82 games per season
    avg_shots_on_goal_5on5_for = total_shots_on_goal_5on5_for / 82
    avg_shots_on_goal_all_for = total_shots_on_goal_all_for / 82
    avg_defender_shots_for = total_defender_shots_for / 82
    avg_long_shots_for = total_long_shots_for / 82
    avg_WRIST_shots_for = total_WRIST_shots_for / 82
    avg_SLAP_shots_for = total_SLAP_shots_for / 82
    avg_SNAP_shots_for = total_SNAP_shots_for / 82
    avg_BACKHAND_shots_for = total_BACKHAND_shots_for / 82
    avg_TIP_shots_for = total_TIP_shots_for / 82
    avg_rebound_shots_for = total_rebound_shots_for / 82

    avg_shots_on_goal_5on5_against = total_shots_on_goal_5on5_against / 82
    avg_shots_on_goal_all_against = total_shots_on_goal_all_against / 82
    avg_defender_shots_against = total_defender_shots_against / 82
    avg_long_shots_against = total_long_shots_against / 82
    avg_WRIST_shots_against = total_WRIST_shots_against / 82
    avg_SLAP_shots_against = total_SLAP_shots_against / 82
    avg_SNAP_shots_against = total_SNAP_shots_against / 82
    avg_BACKHAND_shots_against = total_BACKHAND_shots_against / 82
    avg_TIP_shots_against = total_TIP_shots_against / 82
    avg_rebound_shots_against = total_rebound_shots_against / 82

    # add to dataframe
    season_averages.loc[len(season_averages)] = [
        team,
        avg_shots_on_goal_5on5_for,
        avg_shots_on_goal_all_for,
        avg_defender_shots_for,
        avg_long_shots_for,
        avg_WRIST_shots_for,
        avg_SLAP_shots_for,
        avg_SNAP_shots_for,
        avg_BACKHAND_shots_for,
        avg_TIP_shots_for,
        avg_rebound_shots_for,
        avg_shots_on_goal_5on5_against,
        avg_shots_on_goal_all_against,
        avg_defender_shots_against,
        avg_long_shots_against,
        avg_WRIST_shots_against,
        avg_SLAP_shots_against,
        avg_SNAP_shots_against,
        avg_BACKHAND_shots_against,
        avg_TIP_shots_against,
        avg_rebound_shots_against
    ]

# sort alphabetically
season_averages = season_averages.sort_values(by='team', ascending=True)

# save csv
season_averages.to_csv('stage1and2-gatherAndCleanData/moneypuck/seasonAveragesByTeam.csv', index=False)


