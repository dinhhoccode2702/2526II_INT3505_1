from flask import Flask, jsonify, request

app = Flask(__name__)

candidates = [
    {"id": 1, "name": "Alice", "position": "Developer", "skills": ["Python", "Flask"]},
    {"id": 2, "name": "Bob", "position": "Designer", "skills": ["UI/UX", "Figma"]},
    {"id": 3, "name": "Charlie", "position": "Tester", "skills": ["Selenium", "TestNG"]}
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
        "data": None,
        "message": "Candidate not found"
    }), 404


@app.route("/api/v1/candidates/<int:id>/skill-list", methods=["GET"])
def get_candidate_skill_list(id):
    for c in candidates:
        if c["id"] == id:
            return jsonify({
                "success": True,
                "data": {"skills": c["skills"]},
                "message": "Candidate retrieved successfully"
            }), 200
    return jsonify({
        "success": False,
        "data": None,
        "message": "Candidate not found"
    }), 404

@app.route("/api/v1/candidates/<int:id>/name", methods=["GET"])
def get_candidate_name(id):
    for c in candidates:
        if c["id"] == id:
            return jsonify({
                "success": True,
                "data": {"name": c["name"]},
                "message": "Candidate retrieved successfully"
            }), 200
    return jsonify({
        "success": False,
        "data": None,
        "message": "Candidate not found"
    }), 404

@app.route("/api/v1/candidates", methods=["POST"])
def create_candidate():
    data = request.json
    if not data:
        return jsonify({
            "success": False,
            "data": None,
            "message": "Invalid request body"
        }), 400
    
    candidates.append(data)

    return jsonify({
        "success": True,
        "data": data,
        "message": "Candidate created successfully"
    }), 201

@app.route("/api/v1/candidates/<int:id>", methods=["DELETE"])
def delete_candidate(id):
    global candidates
    
    # Check if candidate exists
    candidate_to_delete = None
    for c in candidates:
        if c["id"] == id:
            candidate_to_delete = c
            break
    
    if not candidate_to_delete:
        return jsonify({
            "success": False,
            "data": None,
            "message": "Candidate not found"
        }), 404
    
    candidates = [c for c in candidates if c["id"] != id]

    return jsonify({
        "success": True,
        "data": candidate_to_delete,
        "message": "Candidate deleted successfully"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)