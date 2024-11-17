import os
from flask import Flask, render_template
import webbrowser
from threading import Timer

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.jinja", text_block="This is a block of plain text passed from app.py.")


@app.route("/gallery")
def gallery():
    # TODO : Currently a placeholder
    return "This page has not yet been defined."


@app.route("/about")
def about():
    # TODO : Currently a placeholder
    return "This page has not yet been defined."


@app.route("/contact")
def contact():
    # TODO : Currently a placeholder
    return "This page has not yet been defined."


@app.route("/privacy_policy")
def privacy_policy():
    # TODO : Currently a placeholder
    return "This page has not yet been defined."


@app.route("/terms_of_service")
def terms_of_service():
    # TODO : Currently a placeholder
    return "This page has not yet been defined."


@app.route("/cookie_policy")
def cookie_policy():
    # TODO : Currently a placeholder
    return "This page has not yet been defined."


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    print("Starting Flask server...")
    # Check if the script is run by the Flask reloader
    if not app.debug or "FLASK_RUN_FROM_CLI" not in os.environ:
        Timer(1, open_browser).start()  # Non-blocking delay before opening the page to let the server start, since the server itself is blocking

    app.run(debug=True, use_reloader=False)
