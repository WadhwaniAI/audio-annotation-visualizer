import collections
import glob
import json
import os
import string
from datetime import timedelta

import numpy as np
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, send_file, session, url_for

load_dotenv()
# Create the main Flask application
app = Flask(__name__)
app.secret_key = os.urandom(24)  # TODO: Check why is this required?
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set the username and password for the login
# TODO: Move this to a dotenv file
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
AUDIO_ROOT_DIR = os.getenv("AUDIO_ROOT_DIR")
ANNOTATED_DATA_DIR = os.getenv("ANNOTATED_DATA_DIR")

###### START: Website handler functions


@app.after_request
def after_request(response):
    response.headers.add("Accept-Ranges", "bytes")
    return response


@app.before_request
def set_session_timeout():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


# 401 Unauthorized
@app.errorhandler(401)
def unauthorized(e):
    return redirect("/login/")


# TODO: Change Makarand's name and instead ask to create an issue on GitHub
# 404 page
@app.errorhandler(404)
def page_not_found(e):
    return 'Page Not Found. Go back to <a href="/">home</a>, or contact Makarand Tapaswi with the URL.'


# 500 page
@app.errorhandler(500)
def internal_server_error(e):
    return "Internal server error. Contact Makarand Tapaswi with the URL that got you to this page. Thanks!"


###### END: Website handler functions
# TODO: Add to README that autentication is basic and supports only one username and password.
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
    return render_template("index.html", samples=DATA)


# TODO: Move this to utils.py
def hhmmss_to_ss(input):
    """Convert HH:MM:SS.mmm to seconds"""
    hh, mm, ssms = input.split(":")
    return round(float(hh) * 3600 + float(mm) * 60 + float(ssms), 3)


@app.route("/annot_viewer/")
@app.route("/annot_viewer/<path:fname>/")
def annot_viewer(fname=""):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if fname == "":
        # pick a random file
        fname = list(DATA.keys())[np.random.randint(0, len(DATA))]

    # Prep audio path and json annotations
    try:
        json_fname, ref_text_fname = DATA[fname]
    except:
        json_fname, ref_text_fname = DATA["/" + fname]

    with open(json_fname, "r") as fid:
        json_annots = json.load(fid)

    ref_text = open(ref_text_fname, "r").read().replace("\n", " ")

    # Step 2: Strip punctuation, convert to lowercase, and clean up spaces
    ref_text = ref_text.translate(str.maketrans("", "", string.punctuation)).lower()
    ref_text = ref_text.replace("'", "").replace('"', "").replace("  ", " ").strip()

    # Step 3: Split into words
    ref_text = ref_text.split(" ")
    # Process JSON annotations
    annots = []
    word_counter = 0  # This will be used to map words sequentially

    for annot in json_annots["annotations"]:
        if len(annot["Transcription"]) != 1:
            print("** Something wrong with annotation:", annot)
            continue

        word_index = word_counter if word_counter < len(ref_text) else np.nan

        if not np.isnan(word_index) and 0 <= word_index < len(ref_text):
            mapped_word = ref_text[word_index]
        else:
            mapped_word = "none"

        annots.append(
            {
                "start": hhmmss_to_ss(annot["start"]),
                "end": hhmmss_to_ss(annot["end"]),
                "label": annot["Transcription"][0],
                "word_index": word_index,
                "mapped_word": mapped_word,
            }
        )

        word_counter += 1

    ref_mapback = collections.defaultdict(list)
    for _, annot in enumerate(annots):
        ref_mapback[annot["word_index"]].append(annot)

    reference = []
    for k, word in enumerate(ref_text):
        reference.append(
            [
                k,
                word,
                [annot["start"] for annot in ref_mapback[k]],
                [annot["end"] for annot in ref_mapback[k]],
                [annot["label"] for annot in ref_mapback[k]],
            ]
        )

    return render_template(
        "annot_viewer.html",
        fname=fname,
        annots=annots,
        reference=reference,
        ref_text=" ".join(ref_text),
    )


@app.route("/audio/<path:audio>")
def play_audio(audio):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return send_file(audio)


def populate_data():
    """Get list of all audio files with JSON annotations"""
    annotation_paths = glob.glob(os.path.join(ANNOTATED_DATA_DIR, "*.json"))
    for fn in annotation_paths:
        audio_folder = os.path.basename(fn).split(".")[0]
        audio_fn = os.path.join(AUDIO_ROOT_DIR, audio_folder, "audio.mp3")
        ref_text_fn = os.path.join(ANNOTATED_DATA_DIR, audio_folder, "ref_text.txt")
        if os.path.exists(audio_fn):
            DATA[audio_fn] = (fn, ref_text_fn)


if __name__ == "__main__":
    DATA = {}
    populate_data()
    app.run(host="0.0.0.0", port=30110, debug=True)
