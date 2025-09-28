import os

from flask import Flask, render_template, request, jsonify
import json, random
from datetime import datetime

app = Flask(__name__)

# Load intents for small talk
with open("intents.json") as f:
    intents = json.load(f)

# --- Funny response banks ---

funny_greetings = [
    "Morning! Don’t worry, the coffee will eventually do its job ☕",
    "Good morning! I’m 80% code, 20% sass, and 0% awake.",
    "Rise and shine… or at least rise. Shining is optional."
]

funny_evenings = [
    "Good evening! Perfect time to do absolutely nothing productive.",
    "Evening! Don’t forget: Netflix counts as self-care.",
    "Another day survived. You deserve a cookie 🍪"
]

funny_nights = [
    "Good night! May your dreams be bug-free.",
    "Nighty night! Don’t let existential dread bite.",
    "Sleep well — I’ll be here judging your browsing history tomorrow."
]

funny_afternoons = [
    "Good afternoon! Aka the time when everyone wants a nap.",
    "Afternoon! Half the day’s gone, but hey, you’re still standing.",
    "Good afternoon — productivity optional, snacking mandatory."
]

funny_math = [
    "The answer is {}. And yes, I checked twice.",
    "{}. Easy math. Don’t ask me to do calculus though.",
    "Math complete: {}. I deserve a medal 🏅"
]

funny_time = [
    "It’s currently {}. Time to panic about deadlines?",
    "{} — which is just a fancy way of saying 'too late to nap'.",
    "Right now it’s {}. You’re welcome, human clock."
]

funny_date = [
    "Today’s date is {}. Do what you want with that info.",
    "{} — another day to make questionable life choices.",
    "It’s {}. A perfectly fine day for snacks."
]

funny_fallback = [
    "I have no idea… but I said that with confidence so it counts.",
    "Can’t help you there, but let’s pretend I answered.",
    "That question is above my pay grade (which is $0).",
    "Ask me again later. Or never. Never works too."
]

# --- Core Response Logic ---
def get_response(user_input):
    user_input = user_input.lower().strip()

    # Greetings
    if "good morning" in user_input:
        return random.choice(funny_greetings)
    if "good evening" in user_input:
        return random.choice(funny_evenings)
    if "good night" in user_input:
        return random.choice(funny_nights)
    if "good afternoon" in user_input:
        return random.choice(funny_afternoons)

    # Math calculation
    if any(char.isdigit() for char in user_input) and any(op in user_input for op in "+-*/"):
        try:
            result = str(eval(user_input))
            return random.choice(funny_math).format(result)
        except:
            return "Math isn’t my strong suit today."

    # Time and Date
    if "time" in user_input:
        current_time = datetime.now().strftime("%H:%M")
        return random.choice(funny_time).format(current_time)
    if "date" in user_input:
        current_date = datetime.now().strftime("%Y-%m-%d")
        return random.choice(funny_date).format(current_date)

    # Check intents.json for small talk
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern in user_input:
                return random.choice(intent['responses'])

    # Fallback
    return random.choice(funny_fallback)

# --- Flask Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.form["msg"]
    response = get_response(user_input)
    return jsonify({"response": response})

# --- Run the app ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)