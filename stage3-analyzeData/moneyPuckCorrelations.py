import pandas as pd
from scipy.stats import linregress

# load
df = pd.read_csv("stage1and2-gatherAndCleanData/moneypuck/VariablesFromMoneyPuck.csv")

# make a copy of the dataframe without non-relevant columns
df = df.drop(columns=["homeTeamShotsOnGoalAll", "awayTeamShotsOnGoalAll"])

# helper function to compare a target column (e.g., shots on goal) against other columns
def regression(target_col, columns, alpha=0.05):
    results = {}
    for col in columns:
        # get stats
        slope, intercept, rValue, pValue, std_err = linregress(df[target_col], df[col])
        # relationship type
        relationship = "positive" if rValue > 0 else "negative"
        # Add results to dictionary
        results[col] = {
            "slope": slope,
            "rValue": rValue,
            "pValue": pValue,
            "pValue_significant": "yes" if pValue < alpha else "no",
            "r_>_0.0": "yes" if rValue > 0 else "no",
            "r_>_0.2": "yes" if rValue > 0.2 else "no",
            "r_>_0.4": "yes" if rValue > 0.4 else "no",
            "r_>_0.6": "yes" if rValue > 0.6 else "no",
            "pos or neg relationship": relationship
        }
    return results

# define the target column for home and away team shots on goal (5-on-5)
home_target_col = "homeTeamShotsOnGoal5on5"
away_target_col = "awayTeamShotsOnGoal5on5"

# get home team columns to analyze
home_columns = [
    col for col in df.columns 
    if col.startswith("home") and col != home_target_col and pd.api.types.is_numeric_dtype(df[col])
]

# get away team columns to analyze
away_columns = [
    col for col in df.columns 
    if col.startswith("away") and col != away_target_col and pd.api.types.is_numeric_dtype(df[col])
]

# apply the regression helper function for home and away team data
home_results = regression(home_target_col, home_columns)
away_results = regression(away_target_col, away_columns)

# convert results to DataFrames and save them as CSV files
home_results_df = pd.DataFrame.from_dict(home_results, orient='index')
home_results_df.to_csv("stage3-analyzeData/homeStrongCorrelationMoneyPuck.csv", index_label="Column")

away_results_df = pd.DataFrame.from_dict(away_results, orient='index')
away_results_df.to_csv("stage3-analyzeData/awayStrongCorrelationMoneyPuck.csv", index_label="Column")