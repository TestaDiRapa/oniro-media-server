from flask import Flask, jsonify, request, send_file
from random import randint
import os

app = Flask(__name__)
app.config["IMAGE_UPLOADS"] = "/root/oniro-media-server"
app.config["HOST_IP"] = "45.76.47.94:8082"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def is_file_valid(filename):
    return filename[-3:] in ALLOWED_EXTENSIONS


@app.route('/mediaserver', methods=['POST'])
def add_image():

    params = request.form

    if "user" not in params:
        return jsonify(status="error", message="user is a mandatory parameter")

    user = params["user"]

    if "file" not in request.files or request.files["file"].filename == '':
        return jsonify(status="error", message="no file sent")

    filename = request.files["file"].filename

    if not is_file_valid(filename):
        return jsonify(status="error", message="file is not valid")

    try:
        path = user + "-propic"+str(randint(0,1000000))+filename[-4:]
        request.files["file"].save(os.path.join(app.config["IMAGE_UPLOADS"], path))
        return jsonify(status="ok", path="http://"+ app.config["HOST_IP"] +"/mediaserver/"+path)

    except Exception as e:
        return jsonify(status="error", message=str(e))


@app.route('/mediaserver/<path:file_path>', methods=['GET'])
def get_image(file_path):
    return send_file(file_path)


if __name__ == "__main__":
    app.run("0.0.0.0", 8082)
