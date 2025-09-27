from flask import Flask, render_template, request, jsonify
import json, random
from datetime import datetime

app = Flask(__name__)

# Load intents for small talk
with open("intents.json") as f:
    intents = json.load(f)

# --- Personality Wrappers ---
funny_wrappers = [
    "Here’s what my overworked circuits found: {}",
    "Easy peasy. The answer is {}, and yes, I double-checked.",
    "{}… at least that’s what the internet told me.",
    "Drumroll please… {}.",
    "My crystal ball says: {}",
    "I was going to keep this to myself, but fine: {}",
    "Don’t tell anyone I told you this… {}",
    "Let’s pretend I thought hard about it: {}",
    "Obviously, it’s {}. Anyone could’ve guessed that."
]

def wrap_answer(answer):
    """Always add humor/personality to any answer."""
    return random.choice(funny_wrappers).format(answer)


# --- Core Response Logic ---
def get_response(user_input):
    user_input = user_input.lower().strip()

    # Math calculation
    if any(char.isdigit() for char in user_input) and any(op in user_input for op in "+-*/"):
        try:
            result = str(eval(user_input))
            return wrap_answer(result)
        except:
            return wrap_answer("Math isn’t my strong suit today")

    # Time and Date
    if "time" in user_input:
        return wrap_answer(f"The current time is {datetime.now().strftime('%H:%M')}")
    if "date" in user_input:
        return wrap_answer(f"Today’s date is {datetime.now().strftime('%Y-%m-%d')}")

    # Check intents.json for small talk
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern in user_input:
                return wrap_answer(random.choice(intent['responses']))

    # Fallback
    return wrap_answer("I have no idea… but I said it with confidence, so it counts.")


# --- Flask Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.form["msg"]
    response = get_response(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)