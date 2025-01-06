import pandas as pd

#read data
df = pd.read_csv("cleanSaveData.csv")

# calculate avgShotsProjectedAgainst for each goalieTeam (average of opening line for each team)
# a higher value means more shots are projected to be taken against that team (weaker defence)
avgShotsProjectedAgainst = df.groupby('goalieTeam')['opening_line'].mean()

# calculate avgShotsProjectedFor for each team, using the opposite team opening_line
# a higher value means that a team is projected to take more shots
# look at goalie's team, and label the opening line as projection for other team
df['opposite_team'] = df.apply(lambda row: row['away_team'] if row['home_team'] == row['goalieTeam'] else row['home_team'], axis=1)
avgShotsProjectedFor = df.groupby('opposite_team')['opening_line'].mean()

# Combine the two DataFrames to create the result
result = pd.DataFrame({
    'team': avgShotsProjectedAgainst.index,
    'avgShotsProjectedAgainst': avgShotsProjectedAgainst.values
})

result['avgShotsProjectedFor'] = result['team'].map(avgShotsProjectedFor)

# Save the result to a new CSV file
result.to_csv('averagedShotProjection.csv', index=False)

result
