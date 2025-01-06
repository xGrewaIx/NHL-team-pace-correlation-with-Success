#https://docs.python.org/3/library/subprocess.html

import subprocess

# get files to run in sequence

#not included: stage1and2-gatherAndCleanData/nhlAPI/5_v_5_game_by_game_api_scrape.py, stage1and2-gatherAndCleanData/nhlAPI/all_sit_game_by_game_api_scrape.py
files = [
    "stage1and2-gatherAndCleanData/moneypuck/gatherVariablesFromMoneyPuckData.py",
    "stage1and2-gatherAndCleanData/moneypuck/seasonAvgMoneyPuckVariables.py",
    "stage1and2-gatherAndCleanData/nhlAPI/mergeNHLData.py",
    "stage3-analyzeData/moneyPuckCorrelations.py",
    "stage3-analyzeData/nhlCorrelations.py",
    "stage3-analyzeData/machine_learning.py"
]

# Run each script
for file in files:
    try:
        subprocess.run(["python3", file], check=True)
    except subprocess.CalledProcessError as e:
        print('error')
        break