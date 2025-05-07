from flask import Flask, render_template, request
from gradio_client import Client, handle_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = Client("selfit-camera/OutfitAnyway")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cloth = request.files["cloth_image"]
        pose = request.files["pose_image"]
        high_res = bool(request.form.get("high_resolution"))

        cloth_path = os.path.join(app.config['UPLOAD_FOLDER'], cloth.filename)
        pose_path = os.path.join(app.config['UPLOAD_FOLDER'], pose.filename)
        cloth.save(cloth_path)
        pose.save(pose_path)

        result = client.predict(
            cloth_image=handle_file(cloth_path),
            pose_image=handle_file(pose_path),
            high_resolution=high_res,
            api_name="/onClick"
        )

        result_img, runtime_info, value_21 = result
        return render_template("index.html", result_img=result_img,
                               runtime_info=runtime_info, value_21=value_21)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
