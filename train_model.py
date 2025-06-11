import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load dataset
df = pd.read_csv("mexican_medical_students_mental_health_data.csv")

# Compute scores based on question groups
df['Depression'] = df[[f'phq{i}' for i in range(1, 10)]].sum(axis=1)
df['Anxiety'] = df[[f'gad{i}' for i in range(1, 8)]].sum(axis=1)
df['Stress'] = df[[f'epw{i}' for i in range(1, 9)]].sum(axis=1)

# Define target labels
def get_depression_level(score):
    if score < 5:
        return "Minimal"
    elif score < 10:
        return "Mild"
    elif score < 15:
        return "Moderate"
    elif score < 20:
        return "Moderately Severe"
    else:
        return "Severe"

def get_anxiety_level(score):
    if score < 5:
        return "Minimal"
    elif score < 10:
        return "Mild"
    elif score < 15:
        return "Moderate"
    else:
        return "Severe"

def get_stress_level(score):
    if score < 10:
        return "Low"
    elif score < 20:
        return "Moderate"
    else:
        return "High"

# Apply label mappings
df['Depression_Level'] = df['Depression'].apply(get_depression_level)
df['Anxiety_Level'] = df['Anxiety'].apply(get_anxiety_level)
df['Stress_Level'] = df['Stress'].apply(get_stress_level)

# Features to use for prediction (you can choose more if needed)
features = ['phq1','phq2','phq3','phq4','phq5','phq6','phq7','phq8','phq9',
            'gad1','gad2','gad3','gad4','gad5','gad6','gad7',
            'epw1','epw2','epw3','epw4','epw5','epw6','epw7','epw8']

X = df[features]

# Train Depression Model
y_dep = df['Depression_Level']
X_train_dep, X_test_dep, y_train_dep, y_test_dep = train_test_split(X, y_dep, test_size=0.2, random_state=42)
dep_model = RandomForestClassifier()
dep_model.fit(X_train_dep, y_train_dep)
pickle.dump(dep_model, open("depression_model.pkl", "wb"))

# Train Anxiety Model
y_anx = df['Anxiety_Level']
X_train_anx, X_test_anx, y_train_anx, y_test_anx = train_test_split(X, y_anx, test_size=0.2, random_state=42)
anx_model = RandomForestClassifier()
anx_model.fit(X_train_anx, y_train_anx)
pickle.dump(anx_model, open("anxiety_model.pkl", "wb"))

# Train Stress Model
y_str = df['Stress_Level']
X_train_str, X_test_str, y_train_str, y_test_str = train_test_split(X, y_str, test_size=0.2, random_state=42)
str_model = RandomForestClassifier()
str_model.fit(X_train_str, y_train_str)
pickle.dump(str_model, open("stress_model.pkl", "wb"))

print("✅ All models trained and saved successfully.")
