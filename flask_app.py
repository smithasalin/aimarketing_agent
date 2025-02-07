from markupsafe import escape
from flask import Flask, request, jsonify, escape
import requests  # Import the requests module
import pickle
import pandas as pd
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Hello, world!")

# Load the trained model
with open("lead_scoring_model.pkl", "rb") as file:
    model = pickle.load(file)

# Initialize database
def init_db():
    conn = sqlite3.connect('leads.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, website_visits INTEGER, email_opens INTEGER, service_interest TEXT, conversion_probability REAL)''')
    conn.commit()
    conn.close()

# Save lead to database
def save_lead(name, email, website_visits, email_opens, service_interest, conversion_probability):
    conn = sqlite3.connect('leads.db')
    c = conn.cursor()
    c.execute("INSERT INTO leads (name, email, website_visits, email_opens, service_interest, conversion_probability) VALUES (?, ?, ?, ?, ?, ?)",
              (name, email, website_visits, email_opens, service_interest, conversion_probability))
    conn.commit()
    conn.close()

def predict_lead_score(website_visits, email_opens, service_interest):
    service_map = {"Low": 1, "Medium": 2, "High": 3}
    service_interest_num = service_map.get(service_interest, 1)

    lead_data = pd.DataFrame([[website_visits, email_opens, service_interest_num]],
                             columns=["website_visits", "email_opens", "service_interest"])
    
    score = model.predict_proba(lead_data)[0][1]  # Probability of conversion
    return round(score * 100, 2)  # Convert to percentage

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get("message")
    name = data.get("name")
    email = data.get("email")
    website_visits = data.get("website_visits", 0)
    email_opens = data.get("email_opens", 0)
    service_interest = data.get("service_interest", "Low")
    
    score = predict_lead_score(website_visits, email_opens, service_interest)
    save_lead(name, email, website_visits, email_opens, service_interest, score)
    
    response_message = f"AI says: {user_message}. Lead conversion probability: {score}%"
    return jsonify({"response": response_message})

@app.route('/test', methods=['GET'])
def test():
    return "Test route works!"

@app.route('/send_request', methods=['GET'])
def send_request():
    # Sending a POST request to /chatbot from within the Flask app
    data = {"message": "Hello AI!"}
    response = requests.post('http://127.0.0.1:8080/chatbot', json=data)  # Adjusted port to 8080
    if response.status_code == 200:
        return jsonify(response.json())  # Forward the response from the chatbot to the user
    else:
        return jsonify({"error": "Failed to connect to chatbot"}), 500

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=8080)
