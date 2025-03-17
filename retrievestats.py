import requests
import pandas as pd
import time
import os

# API credentials
api_key = '43a8c8bc852b94f05370766b571c1069'
base_url = 'https://v3.football.api-sports.io/'

# Headers for API request
headers = {
    'x-apisports-key': api_key
}

# Function to fetch fixture statistics for both teams
def fetch_fixture_statistics(match_id, home_team, away_team):
    endpoint = 'fixtures/statistics'
    params = {'fixture': match_id}
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    data = response.json()

    if 'response' in data and data['response']:
        stats = {}
        
        for team_data in data['response']:
            team_name = team_data['team']['name']
            team_stats = {stat['type']: stat['value'] for stat in team_data['statistics']}
            
            if team_name == home_team:
                stats.update({
                    'Home_Ball_Possession': team_stats.get('Ball Possession', 'N/A'),
                    'Home_Pass_Accuracy': team_stats.get('Passes %', 'N/A'),
                    'Home_Total_Shots': team_stats.get('Total Shots', 'N/A'),
                    'Home_Expected_Goals': team_stats.get('expected_goals', 'N/A')
                })
            elif team_name == away_team:
                stats.update({
                    'Away_Ball_Possession': team_stats.get('Ball Possession', 'N/A'),
                    'Away_Pass_Accuracy': team_stats.get('Passes %', 'N/A'),
                    'Away_Total_Shots': team_stats.get('Total Shots', 'N/A'),
                    'Away_Expected_Goals': team_stats.get('expected_goals', 'N/A')
                })

        return stats
    return None

# Load existing matches.csv
df = pd.read_csv('matches.csv')

# Check if an expanded file already exists to resume progress
if os.path.exists('matches_expanded.csv'):
    df_expanded = pd.read_csv('matches_expanded.csv')
else:
    df_expanded = df.copy()
    df_expanded['Home_Ball_Possession'] = None
    df_expanded['Home_Pass_Accuracy'] = None
    df_expanded['Home_Total_Shots'] = None
    df_expanded['Home_Expected_Goals'] = None
    df_expanded['Away_Ball_Possession'] = None
    df_expanded['Away_Pass_Accuracy'] = None
    df_expanded['Away_Total_Shots'] = None
    df_expanded['Away_Expected_Goals'] = None

# Identify matches that still need data fetching
remaining_matches = df_expanded[df_expanded['Home_Ball_Possession'].isna()]
match_ids = remaining_matches[['match_id', 'home_team', 'away_team']].values.tolist()

# Process only 80 matches at a time
batch_size = 1
matches_to_process = match_ids[:batch_size]

print(f"Fetching statistics for {len(matches_to_process)} matches...")

# Iterate through the batch and fetch statistics
for match_id, home_team, away_team in matches_to_process:
    stats = fetch_fixture_statistics(match_id, home_team, away_team)
    print(stats)
    
    if stats:
        df_expanded.loc[df_expanded['match_id'] == match_id, 'Home_Ball_Possession'] = stats['Home_Ball_Possession']
        df_expanded.loc[df_expanded['match_id'] == match_id, 'Home_Pass_Accuracy'] = stats['Home_Pass_Accuracy']
        df_expanded.loc[df_expanded['match_id'] == match_id, 'Home_Total_Shots'] = stats['Home_Total_Shots']
        df_expanded.loc[df_expanded['match_id'] == match_id, 'Home_Expected_Goals'] = stats['Home_Expected_Goals']
        df_expanded.loc[df_expanded['match_id'] == match_id, 'Away_Ball_Possession'] = stats['Away_Ball_Possession']
        df_expanded.loc[df_expanded['match_id'] == match_id, 'Away_Pass_Accuracy'] = stats['Away_Pass_Accuracy']
        df_expanded.loc[df_expanded['match_id'] == match_id, 'Away_Total_Shots'] = stats['Away_Total_Shots']
        df_expanded.loc[df_expanded['match_id'] == match_id, 'Away_Expected_Goals'] = stats['Away_Expected_Goals']
    
    # Sleep to avoid hitting API rate limits
    time.sleep(3)  # Adjust based on API restrictions

# Save progress
df_expanded.to_csv('matches_expanded.csv', index=False)
print("Updated matches_expanded.csv with fixture statistics.")


