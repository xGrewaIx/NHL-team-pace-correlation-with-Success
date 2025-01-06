import pandas as pd

#https://pypi.org/project/Unidecode/
from unidecode import unidecode

#for ease of reference throughout the file, to approximately map game id between files
key = 'game_id'

# load first two datasets, data scraped from betting pros .com
events = pd.read_csv("events_data.csv")  # teams data
saves = pd.read_csv("goalie_saves_data.csv")  # goalie saves data

# merge files
merged = pd.merge(events, saves, on=['event_id'])

def main():
    
    #declare global so can be adjusted within main
    global merged
    #rename columns for consistancy 
    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html
    merged.rename(columns={'visitor_team': 'away_team', 'event_id': 'game_id'}, inplace=True)

    # apply unidecode to remove special characters
    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html
    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.applymap.html
    merged = merged.applymap(lambda x: unidecode(x) if isinstance(x, str) else x)

    # load starting goaltender data
    # this was scraped because when scraping data from betting pros, the current team for each goaltender represents the current team they play on (24-25) season, and not the team they played for in the game (23-24) season
    # this data will be used to reference the goaltender's team when the goalie played the game
    # this is done by finding the approx game id equivalent from the bettingpros data, then finding the game around that transformed game id. then, the goalie is cross referenced as the 'home goaltender' or 'away goaltender', which is then used to verify the team the goaltender played on
    startingGoalies = pd.read_csv("starting_goaltender_data.csv")

    # apply unidecode to startingGoalies to remove special characters
    startingGoalies = startingGoalies.applymap(lambda x: unidecode(x) if isinstance(x, str) else x)

    #get game id offset
    offset = offsetCalculation(merged, startingGoalies)

    # apply the getTeam function to each row and add the correctedTeam column
    merged['correctedTeam'] = merged.apply(lambda row: getTeam(row, startingGoalies, offset), axis=1)

    # check for game_id occurrences greater than 2
    # because somestimes bettingpros listed more than 1 goalie per team for a game, as goalies are sometimes a game time decision
    game_id_counts = merged.groupby('game_id').size()
    # Get game_ids with more than 2 occurrences  
    duplicate_game_ids = game_id_counts[game_id_counts > 2].index.tolist()  

    # remove rows where correctedTeam is empty and game_id is not part of duplicate game_id groups
    # sometimes betting pros listed the wrong goalie for the team (did not match up with starting goaltender data), so remove these data points that are not valid
    rows_with_empty_corrected_team = merged[merged['correctedTeam'].isna()]
    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isin.html#pandas.DataFrame.isin
    rows_with_empty_corrected_team_and_non_duplicate_game_id = rows_with_empty_corrected_team[~rows_with_empty_corrected_team['game_id'].isin(duplicate_game_ids)]

    # remove these rows from the merged DataFrame
    merged = merged[~merged.index.isin(rows_with_empty_corrected_team_and_non_duplicate_game_id.index)]

    # game_id groups with more than 2 occurrences, check if only one row has an empty correctedTeam
    # based on the way getTeam works, one of the goalies will not have a value for 'correctedTeam', because the goalie is not present in the starting goalie file
    # so, if only one goalie in a gameID with three or more entries, it means that goalie is useless data
    for game_id in duplicate_game_ids:
        game_id_rows = merged[merged['game_id'] == game_id]

        # check if only one row in the group has an empty correctedTeam
        empty_corrected_team_count = game_id_rows['correctedTeam'].isna().sum()
        if empty_corrected_team_count == 1:
            # remove
            row_to_remove = game_id_rows[game_id_rows['correctedTeam'].isna()].index
            merged = merged.drop(row_to_remove)

    #naCount = merged['correctedTeam'].isna().sum()
    #print(naCount)

    #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
    # drop team, replace with corrected team
    merged = merged.drop(columns='team')

    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html
    merged = merged.rename(columns={'correctedTeam' : 'goalieTeam'})

    # Save the cleaned DataFrame to a CSV file
    merged.to_csv("cleanSaveData.csv", index=False)

# problem: game id for starting goalie information (scraped from nhl api), and game id from betting pros data is not the same
# solution: calculate offset by finding difference between first gameid in one file with the other
# additional problem: transformation is not 1:1, as the order of games per day is not tracked the same
# solution: start from 10 games before (10 picked after trial and error)
def offsetCalculation(df1, df2):
    #get first gameid in df1
    gameID1 = df1[key].iloc[0]
    #get first gameid in df2
    gameID2 = df2[key].iloc[0]
    #return offset, account for not 1-1 tranformation with -10 to start 10 rows before
    return abs(gameID1 - gameID2) - 10

# helper func: goes through dataframe, and gets the correct team for the goalie (if the goalie is noted to be playing game in starting goalie file)
def getTeam(incorrectRow, correctRow, offset):
    #incorrectrow: rows from dataframe from bettingpros data (merged)
    homeTeam1 = incorrectRow['home_team']
    awayTeam1 = incorrectRow['away_team']
    goalieName = incorrectRow['goalie_name']

    #get gameId in starting goalie file, which is about 8758 + gameid from bettingpros
    transformedID = incorrectRow[key] + offset

    #get the final gameid, because chicago vs buffalo was postponed which pushed the game a day after, and made the gameid out of sync with the surrounding games 
    final_game_id = merged.iloc[-1]['game_id']  

    #if tranformed ID before start of file, start at first row 
    if transformedID < correctRow[key].iloc[0]:
        transformedID = correctRow[key].iloc[0]
    
    #if transformed ID is for chicago v buffalo game (postponed), jump to spot on file
    elif transformedID == final_game_id + offset:
        transformedID = 22230

    # make window: rows that make up the surrounding rows to the transformed gameID
    window = correctRow[(correctRow[key] >= transformedID) & (correctRow[key] <= transformedID + 25)]
    
    # find matching game in window 
    result = window[(window['home_team'] == homeTeam1) & (window['away_team'] == awayTeam1)]

    if result.empty:
        return []

    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iterrows.html#pandas.DataFrame.iterrows
    # check if the goalie is the home or away goalie for the game, return result and add that code as the goalie's "real" team
    for _, row in result.iterrows():
        if goalieName == row['home_goaltender']:
            return row['home_team']
        elif goalieName == row['away_goaltender']:
            return row['away_team']

if __name__ == "__main__":
    main()
