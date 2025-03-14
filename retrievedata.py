import requests
import pandas as pd

# Replace 'YOUR_API_KEY' with your actual API key
api_key = '9fd656462aa08abb461cb4e8a6167547'
base_url = 'https://v3.football.api-sports.io/'

# Set the headers with your API key
headers = {
    'x-apisports-key': api_key
}

# Function to fetch data from the API
def fetch_data(endpoint, params):
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    return response.json()

# Example: Fetch matches from the English Premier League (league ID: 39) for the 2023 season
params = {
    'league': 39,
    'season': 2023
}

# Fetch matches
matches = fetch_data('fixtures', params)

# Check if the request was successful
if matches['response']:
    # Extract relevant data
    data = []
    for match in matches['response']:
        match_data = {
            'match_id': match['fixture']['id'],
            'home_team': match['teams']['home']['name'],
            'away_team': match['teams']['away']['name'],
            'home_goals': match['goals']['home'],
            'away_goals': match['goals']['away'],
            'match_outcome': 'Win' if match['teams']['home']['winner'] else ('Draw' if match['goals']['home'] == match['goals']['away'] else 'Loss')
        }
        data.append(match_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv('matches.csv', index=False)
    print("Data saved to matches.csv")
else:
    print("No data found or an error occurred.")
