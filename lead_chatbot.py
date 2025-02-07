import openai
import json
import csv
import sqlite3

# OpenAI API Key (Replace with your key)
openai.api_key = "OPENAI_API_KEY"

# Initialize database
def init_db():
    conn = sqlite3.connect('leads.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS leads
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, website_visits INTEGER, email_opens INTEGER, service_interest TEXT, conversion_probability REAL)''')
    conn.commit()
    conn.close()

# Function to interact with chatbot
def chatbot_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a lead generation chatbot. Ask questions to capture customer details."},
                  {"role": "user", "content": user_input}]
    )
    return response['choices'][0]['message']['content']

# Function to collect lead details
def collect_lead_info():
    print("🤖 AI Chatbot: Hello! I’d love to learn more about your needs. What’s your name?")
    name = input("You: ")

    print(f"🤖 AI Chatbot: Thanks, {name}! What’s your email?")
    email = input("You: ")

    print("🤖 AI Chatbot: What service or product are you looking for?")
    service = input("You: ")

    lead = {"name": name, "email": email, "service": service}
    print("\n✅ Lead Captured:", json.dumps(lead, indent=2))

    return lead

# Function to save lead to database
def save_lead_to_db(lead):
    conn = sqlite3.connect('leads.db')
    c = conn.cursor()
    c.execute("INSERT INTO leads (name, email, service) VALUES (?, ?, ?)",
              (lead["name"], lead["email"], lead["service"]))
    conn.commit()
    conn.close()
    print("✅ Lead saved to database!")

# Run chatbot
if __name__ == "__main__":
    init_db()
    lead = collect_lead_info()
    save_lead_to_db(lead)
