import pandas as pd
import os

url = 'https://fbref.com/en/squads/19538871/2023-2024/matchlogs/c9/schedule/Manchester-United-Scores-and-Fixtures-Premier-League'
df = pd.read_html(url, attrs = {"id":"matchlogs_for"})


df = df[0]

columns_to_keep = ['Date', 'Round', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'xG', 'xGA', 'Poss']
filtered_df = df[columns_to_keep]

data_directory = '../data'
os.makedirs(data_directory, exist_ok=True)
csv_file_path = os.path.join(data_directory, 'manchester_united_match_logs.csv')

# Save the filtered DataFrame to a CSV file in the specified directory
filtered_df.to_csv(csv_file_path, index=False)

print(f"Filtered DataFrame saved to {csv_file_path}")