from flask import Flask, render_template, request, redirect, url_for
import os

# Create Flask app
app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload limit


# Home / Upload Page
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")

        if not file or file.filename == "":
            return redirect(request.url)

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Later: preprocess + metrics + visualization
        return redirect(url_for("upload_file"))

    return render_template("upload.html")


if __name__ == "__main__":
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    app.run(debug=True)
