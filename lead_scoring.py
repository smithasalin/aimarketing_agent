import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import sqlite3

# Load lead data
df = pd.read_csv("lead_data.csv")

# Convert categorical values to numeric
df["service_interest"] = df["service_interest"].map({"Low": 1, "Medium": 2, "High": 3})

# Features and target
X = df[["website_visits", "email_opens", "service_interest"]]
y = df["converted"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
with open("lead_scoring_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✅ Lead Scoring Model Trained & Saved!")
