from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

tasks = [
    {
        "id" : 1,
        "title": "First",
        "description": "first",
        "done": False
    },

    {
        "id" : 2,
        "title": "Second",
        "description": "second one",
        "done": False
    },

    {
        "id" : 3,
        "title": "Third",
        "description": "third one",
        "done": False
    }
]

@auth.get_password
def getPasword(username):
    return "password" if username == "shiva" else None

@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({"error": "not found"}), 404)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error": "unauthorized"}), 401)


@app.route("/v1/tasks", methods=['GET'])
@auth.login_required
def getTasks():
    return jsonify({"tasks": tasks})

@app.route("/v1/getTask/<int:taskId>", methods=['GET'])
def returnTask(taskId):
    task = [task for task in tasks if task["id"] == taskId]
    if len(task) == 0:
        abort(404)
    return jsonify({"task": task[0]})

@app.route("/v1/createTask", methods=['POST'])
def createTask():
    if not request.json or "title" not in request.json:
        abort(400)
    task = {
        "id": tasks[-1]["id"]+1,
        "title": request.json["title"],
        "description": request.json.get("description", ""),
        "done": False
    }

    tasks.append(task)
    return jsonify({"task": task}), 201


if __name__ == '__main__':
    app.run()
