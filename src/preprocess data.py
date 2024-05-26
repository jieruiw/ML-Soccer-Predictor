import pandas as pd
import os
from glob import glob

data_directory = '../data'
all_files = glob(os.path.join(data_directory, '*_gen.csv'))

dfs = []
for file in all_files:
    team_name = os.path.basename(file).split('-')[0]
    df = pd.read_csv(file)
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

# Sort by Matchweek and Team
combined_df['Round'] = combined_df['Round'].str.extract('(\d+)').astype(int)
combined_df = combined_df.sort_values(by=['Round', 'Team'])


# Feature engineering
def add_rolling_features(df, window=3):
    df['Avg_GF'] = df.groupby('Team')['GF'].transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    df['Avg_GA'] = df.groupby('Team')['GA'].transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    df['Avg_xG'] = df.groupby('Team')['xG'].transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    df['Avg_xGA'] = df.groupby('Team')['xGA'].transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    df['Avg_Poss'] = df.groupby('Team')['Poss'].transform(lambda x: x.shift(1).rolling(window, min_periods=1).mean())
    return df


combined_df = add_rolling_features(combined_df)


# Label creation
def create_labels(df):
    df['Label'] = 0
    df.loc[df['Result'] == 'W', 'Label'] = 1
    df.loc[df['Result'] == 'L', 'Label'] = -1
    return df


combined_df = create_labels(combined_df)


# Add form feature
def calculate_form(df):
    def form_points(result):
        if result == 'W':
            return 3
        elif result == 'D':
            return 2
        elif result == 'L':
            return 1
        return 0

    df['Form_Points'] = df['Result'].apply(form_points)

    weights = [1.5, 1.25, 1.0]

    def weighted_form(group):
        form = (
            group.shift(1).rolling(3, min_periods=1).apply(
                lambda x: sum(a * b for a, b in zip(x[::-1], weights[:len(x)])), raw=True)
        )
        form = form / 11.25 * 10  # Normalize to be out of 10
        return form

    df['Form'] = df.groupby('Team')['Form_Points'].transform(weighted_form)
    df.drop(columns=['Form_Points'], inplace=True)
    return df


combined_df = calculate_form(combined_df)

# Create a unique match identifier for home and away matches separately
combined_df['Match_ID'] = combined_df.apply(
    lambda row: f"{row['Round']}-{row['Team'].replace(' ', '_')}-{row['Opponent'].replace(' ', '_')}", axis=1)
combined_df['Opponent_Match_ID'] = combined_df.apply(
    lambda row: f"{row['Round']}-{row['Opponent'].replace(' ', '_')}-{row['Team'].replace(' ', '_')}", axis=1)

# Split the dataframe into home and away dataframes
home_df = combined_df[combined_df['Venue'] == 'Home'].set_index('Match_ID')
away_df = combined_df[combined_df['Venue'] == 'Away'].set_index('Opponent_Match_ID')

# Join home and away dataframes on their unique match identifiers
combined_df = home_df.join(away_df, lsuffix='_home', rsuffix='_away', how='inner')

# Adjust target to reflect three possible outcomes: 1 (home win), 0 (draw), -1 (away win)
combined_df['Label'] = combined_df['Label_home']
combined_df['Label'] = combined_df.apply(
    lambda row: 0 if row['Label_home'] == 0 and row['Label_away'] == 0 else row['Label'], axis=1
)

# Drop rows with NaN values after merging
combined_df = combined_df.dropna()

# Define features and target
features = [
    'Avg_GF_home', 'Avg_GA_home', 'Avg_xG_home', 'Avg_xGA_home', 'Avg_Poss_home', 'Form_home',
    'Avg_GF_away', 'Avg_GA_away', 'Avg_xG_away', 'Avg_xGA_away', 'Avg_Poss_away', 'Form_away'
]

# Save the final dataframe to a CSV file for inspection
combined_df.to_csv('../data/final_combined_df.csv')
