import pandas as pd

# Load matches_expanded.csv
df = pd.read_csv('copymatches.csv')

# Ensure match outcomes are correctly labeled
win_label = "Win"  # Adjust if necessary based on dataset

# Initialize new columns
df['Last_5_Home_Wins'] = 0
df['Last_5_Away_Wins'] = 0

# Dictionary to track last 5 home/away results for each team
home_form_tracker = {}  # {team_name: [last 5 home results]}
away_form_tracker = {}  # {team_name: [last 5 away results]}

# Iterate through matches (since they are already in order)
for index, row in df.iterrows():
    home_team = row['home_team']
    away_team = row['away_team']
    match_outcome = row['match_outcome']

    # Track home form
    home_results = home_form_tracker.get(home_team, [])
    if match_outcome == win_label:  # Home team won
        home_results.append(1)
    else:
        home_results.append(0)
    if len(home_results) > 5:
        home_results.pop(0)  # Keep only last 5 results
    home_form_tracker[home_team] = home_results
    df.at[index, 'Last_5_Home_Wins'] = sum(home_results)  # Count home wins in last 5

    # Track away form
    away_results = away_form_tracker.get(away_team, [])
    if match_outcome == "Loss":  # Home team lost, so away team won
        away_results.append(1)
    else:
        away_results.append(0)
    if len(away_results) > 5:
        away_results.pop(0)  # Keep only last 5 results
    away_form_tracker[away_team] = away_results
    df.at[index, 'Last_5_Away_Wins'] = sum(away_results)  # Count away wins in last 5

# Save the updated dataset
df.to_csv('copymatches.csv', index=False)
print("Updated matches_expanded.csv with home and away form.")