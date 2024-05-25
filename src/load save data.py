import pandas as pd
import os

team_ids = {
    "Arsenal": "18bb7c10",
    "Aston-Villa": "8602292d",
    "Bournemouth": "4ba7cbea",
    "Brentford": "cd051869",
    "Brighton-and-Hove-Albion": "d07537b9",
    "Burnley": "943e8050",
    "Chelsea": "cff3d9bb",
    "Crystal-Palace": "47c64c55",
    "Everton": "d3fd31cc",
    "Fulham": "fd962109",
    "Liverpool": "822bd0ba",
    "Luton-Town": "e297cd13",
    "Manchester-City": "b8fd03ef",
    "Manchester-United": "19538871",
    "Newcastle-United": "b2b47a98",
    "Nottingham-Forest": "e4a775cb",
    "Sheffield-United": "1df6b87e",
    "Tottenham-Hotspur": "361ca564",
    "West-Ham-United": "7c21e445",
    "Wolverhampton-Wanderers": "8cec06e1"

}

team_name_mapping = {
    "Arsenal": "Arsenal",
    "Aston Villa": "Aston-Villa",
    "Bournemouth": "Bournemouth",
    "Brentford": "Brentford",
    "Brighton and Hove Albion": "Brighton-and-Hove-Albion",
    "Burnley": "Burnley",
    "Chelsea": "Chelsea",
    "Crystal Palace": "Crystal-Palace",
    "Everton": "Everton",
    "Fulham": "Fulham",
    "Liverpool": "Liverpool",
    "Luton Town": "Luton-Town",
    "Manchester City": "Manchester-City",
    "Manchester United": "Manchester-United",
    "Newcastle United": "Newcastle-United",
    "Nott'ham Forest": "Nottingham-Forest",
    "Sheffield United": "Sheffield-United",
    "Tottenham Hotspur": "Tottenham-Hotspur",
    "West Ham United": "West-Ham-United",
    "Wolverhampton Wanderers": "Wolverhampton-Wanderers"
}


def process_gen_data(team_name, team_id):
    base_url = 'https://fbref.com/en/squads/{}/2023-2024/matchlogs/c9/schedule/{}-Scores-and-Fixtures-Premier-League'
    url = base_url.format(team_id, team_name)

    # Read the data from the URL
    df = pd.read_html(url, attrs={"id": "matchlogs_for"})[0]

    # Filter the columns
    df['Team'] = team_name
    gen_columns = ['Round', 'Team', 'Opponent', 'Result', 'Venue', 'GF', 'GA', 'xG', 'xGA', 'Poss']

    df = df[gen_columns]

    # Standardize team names
    df['Team'] = df['Team'].replace(team_name_mapping)
    df['Opponent'] = df['Opponent'].replace(team_name_mapping)

    # Create the data directory if it doesn't exist
    data_directory = '../data'
    os.makedirs(data_directory, exist_ok=True)

    # Create the file path and save the CSV
    file_path = os.path.join(data_directory, f'{team_name.lower().replace(" ", "_")}_gen.csv')
    df.to_csv(file_path, index=False)
    print(f"Saved data for {team_name} to {file_path}")


# Loop through each team and process its data
for team_name, team_id in team_ids.items():
    process_gen_data(team_name, team_id)

muShootingURL = 'https://fbref.com/en/squads/19538871/2023-2024/matchlogs/c9/shooting/Manchester-United-Match-Logs-Premier-League'
muPassingURL = 'https://fbref.com/en/squads/19538871/2023-2024/matchlogs/c9/passing/Manchester-United-Match-Logs-Premier-League'
muDefenceURL = 'https://fbref.com/en/squads/19538871/2023-2024/matchlogs/c9/defense/Manchester-United-Match-Logs-Premier-League'

muShootingDF = pd.read_html(muShootingURL, attrs={"id": "matchlogs_for"})[0]
muPassingDF = pd.read_html(muPassingURL, attrs={"id": "matchlogs_for"})[0]
muDefenceDF = pd.read_html(muDefenceURL, attrs={"id": "matchlogs_for"})[0]

muShootingDF.columns = muShootingDF.columns.get_level_values(1)
muPassingDF.columns = ['_'.join(col).strip() for col in muPassingDF.columns.values]
muDefenceDF.columns = ['_'.join(col).strip() for col in muDefenceDF.columns.values]

muPassingDF.rename(columns={'For Manchester United_Round': 'Round'}, inplace=True)
muDefenceDF.rename(
    columns={'For Manchester United_Round': 'Round', 'Tackles_Tkl': 'Tackles', 'Unnamed: 21_level_0_Int': 'Int'},
    inplace=True)

shooting_columns = ['Round', 'G/Sh', 'npxG/Sh']
passing_columns = ['Round', 'Total_Cmp%']
defence_columns = ['Round', 'Tackles', 'Int']

muShootingDF = muShootingDF[shooting_columns]
muPassingDF = muPassingDF[passing_columns]
muDefenceDF = muDefenceDF[defence_columns]

data_directory = '../data'
os.makedirs(data_directory, exist_ok=True)

muShootingPath = os.path.join(data_directory, 'mu_shooting.csv')
muPassingPath = os.path.join(data_directory, 'mu_passing.csv')
muDefencePath = os.path.join(data_directory, 'mu_defence.csv')

muShootingDF.to_csv(muShootingPath, index=False)
muPassingDF.to_csv(muPassingPath, index=False)
muDefenceDF.to_csv(muDefencePath, index=False)

print(f"Filtered DataFrames saved to data folder")
