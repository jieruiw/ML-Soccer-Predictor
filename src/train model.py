import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

# Load the data
data_path = '../data/final_combined_df.csv'
df = pd.read_csv(data_path)

# Define features and target
features = [
    'Recent_GF_home', 'Recent_GA_home', 'Recent_xG_home', 'Recent_xGA_home', 'Recent_Poss_home', 'Form_home',
    'Recent_GF_away', 'Recent_GA_away', 'Recent_xG_away', 'Recent_xGA_away', 'Recent_Poss_away', 'Form_away'
]


X = df[features]
y = df['Label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=43)

# Debug: Check the shape of the training and test sets
print(f'Training set shape: {X_train.shape}')
print(f'Test set shape: {X_test.shape}')

# Train a multinomial logistic regression model
model = LogisticRegression(max_iter=3000, solver='lbfgs')
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy:.2f}')
print('Confusion Matrix:')
print(conf_matrix)
print('Classification Report:')
print(class_report)