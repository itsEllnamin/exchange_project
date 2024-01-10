# API
from flask import Flask, request, jsonify

app = Flask(__name__)

verification_code = None

@app.route("/receive_code", methods=["POST"])
def receive_code():
    global verification_code
    verification_code = request.json.get("code")
    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=True)