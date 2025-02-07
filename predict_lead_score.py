import pickle
import pandas as pd
import sqlite3

# Load the trained model
with open("lead_scoring_model.pkl", "rb") as file:
    model = pickle.load(file)

# Function to predict lead score
def predict_lead_score(website_visits, email_opens, service_interest):
    service_map = {"Low": 1, "Medium": 2, "High": 3}
    service_interest_num = service_map.get(service_interest, 1)

    lead_data = pd.DataFrame([[website_visits, email_opens, service_interest_num]],
                             columns=["website_visits", "email_opens", "service_interest"])
    
    score = model.predict_proba(lead_data)[0][1]  # Probability of conversion
    return round(score * 100, 2)  # Convert to percentage

# Example lead
new_lead_score = predict_lead_score(7, 3, "High")
print(f"🔥 Lead Conversion Probability: {new_lead_score}%")
