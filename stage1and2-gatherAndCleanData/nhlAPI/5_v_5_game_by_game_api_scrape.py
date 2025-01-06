import numpy as np
import pandas as pd

# https://requests.readthedocs.io/en/latest/
import requests as req

# https://www.programiz.com/python-programming/examples/elapsed-time

import time


# from https://stackoverflow.com/questions/34512646/how-to-speed-up-api-requests
# Use this library to speed up requests
from multiprocessing import Pool


# using the below 2 links we scrape shot data for each game in the 2023-24 season
# https://github.com/Zmalski/NHL-API-Reference?tab=readme-ov-file#get-play-by-play
# https://gitlab.com/dword4/nhlapi/-/blob/master/new-api.md?ref_type=heads

# from https://en.wikipedia.org/wiki/Season_structure_of_the_NHL
# there are 1,312 games in a season

# iterate through games 1 through 1312
# url is f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play"

# get the game data

def get_game_data(game_id):
    r = req.get(f"https://api-web.nhle.com/v1/gamecenter/{game_id}/play-by-play")
    
    # use .json(), the built in json decoder
    data = r.json()
    
    # print(data.keys()) We want the plays key
    return data

def get_shot_data(game_data):
    
    shot_counts = {
        'home-shot-on-goal': 0,
        'home-missed-shot': 0,
        'home-blocked-shot': 0,
        'home-goal': 0,
        'away-shot-on-goal': 0,
        'away-missed-shot': 0,
        'away-blocked-shot': 0,
        'away-goal': 0
    }

    
    # https://www.w3schools.com/python/ref_dictionary_get.asp
    # https://docs.python.org/3/library/stdtypes.html#dict.get
    home_team_abbr = game_data.get('homeTeam').get('abbrev')
    home_team_id = game_data.get('homeTeam').get('id')
    
    away_team_abbr = game_data.get('awayTeam').get('abbrev')
    away_team_id = game_data.get('awayTeam').get('id')
    # print(home_team_id, away_team_id)
    
    
    plays = game_data.get('plays')
    
    for play in plays:
        
        typeDescKey = play.get('typeDescKey')
        situationCode = play.get('situationCode')
        
        if typeDescKey in ['shot-on-goal', 'missed-shot', 'blocked-shot', 'goal'] and situationCode == '1551':
            
            event_owner_team_id = play.get('details').get('eventOwnerTeamId')
            
            if event_owner_team_id == home_team_id:
                shot_counts[f'home-{typeDescKey}'] += 1
            elif event_owner_team_id == away_team_id:
                shot_counts[f'away-{typeDescKey}'] += 1
    
    # create a dictionary with all the data
        shot_data = {
            'game_id': game_data.get('id'),
            'home_team': home_team_abbr,
            'away_team': away_team_abbr,
            'home_shot_on_goal': shot_counts['home-shot-on-goal'],
            'away_shot_on_goal': shot_counts['away-shot-on-goal'],
            'home_missed_shot': shot_counts['home-missed-shot'],
            'away_missed_shot': shot_counts['away-missed-shot'],
            'home_blocked_shot': shot_counts['home-blocked-shot'],
            'away_blocked_shot': shot_counts['away-blocked-shot'],
            'home_goal': shot_counts['home-goal'],
            'away_goal': shot_counts['away-goal']
        }
    
    # print(shot_data)
    
    return shot_data

