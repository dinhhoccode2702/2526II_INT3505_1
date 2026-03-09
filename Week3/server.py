from flask import Flask, jsonify, request

app = Flask(__name__)

candidates = [
    {"id": 1, "name": "Alice", "position": "Developer"},
    {"id": 2, "name": "Bob", "position": "Designer"},
    {"id": 3, "name": "Charlie", "position": "Tester"}
]

@app.route("/candidates", methods=["GET"])
def get_candidates():
    return jsonify(candidates), 200

@app.route("/get_candidates_details/<int:id>", methods=["GET"])
def get_candidate(id):
    for c in candidates:
        if c["id"] == id:
            return jsonify(c), 200

    return jsonify({"error": "Candidate not found"}), 404

@app.route("/Candidates", methods=["POST"])
def create_candidate():
    data = request.json
    candidates.append(data)

    return jsonify({
        "data": data,
        "message": "Candidate created"
    }), 201

@app.route("/Candidates/<int:id>", methods=["DELETE"])
def delete_candidate(id):

    global candidates
    candidates = [c for c in candidates if c["id"] != id]

    return jsonify({
        "message": "Candidate deleted"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)