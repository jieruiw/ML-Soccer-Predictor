import pandas as pd
import os
from glob import glob

# Load all team CSV files into a combined DataFrame
data_directory = '../data'
all_files = glob(os.path.join(data_directory, '*_gen.csv'))

dfs = []
for file in all_files:
    team_name = os.path.basename(file).split('-')[0]
    df = pd.read_csv(file)
    df['Team'] = team_name
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# Feature engineering
def add_rolling_features(df, window=3):
    df['Avg_GF'] = df.groupby('Team')['GF'].transform(lambda x: x.rolling(window).mean())
    df['Avg_GA'] = df.groupby('Team')['GA'].transform(lambda x: x.rolling(window).mean())
    df['Avg_xG'] = df.groupby('Team')['xG'].transform(lambda x: x.rolling(window).mean())
    df['Avg_xGA'] = df.groupby('Team')['xGA'].transform(lambda x: x.rolling(window).mean())
    df['Avg_Poss'] = df.groupby('Team')['Poss'].transform(lambda x: x.rolling(window).mean())
    return df

combined_df = add_rolling_features(combined_df)

# Label creation
def create_labels(df):
    df['Label'] = 0
    df.loc[df['Result'] == 'W', 'Label'] = 1
    df.loc[df['Result'] == 'L', 'Label'] = -1
    return df

combined_df = create_labels(combined_df)

# Save the processed data
processed_data_path = os.path.join(data_directory, 'processed_combined_data.csv')
combined_df.to_csv(processed_data_path, index=False)