def get_faceoff_data(game_data):
    
    faceoff_counts = {
        'home_o_zone_win': 0,
        'home_d_zone_win': 0,
        'home_n_zone_win': 0,
        'home_o_zone_loss': 0,
        'home_d_zone_loss': 0,
        'home_n_zone_loss': 0,
        'away_o_zone_win': 0,
        'away_d_zone_win': 0,
        'away_n_zone_win': 0,
        'away_o_zone_loss': 0,
        'away_d_zone_loss': 0,
        'away_n_zone_loss': 0
    }
    
    home_team_abbr = game_data.get('homeTeam').get('abbrev')
    home_team_id = game_data.get('homeTeam').get('id')
    
    away_team_abbr = game_data.get('awayTeam').get('abbrev')
    away_team_id = game_data.get('awayTeam').get('id')
    # print(home_team_id, away_team_id)
    
    
    plays = game_data.get('plays')
    
    for play in plays:
        
        typeDescKey = play.get('typeDescKey')
        situationCode = play.get('situationCode')

        
        if typeDescKey == 'faceoff' and situationCode == '1551':
            details = play.get('details', {})
            event_owner_team_id = details.get('eventOwnerTeamId')
            zone_code = details.get('zoneCode')
            
            if event_owner_team_id == home_team_id:
                # Home team wins faceoff
                if zone_code == 'O':
                    faceoff_counts['home_o_zone_win'] += 1
                elif zone_code == 'D':
                    faceoff_counts['home_d_zone_win'] += 1
                elif zone_code == 'N':
                    faceoff_counts['home_n_zone_win'] += 1
                
                # Away team loses faceoff
                if zone_code == 'O':
                    faceoff_counts['away_d_zone_loss'] += 1
                elif zone_code == 'D':
                    faceoff_counts['away_o_zone_loss'] += 1
                elif zone_code == 'N':
                    faceoff_counts['away_n_zone_loss'] += 1
            
            elif event_owner_team_id == away_team_id:
                # Away team wins faceoff
                if zone_code == 'O':
                    faceoff_counts['away_o_zone_win'] += 1
                elif zone_code == 'D':
                    faceoff_counts['away_d_zone_win'] += 1
                elif zone_code == 'N':
                    faceoff_counts['away_n_zone_win'] += 1
                
                # Home team loses faceoff
                if zone_code == 'O':
                    faceoff_counts['home_d_zone_loss'] += 1
                elif zone_code == 'D':
                    faceoff_counts['home_o_zone_loss'] += 1
                elif zone_code == 'N':
                    faceoff_counts['home_n_zone_loss'] += 1
                    
        faceoff_data = {
            'game_id': game_data.get('id'),
            'home_team': home_team_abbr,
            'away_team': away_team_abbr,
            'home_o_zone_win': faceoff_counts['home_o_zone_win'],
            'home_d_zone_win': faceoff_counts['home_d_zone_win'],
            'home_n_zone_win': faceoff_counts['home_n_zone_win'],
            'home_o_zone_loss': faceoff_counts['home_o_zone_loss'],
            'home_d_zone_loss': faceoff_counts['home_d_zone_loss'],
            'home_n_zone_loss': faceoff_counts['home_n_zone_loss'],
            'away_o_zone_win': faceoff_counts['away_o_zone_win'],
            'away_d_zone_win': faceoff_counts['away_d_zone_win'],
            'away_n_zone_win': faceoff_counts['away_n_zone_win'],
            'away_o_zone_loss': faceoff_counts['away_o_zone_loss'],
            'away_d_zone_loss': faceoff_counts['away_d_zone_loss'],
            'away_n_zone_loss': faceoff_counts['away_n_zone_loss']
        }

    return faceoff_data
    

def get_game(game_id):
    # print(f"Getting data for game {game_id}")
    game_data = get_game_data(game_id)
    
    shot_data = get_shot_data(game_data)
    faceoff_data = get_faceoff_data(game_data)

    return shot_data, faceoff_data


