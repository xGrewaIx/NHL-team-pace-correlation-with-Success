# HOW TO RUN:

### 1) run `python3 packages.py` to install required packages (pandas, numpy, sci-kit learn, matplotlib)

### 2) run `python3 run.py`, to scrape, generate data csv files, and ml models for visualizations

***

The following file is **not included** in the automated run file. Run manually if needed (it is pre-loaded for convenience due to the long run time):  

```bash
stage1and2-gatherAndCleanData/nhlAPI/5_v_5_game_by_game_api_scrape.py
```
***

Or, install packages and run files manually in this order:

packages: 
```
    pandas 
    numpy 
    scikit-learn
    matplotlib
```
files (in order of execution top to bottom):
```
    stage1and2-gatherAndCleanData/moneypuck/gatherVariablesFromMoneyPuckData.py &&
    stage1and2-gatherAndCleanData/moneypuck/seasonAvgMoneyPuckVariables.py &&
    stage1and2-gatherAndCleanData/nhlAPI/5_v_5_game_by_game_api_scrape.py &&
    stage1and2-gatherAndCleanData/nhlAPI/mergeNHLData.py &&
    stage3-analyzeData/moneyPuckCorrelations.py &&
    stage3-analyzeData/nhlCorrelations.py &&
    stage3-analyzeData/machine_learning.py

```
The files in stage1and2 either scrape NHL API or the included moneypuck files for data, then calculate season averages and merge all data. In stage3, correlations are calculated between variables and shots on net, and then `machine_learning.py` employs ml models to cluster teams beased on relationships found to be significant (and varying levels of correlation strength). 

### 3) After, you should expect these csv files:

in `stage1and2-gatherAndCleanData`:
    
   /moneypuck

   1)    `VariablesFromMoneyPuck.csv`: which  relevant data from the files in the `moneypuckData` folder
   2)    `seasonAveragesByTeam.csv`: which contains the average of the data above for each team throughout the 23-24 NHL regular season

   /nhlAPI
   
   1) `5v5nhl_faceoff_data.csv`, `5v5nhl_season_averages.csv`, `5v5nhl_shot_data.csv`, `merged5v5NHLData.csv`: contains 5 on 5 data scraped from NHL API
   2) `season_team_points.csv`: contains season points for 23-24 regular season NHL

in `stage3-analyzeData`:

   1) `awayStrongCorrelationMoneyPuck.csv`, `homeStrongCorrelationMoneyPuck.csv`: contains r and p values, among other stats, for the comparision between shots on net and shot on net subtypes from moneypuck data
   2) `awayStrongCorrelationNHL.csv`, `homeStrongCorrelationNHL.csv`: contains r and p values, among other stats, for the comparision between shots on net and categories such as faceoff win percentages and corsi/fenwick from NHL API data

in `stage4-results`:

   1) contains png of each clustering model, for each r-value threshold (0, 0.2, 0.4, 0.6)

