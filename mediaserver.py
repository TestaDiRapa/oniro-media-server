from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def is_file_valid(filename):
    return filename[-3:] in ALLOWED_EXTENSIONS


@app.route('/mediaserver', methods=['POST'])
def add_image():

    if "user" not in request.form:
        return jsonify(status="error", message="user is a mandatory parameter")

    if "file" not in request.files or request.files["file"].filename == '':
        return jsonify(status="error", message="no file sent")

    filename = request.files["file"].filename

    if not is_file_valid(filename):
        return jsonify(status="error", message="file is not valid")

    try:
        if not os.path.exists(request.form["user"]):
            os.mkdir(request.form["user"])
        path = request.form["user"] + "/propic"+filename[-4:]
        request.files["file"].save(path)
        return jsonify(status="ok", path="http://"+request.host+"/mediaserver/"+path)

    except Exception as e:
        return jsonify(status="error", message=str(e))


@app.route('/mediaserver/<path:file_path>', methods=['GET'])
def get_image(file_path):
    return send_file(file_path)


if __name__ == "__main__":
    app.run("0.0.0.0", 8082)
