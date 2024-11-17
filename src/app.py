import os
from flask import Flask, render_template
import webbrowser
from threading import Timer
import markdown

from portfolio import Portfolio

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.jinja", text_block="This is a block of plain text passed from app.py.")


@app.route("/gallery")
def gallery():
    print("User accessed the gallery page.")
    list_of_elements = portfolio.get_elements()
    print(f"Found {len(list_of_elements)} elements in the portfolio.")
    return render_template("gallery.jinja", elements=portfolio.get_elements())


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


@app.route("/markdown_test")
def markdown_test():
    raw_markdown = """# This is a markdown test page

This is a **markdown-powered** page.
"""
    rendered_markdown = markdown.markdown(raw_markdown)
    return render_template("text_page.jinja", page_title="Markdown Test Page", markdown_content=rendered_markdown)


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    print("Application starting.")
    print("Building portfolio structure.")
    portfolio = Portfolio()

    print("Schedule browser to open in 1 second.")
    Timer(1, open_browser).start()  # Non-blocking delay before opening the page to let the server start, since the server itself is blocking

    print("Starting Flask server...")
    app.run(debug=True, use_reloader=False)
