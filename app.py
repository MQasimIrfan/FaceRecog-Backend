from flask import Flask, request, jsonify
from flask_cors import CORS
from face_utils import find_face
import os, base64, tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

DATASET_DIR = "dataset"

@app.route("/recognize", methods=["POST"])
def recognize():
    try:
        data = request.json
        if not data or "image" not in data:
            return jsonify({"error": "No image data provided"}), 400

        img_data = base64.b64decode(data["image"].split(",")[1])
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tmp.write(img_data)
        tmp.close()

        identity = find_face(tmp.name)
        os.unlink(tmp.name)

        return jsonify({"name": identity})

    except Exception as e:
        print("Error in /recognize:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/register", methods=["POST"])
def register():
    try:
        name = request.form.get("name")
        file = request.files.get("image")
        image_name = request.form.get("image_name", "image").strip()

        if not name or not file:
            return jsonify({"error": "Name and image are required"}), 400

        name = secure_filename(name)
        image_name = secure_filename(image_name)

        user_folder = os.path.join(DATASET_DIR, name)
        os.makedirs(user_folder, exist_ok=True)

        save_path = os.path.join(user_folder, f"{image_name}.jpg")
        file.save(save_path)

        return jsonify({
            "status": "success",
            "message": f"{name} registered with image: {image_name}.jpg"
        })

    except Exception as e:
        print("Error in /register:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Face Recognition API is live!"

if __name__ == "__main__":
    app.run(debug=True)
