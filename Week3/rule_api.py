from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

candidates = [
    {"id": 1, "name": "Alice", "position": "Developer"},
    {"id": 2, "name": "Bob", "position": "Designer"},
    {"id": 3, "name": "Charlie", "position": "Tester"}
]


@app.route("/api/v1/candidates", methods=["GET"])
def get_candidates():

    response_body = {
        "success": True,
        "data": candidates,
        "message": "Candidates retrieved successfully"
    }

    response = make_response(jsonify(response_body), 200)
    
    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)