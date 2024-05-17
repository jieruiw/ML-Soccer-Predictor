import pandas as pd
import os

team_ids = {
    "Arsenal": "18bb7c10",
    "Aston-Villa": "8602292d",
    "Bournemouth": "4ba7cbea",
    "Brentford": "cd051869",
    "Brighton-and-Hove-Albion": "d07537b9",
    "Burnley": "943e8050",
    "Chelsea": "cff3d9bb"
}

muGenURL = 'https://fbref.com/en/squads/19538871/2023-2024/matchlogs/c9/schedule/Manchester-United-Scores-and-Fixtures-Premier-League'
mcGenURL = 'https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/schedule/Manchester-City-Scores-and-Fixtures-Premier-League'
arsGenURL = 'https://fbref.com/en/squads/18bb7c10/2023-2024/matchlogs/c9/schedule/Arsenal-Scores-and-Fixtures-Premier-League'
avGenURL = 'https://fbref.com/en/squads/8602292d/2023-2024/matchlogs/c9/schedule/Aston-Villa-Scores-and-Fixtures-Premier-League'
boGenURL = 'https://fbref.com/en/squads/4ba7cbea/2023-2024/matchlogs/c9/schedule/Bournemouth-Scores-and-Fixtures-Premier-League'
breGenURL = 'https://fbref.com/en/squads/cd051869/2023-2024/matchlogs/c9/schedule/Brentford-Scores-and-Fixtures-Premier-League'
bhGenURL = 'https://fbref.com/en/squads/d07537b9/2023-2024/matchlogs/c9/schedule/Brighton-and-Hove-Albion-Scores-and-Fixtures-Premier-League'
buGenURL = 'https://fbref.com/en/squads/943e8050/2023-2024/matchlogs/c9/schedule/Burnley-Scores-and-Fixtures-Premier-League'
chGenURL = 'https://fbref.com/en/squads/cff3d9bb/2023-2024/matchlogs/c9/schedule/Chelsea-Scores-and-Fixtures-Premier-League'

muShootingURL = 'https://fbref.com/en/squads/19538871/2023-2024/matchlogs/c9/shooting/Manchester-United-Match-Logs-Premier-League'
muPassingURL = 'https://fbref.com/en/squads/19538871/2023-2024/matchlogs/c9/passing/Manchester-United-Match-Logs-Premier-League'
muDefenceURL = 'https://fbref.com/en/squads/19538871/2023-2024/matchlogs/c9/defense/Manchester-United-Match-Logs-Premier-League'


muGenDF = pd.read_html(muGenURL, attrs={"id": "matchlogs_for"})[0]
mcGenDF = pd.read_html(mcGenURL, attrs={"id": "matchlogs_for"})[0]
arsGenDF = pd.read_html(arsGenURL, attrs={"id": "matchlogs_for"})[0]
avGenDF = pd.read_html(avGenURL, attrs={"id": "matchlogs_for"})[0]
boGenDF = pd.read_html(boGenURL, attrs={"id": "matchlogs_for"})[0]
breGenDF = pd.read_html(breGenURL, attrs={"id": "matchlogs_for"})[0]
bhGenDF = pd.read_html(bhGenURL, attrs={"id": "matchlogs_for"})[0]
buGenDF = pd.read_html(buGenURL, attrs={"id": "matchlogs_for"})[0]
chGenDF = pd.read_html(chGenURL, attrs={"id": "matchlogs_for"})[0]


muShootingDF = pd.read_html(muShootingURL, attrs={"id": "matchlogs_for"})[0]
muPassingDF = pd.read_html(muPassingURL, attrs={"id": "matchlogs_for"})[0]
muDefenceDF = pd.read_html(muDefenceURL, attrs={"id": "matchlogs_for"})[0]





muShootingDF.columns = muShootingDF.columns.get_level_values(1)
muPassingDF.columns = ['_'.join(col).strip() for col in muPassingDF.columns.values]
muDefenceDF.columns = ['_'.join(col).strip() for col in muDefenceDF.columns.values]

muPassingDF.rename(columns={'For Manchester United_Round': 'Round'}, inplace = True)
muDefenceDF.rename(columns={'For Manchester United_Round': 'Round', 'Tackles_Tkl': 'Tackles', 'Unnamed: 21_level_0_Int':'Int'}, inplace = True)

gen_columns = ['Round', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'xG', 'xGA', 'Poss']
shooting_columns = ['Round', 'G/Sh', 'npxG/Sh']
passing_columns = ['Round', 'Total_Cmp%']
defence_columns = ['Round', 'Tackles', 'Int']

muGenDF = muGenDF[gen_columns]
mcGenDF = mcGenDF[gen_columns]
arsGenDF = arsGenDF[gen_columns]
avGenDF = avGenDF[gen_columns]
boGenDF = boGenDF[gen_columns]
breGenDF = breGenDF[gen_columns]
bhGenDF = bhGenDF[gen_columns]
buGenDF = buGenDF[gen_columns]
chGenDF = chGenDF[gen_columns]


muShootingDF = muShootingDF[shooting_columns]
muPassingDF = muPassingDF[passing_columns]
muDefenceDF = muDefenceDF[defence_columns]


data_directory = '../data'
os.makedirs(data_directory, exist_ok=True)

muGenPath = os.path.join(data_directory, 'mu_gen.csv')
mcGenPath = os.path.join(data_directory, 'mc_gen.csv')
arsGenPath = os.path.join(data_directory, 'ars_gen.csv')
avGenPath = os.path.join(data_directory, 'av_gen.csv')
boGenPath = os.path.join(data_directory, 'bo_gen.csv')
breGenPath = os.path.join(data_directory, 'bre_gen.csv')
bhGenPath = os.path.join(data_directory, 'bh_gen.csv')
buGenPath = os.path.join(data_directory, 'bu_gen.csv')
chGenPath = os.path.join(data_directory, 'ch_gen.csv')

muShootingPath = os.path.join(data_directory, 'mu_shooting.csv')
muPassingPath = os.path.join(data_directory, 'mu_passing.csv')
muDefencePath = os.path.join(data_directory, 'mu_defence.csv')

muGenDF.to_csv(muGenPath, index=False)
mcGenDF.to_csv(mcGenPath, index=False)
arsGenDF.to_csv(arsGenPath, index=False)
avGenDF.to_csv(avGenPath, index=False)
boGenDF.to_csv(boGenPath, index=False)
breGenDF.to_csv(breGenPath, index=False)
bhGenDF.to_csv(bhGenPath, index=False)
buGenDF.to_csv(buGenPath, index=False)
chGenDF.to_csv(chGenPath, index=False)

muShootingDF.to_csv(muShootingPath, index=False)
muPassingDF.to_csv(muPassingPath, index=False)
muDefenceDF.to_csv(muDefencePath, index=False)

print(f"Filtered DataFrames saved to data folder")
