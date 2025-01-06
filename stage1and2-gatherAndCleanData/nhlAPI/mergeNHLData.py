import pandas as pd

# load files to merge
faceoffData = pd.read_csv("stage1and2-gatherAndCleanData/nhlAPI/5v5nhl_faceoff_data.csv")  # First dataset
shotData = pd.read_csv("stage1and2-gatherAndCleanData/nhlAPI/5v5nhl_shot_data.csv")      # Second dataset

# merge on game_id, removing duplicate caegories'home_team' and 'away_team'
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html
merged_data = pd.merge(
    faceoffData.drop(columns=["home_team", "away_team"]),  # Drop duplicate columns
    shotData,
    on="game_id"
)

# csv
merged_data.to_csv("stage1and2-gatherAndCleanData/nhlAPI/merged5v5NHLData.csv", index=False)