def main():
    # https://api-web.nhle.com/v1/gamecenter/2023020001/play-by-play
    start = time.time()
    
    game_ids = range(2023020001, 2023021313)
    
    # testing with 6 games
    # game_ids = range(2023020001, 2023020007)


    # from https://stackoverflow.com/questions/34512646/how-to-speed-up-api-requests
    # https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool
    # ask greg baker what the the processes=20 does and how this speeds up the code
    with Pool(processes=20) as pool:
        all_shot_data = pool.map(get_game, game_ids)

    shot_data = [data[0] for data in all_shot_data]
    shot_data = pd.DataFrame(shot_data)
    # print(shot_data.head())
    
    faceoff_data = [data[1] for data in all_shot_data]
    faceoff_data = pd.DataFrame(faceoff_data)
    # print(faceoff_data.head())
    
    # Calculate additional metrics
    shot_data['home_shots_on_goal'] = shot_data['home_shot_on_goal'] + shot_data['home_goal']
    shot_data['away_shots_on_goal'] = shot_data['away_shot_on_goal'] + shot_data['away_goal']
    
    shot_data['corsi_home'] = shot_data['home_shots_on_goal'] + shot_data['home_missed_shot'] + shot_data['home_blocked_shot']
    shot_data['corsi_away'] = shot_data['away_shots_on_goal'] + shot_data['away_missed_shot'] + shot_data['away_blocked_shot']
    
    shot_data['corsi_home_%'] = shot_data['corsi_home'] / (shot_data['corsi_home'] + shot_data['corsi_away'])
    shot_data['corsi_away_%'] = shot_data['corsi_away'] / (shot_data['corsi_home'] + shot_data['corsi_away'])
    
    shot_data['fenwick_home'] = shot_data['home_shots_on_goal'] + shot_data['home_missed_shot']
    shot_data['fenwick_away'] = shot_data['away_shots_on_goal'] + shot_data['away_missed_shot']
    
    shot_data['fenwick_home_%'] = shot_data['fenwick_home'] / (shot_data['fenwick_home'] + shot_data['fenwick_away'])
    shot_data['fenwick_away_%'] = shot_data['fenwick_away'] / (shot_data['fenwick_home'] + shot_data['fenwick_away'])
    
    # Display only specific columns
    cleaned_columns = [
        'game_id', 'home_team', 'away_team', 'home_shots_on_goal', 'away_shots_on_goal',
        'corsi_home', 'corsi_away', 'fenwick_home', 'fenwick_away', 'corsi_home_%', 'corsi_away_%',
        'fenwick_home_%', 'fenwick_away_%'
    ]
    
    shot_data = shot_data[cleaned_columns]
    
    # Calculate faceoff percentages
    faceoff_data['home_o_zone_faceoff_pct'] = faceoff_data['home_o_zone_win'] / (faceoff_data['home_o_zone_win'] + faceoff_data['home_o_zone_loss'])
    faceoff_data['home_d_zone_faceoff_pct'] = faceoff_data['home_d_zone_win'] / (faceoff_data['home_d_zone_win'] + faceoff_data['home_d_zone_loss'])
    faceoff_data['home_n_zone_faceoff_pct'] = faceoff_data['home_n_zone_win'] / (faceoff_data['home_n_zone_win'] + faceoff_data['home_n_zone_loss'])
    
    faceoff_data['away_o_zone_faceoff_pct'] = faceoff_data['away_o_zone_win'] / (faceoff_data['away_o_zone_win'] + faceoff_data['away_o_zone_loss'])
    faceoff_data['away_d_zone_faceoff_pct'] = faceoff_data['away_d_zone_win'] / (faceoff_data['away_d_zone_win'] + faceoff_data['away_d_zone_loss'])
    faceoff_data['away_n_zone_faceoff_pct'] = faceoff_data['away_n_zone_win'] / (faceoff_data['away_n_zone_win'] + faceoff_data['away_n_zone_loss'])
    
    # Display only specific columns for faceoff data
    faceoff_cleaned_columns = [
        'game_id', 'home_team', 'away_team', 'home_o_zone_faceoff_pct', 'home_d_zone_faceoff_pct', 'home_n_zone_faceoff_pct',
        'away_o_zone_faceoff_pct', 'away_d_zone_faceoff_pct', 'away_n_zone_faceoff_pct'
    ]
    
    faceoff_data = faceoff_data[faceoff_cleaned_columns]
    
    
    # Get season averages for each team
    # https://www.statology.org/pandas-unique-values-in-column/
    # get an array of all 32 team abbreviations
    team_abbr = shot_data.home_team.unique()
    # print(team_abbr)
    # print(team_abbr.shape)
    
    # create a data frame to store the season averages and give columns names
    season_averages_col_names = ['team', 'avg_shots_on_goal', 'corsi', 'fenwick', 'corsi_%', 'fenwick_%', 'o_zone_faceoff_%', 'd_zone_faceoff_%', 'n_zone_faceoff_%']
    season_averages = pd.DataFrame(columns=season_averages_col_names)
    # print(season_averages)
    
    # Using team abbreviations check for home and away team and calculate the season averages
    # from: https://www.geeksforgeeks.org/how-to-add-one-row-in-an-existing-pandas-dataframe/
    # https://saturncloud.io/blog/how-to-insert-a-row-to-pandas-dataframe/#:~:text=Using%20loc%20method&text=Using%20df.,index%20for%20the%20new%20row.
    # insert new row using loc method df.loc[len(df)] = new_row
    for team in team_abbr:
        # Home and away data filtering for the current team
        # Filter data for the current team
        home_team_data = shot_data[shot_data['home_team'] == team]
        away_team_data = shot_data[shot_data['away_team'] == team]
    
        # Calculate season totals for shots, Corsi, and Fenwick
        total_shots_on_goal = home_team_data['home_shots_on_goal'].sum() + away_team_data['away_shots_on_goal'].sum()
        total_corsi = home_team_data['corsi_home'].sum() + away_team_data['corsi_away'].sum()
        total_fenwick = home_team_data['fenwick_home'].sum() + away_team_data['fenwick_away'].sum()
    
        # Calculate season percentages for Corsi and Fenwick
        corsi_total_for_and_against = total_corsi + (home_team_data['corsi_away'].sum() + away_team_data['corsi_home'].sum())
        fenwick_total_for_and_against = total_fenwick + (home_team_data['fenwick_away'].sum() + away_team_data['fenwick_home'].sum())
    
        corsi_perc = total_corsi / corsi_total_for_and_against 
        fenwick_perc = total_fenwick / fenwick_total_for_and_against 
    
        # Faceoff data for the team
        home_team_faceoff_data = faceoff_data[faceoff_data['home_team'] == team]
        away_team_faceoff_data = faceoff_data[faceoff_data['away_team'] == team]
    
        # Calculate average faceoff percentages (season totals divided by 82 games)
        # https://www.indeed.com/career-advice/career-development/how-to-calculate-average-percentage#:~:text=The%20formula%20to%20calculate%20average,more%20percentages%20of%20a%20whole.
        # sample size is the 82 games 
        o_zone_faceoff_perc = (
            home_team_faceoff_data['home_o_zone_faceoff_pct'].sum() +
            away_team_faceoff_data['away_o_zone_faceoff_pct'].sum()
        ) / 82
        d_zone_faceoff_perc = (
            home_team_faceoff_data['home_d_zone_faceoff_pct'].sum() +
            away_team_faceoff_data['away_d_zone_faceoff_pct'].sum()
        ) / 82
        n_zone_faceoff_perc = (
            home_team_faceoff_data['home_n_zone_faceoff_pct'].sum() +
            away_team_faceoff_data['away_n_zone_faceoff_pct'].sum()
        ) / 82
    
        # Calculate average shots on goal per game
        avg_shots_on_goal = total_shots_on_goal / 82
    
        # Add calculated values to the dataframe
        season_averages.loc[len(season_averages)] = [
        team,
        avg_shots_on_goal,
        total_corsi / 82,
        total_fenwick / 82,
        corsi_perc,
        fenwick_perc,
        o_zone_faceoff_perc,
        d_zone_faceoff_perc,
        n_zone_faceoff_perc
        ]
    
    # print(season_averages)
    
    end = time.time()
    
    # print(f"Time taken: {end - start}")
    
    # print(shot_data.head())
    # print(faceoff_data.head())
    
    shot_data.to_csv('stage1and2-gatherAndCleanData/nhlAPI/5v5nhl_shot_data.csv', index=False)
    faceoff_data.to_csv('stage1and2-gatherAndCleanData/nhlAPI/5v5nhl_faceoff_data.csv', index=False)
    season_averages.to_csv('stage1and2-gatherAndCleanData/nhlAPI/5v5nhl_season_averages.csv', index=False)
    
    

    

if __name__ == "__main__":
    main()
    
