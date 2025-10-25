from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows React (localhost:3000) to talk to Flask (localhost:5000)

@app.route("/message", methods=["POST"])
def get_message():
    data = request.get_json()              # read JSON body from React
    user_input = data.get("message", "")   # extract the "message" field
    print("Message from React:", user_input)

    # send a response back
    return jsonify({"reply": f"You said: {user_input}"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
