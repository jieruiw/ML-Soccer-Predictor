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

# Sort by Matchweek
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

# Calculate team form
def calculate_team_form(df, window=5):
    # Define weights
    weights = [2, 1.75, 1.5, 1.25, 1]

    def form_score(group):
        points = group['Result'].apply(lambda x: 3 if x == 'W' else 2 if x == 'D' else 1)
        form = points.shift().rolling(window, min_periods=1).apply(
            lambda x: sum(a * b for a, b in zip(x[::-1], weights[:len(x)])), raw=True
        )
        return form

    # Calculate Home Form and Away Form separately
    df['Home_Form'] = df[df['Venue'] == 'Home'].groupby('Team', group_keys=False).apply(form_score, include_groups=False)
    df['Away_Form'] = df[df['Venue'] == 'Away'].groupby('Team', group_keys=False).apply(form_score, include_groups=False)

    # Normalize form score out of 10
    max_score = sum([3 * w for w in weights])
    df['Home_Form'] = (df['Home_Form'] / max_score) * 10
    df['Away_Form'] = (df['Away_Form'] / max_score) * 10

    return df

combined_df = calculate_team_form(combined_df)



# Save the processed data
processed_data_path = os.path.join(data_directory, 'processed_combined_data.csv')
combined_df.to_csv(processed_data_path, index=False)
