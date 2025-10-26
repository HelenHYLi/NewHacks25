#Import files
from flask import Flask, request, jsonify
from flask_cors import CORS
import plan 

#Use flask to communicate with react
app = Flask(__name__)
CORS(app)  # allow React to talk to Flask

@app.route("/message", methods=["POST"])
def get_message():
    data = request.get_json()              # read JSON body
    user_input = data.get("message", "")   # pull out "message"
    print("Message from React:", user_input)
    output = plan.gemini(user_input)

    # send a response back to React
    return jsonify({
        "status": "ok",
        "echo": user_input,
        #"reply": f"I got your message: {user_input}"
        "reply": output
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
