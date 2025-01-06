import pandas as pd
from scipy.stats import linregress

# load merged nhl api data
df = pd.read_csv("stage1and2-gatherAndCleanData/nhlAPI/merged5v5NHLData.csv")

# helper func which compares a target column (shots on goal), against other columns
def regression(target_col, columns, alpha=0.05):
    results = {}
    for col in columns:
        # get regression statistics
        slope, intercept, rValue, pValue, std_err = linregress(df[target_col], df[col])
        # determine the relationship type
        relationship = "positive" if rValue > 0 else "negative"
        # add results to dict
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

# get home team stats
home_columns = [
    col for col in df.columns 
    if (col.startswith("home") or col in ["corsi_home", "fenwick_home", "corsi_home_%", "fenwick_home_%"]) 
    and col != "home_shots_on_goal" 
    #https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
    and pd.to_numeric(df[col], errors='coerce').notna().all()
]


# get away team stats
away_columns = [
    col for col in df.columns 
    if (col.startswith("away") or col in ["corsi_away", "fenwick_away", "corsi_away_%", "fenwick_away_%"]) 
    and col != "away_shots_on_goal" 
    and pd.to_numeric(df[col], errors='coerce').notna().all()
]

# apply regression helper func
home_results = regression("home_shots_on_goal", home_columns)
away_results = regression("away_shots_on_goal", away_columns)

# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.from_dict.html
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
home_results_df = pd.DataFrame.from_dict(home_results, orient='index')
home_results_df.to_csv("stage3-analyzeData/homeStrongCorrelationNHL.csv", index_label="Column")

away_results_df = pd.DataFrame.from_dict(away_results, orient='index')
away_results_df.to_csv("stage3-analyzeData/awayStrongCorrelationNHL.csv", index_label="Column")
