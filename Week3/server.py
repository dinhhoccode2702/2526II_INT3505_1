from flask import Flask, jsonify, request

app = Flask(__name__)

candidates = [
    {"id": 1, "name": "Alice", "position": "Developer"},
    {"id": 2, "name": "Bob", "position": "Designer"},
    {"id": 3, "name": "Charlie", "position": "Tester"}
]

@app.route("/api/v1/candidates", methods=["GET"])
def get_candidates():
    return jsonify({
        "success": True,
        "data": candidates,
        "message": "Candidates retrieved successfully"
    }), 200

@app.route("/api/v1/candidates/<int:id>", methods=["GET"])
def get_candidate(id):
    for c in candidates:
        if c["id"] == id:
            return jsonify({
                "success": True,
                "data": c,
                "message": "Candidate retrieved successfully"
            }), 200
    return jsonify({
        "success": False,
        "message": "Candidate not found"
    }), 404

@app.route("/api/v1/candidates", methods=["POST"])
def create_candidate():
    data = request.json
    candidates.append(data)

    return jsonify({
        "data": data,
        "message": "Candidate created"
    }), 201

@app.route("/api/v1/candidates/<int:id>", methods=["DELETE"])
def delete_candidate(id):

    global candidates
    candidates = [c for c in candidates if c["id"] != id]

    return jsonify({
        "message": "Candidate deleted"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)