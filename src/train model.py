import pandas as pd

# Load the data
data_path = '../data/processed_combined_data.csv'
df = pd.read_csv(data_path)

# Remove rows with missing values
df = df.dropna()

# Create a match identifier
df['Match_ID'] = df.apply(lambda row: '-'.join(sorted([row['Team'], row['Opponent']]) + [str(row['Round'])]), axis=1)

# Split the dataframe into two: one for the home team and one for the away team
home_df = df[df['Venue'] == 'Home'].set_index('Match_ID')
away_df = df[df['Venue'] == 'Away'].set_index('Match_ID')

# Combine the home and away dataframes
combined_df = home_df.join(away_df, lsuffix='_home', rsuffix='_away')

# Debug: Check the shape of combined_df
print(f'Combined dataframe shape: {combined_df.shape}')
print(f'First few rows of combined dataframe:\n{combined_df.head()}')

# Define features and target
features = [
    'Avg_GF_home', 'Avg_GA_home', 'Avg_xG_home', 'Avg_xGA_home', 'Avg_Poss_home', 'Form_home',
    'Avg_GF_away', 'Avg_GA_away', 'Avg_xG_away', 'Avg_xGA_away', 'Avg_Poss_away', 'Form_away'
]
target = 'Label_home'  # Using the home team's label for prediction

# Drop rows with NaN values after merging
combined_df = combined_df.dropna()

# Save the final dataframe to a CSV file for inspection
combined_df.to_csv('../data/final_combined_df.csv')

# Debug: Check the shape after dropping NaNs
print(f'Shape after dropping NaNs: {combined_df.shape}')

X = combined_df[features]
y = combined_df[target]

# Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Debug: Check the shape of the training and test sets
print(f'Training set shape: {X_train.shape}')
print(f'Test set shape: {X_test.shape}')

# Train a logistic regression model
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=4000)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy:.2f}')
print('Confusion Matrix:')
print(conf_matrix)
print('Classification Report:')
print(class_report)