import collections
import json
import os
import string

import numpy as np
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, send_file, session, url_for

# Load environment variables
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
AUDIO_ROOT_DIR = os.getenv("AUDIO_ROOT_DIR")

# Global variable to load and store the annotation data being used by the server
ANNOTATION_DATA = {}

# Create the main Flask application
app = Flask(__name__)

# Set the secret key for the Flask application - used for session management
app.secret_key = os.urandom(24)
app.config["TEMPLATES_AUTO_RELOAD"] = True

### Website handler functions

# 401 Unauthorized
@app.errorhandler(401)
def unauthorized(e):
    return redirect("/login/")


@app.errorhandler(404)
def page_not_found(e):
    return """Something went wrong. Please refresh the page or restart the server. 
    In case of further escalation, please create an issue on GitHub with details of how to reproduce the error. We will try our best to resolve the issue.
    Additionally, we'd love to have you contribute to the project by resolving any issue you find relevant under the 'Issues' tracker.
    Thank you!
    """


# 500 page
@app.errorhandler(500)
def internal_server_error(e):
    return # 404 page


@app.route("/login/", methods=["GET", "POST"])
def login():
    """Login page"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            return "Invalid credentials. Please try again.", 401
    return render_template("login.html")


@app.route("/logout/")
def logout():
    """Logout page"""
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route("/")
def home():
    """Show home page"""
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html", samples=ANNOTATION_DATA)


def hhmmss_to_ss(input):
    """Convert HH:MM:SS.mmm to seconds"""
    hh, mm, ssms = input.split(":")
    return round(float(hh) * 3600 + float(mm) * 60 + float(ssms), 3)


@app.route("/annotation_viewer/")
@app.route("/annotation_viewer/<path:fname>/")
def annotation_viewer(fname=""):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if fname == "":
        # pick a random file
        fname = list(ANNOTATION_DATA.keys())[np.random.randint(0, len(ANNOTATION_DATA))]

    # Prep audio path and json annotations
    try:
        json_fname, ref_text_fname = ANNOTATION_DATA[fname]
    except:
        json_fname, ref_text_fname = ANNOTATION_DATA["./" + fname]

    with open(json_fname, "r") as fid:
        json_annots = json.load(fid)

    if os.path.exists(ref_text_fname):
        ref_text = open(ref_text_fname, "r").read().replace("\n", " ")
        # Step 2: Strip punctuation, convert to lowercase, and clean up spaces
        ref_text = ref_text.translate(str.maketrans("", "", string.punctuation)).lower()
        ref_text = ref_text.replace("'", "").replace('"', "").replace("  ", " ").strip()
        # Step 3: Split into words
        ref_text = ref_text.split(" ")
    else:
        ref_text = []

    # Process JSON annotations
    annotations = []

    annotation_transcript = ""
    for i, annot in enumerate(json_annots["annotations"]):
        if len(annot["Transcription"]) != 1:
            print("** Something wrong with annotation:", annot)
            continue
        
        annotation_transcript += " " + annot["Transcription"][0]

        annotations.append(
            {
                "index": i,
                "start": hhmmss_to_ss(annot["start"]),
                "end": hhmmss_to_ss(annot["end"]),
                "label": annot["Transcription"][0],
            }
        )

    return render_template(
        "annotation_viewer.html",
        fname=fname,
        annotations=annotations,
        ref_text=" ".join(ref_text),
    )


@app.route("/audio/<path:audio>")
def play_audio(audio):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return send_file(audio)


def populate_data():
    """Get list of all audio files with JSON annotations"""
    annotated_data = os.listdir(AUDIO_ROOT_DIR)
    for audio_folder in annotated_data:
        audio_file_path = os.path.join(AUDIO_ROOT_DIR, audio_folder, "audio.mp3")
        ref_text_file_path = os.path.join(AUDIO_ROOT_DIR, audio_folder, "ref_text.txt")
        annotation_json_path = os.path.join(
            AUDIO_ROOT_DIR, audio_folder, "annotation.json"
        )
        if os.path.exists(audio_file_path):
            ANNOTATION_DATA[audio_file_path] = (annotation_json_path, ref_text_file_path)

if __name__ == "__main__":
    populate_data()
    app.run(host="0.0.0.0", port=30110, debug=True)
