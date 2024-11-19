import random
from flask import Flask, abort, render_template, send_from_directory
import webbrowser
from threading import Timer
import markdown

import config_manager
import path_util
from portfolio import Portfolio
from portfolio_element import PortfolioElement

app = Flask(__name__)  # Create the Flask app instance


@app.route("/")
def serve_home():
    image_elements = [element for element in portfolio.get_elements() if element.get_asset_type() == "image"]
    three_random_images_elements = random.sample(image_elements, k=min(3, len(image_elements)))
    return render_template(
        "home.jinja", text_block="This is a block of plain text passed from app.py.", carousel_elements=three_random_images_elements
    )


@app.route("/gallery")
def serve_gallery():
    print("User")
    list_of_elements = portfolio.get_elements()
    print(f"Found {len(list_of_elements)} elements in the portfolio.")
    return render_template("gallery.jinja", elements=portfolio.get_elements())


@app.route("/<path:page>")
def serve_page(page):
    markdown_file = path_util.resolve_path(f"custom_pages/{page}.md")
    try:
        # read with utf-8 encoding
        with open(markdown_file, "r", encoding="utf-8") as file:
            markdown_text = file.read()
            rendered_markdown = markdown.markdown(markdown_text)
            return render_template("text_page.jinja", markdown_content=rendered_markdown)
    except FileNotFoundError:
        abort(404)


@app.route("/portfolio/<path:path>")
def serve_portfolio(path):
    # determine if direct file (has extension) or portfolio element
    if "." in path:
        return serve_portfolio_file(path)
    else:
        return serve_portfolio_page(path)


def serve_portfolio_file(path):
    """Serve the portfolio assets files directly when there is an extension, e.g. allow direct access to images."""
    print(f"Requesting portfolio file directly: {path}")
    return send_from_directory("portfolio", path)


def serve_portfolio_page(asset_identifier):
    """Render a single portfolio element's page."""
    print(f"Requesting portfolio element's page: {asset_identifier}")
    portfolio_element: PortfolioElement = portfolio.get_element_by_identifier(asset_identifier)

    if portfolio_element is None:
        abort(404)

    asset_type = portfolio_element.get_asset_type()

    if asset_type == "image":
        template = "image_page.jinja"
    elif asset_type == "video":
        template = "video_page.jinja"
    elif asset_type == "audio":
        template = "audio_page.jinja"
    else:
        template = "text_page.jinja"

    # DEBUG : Print the template being used
    print(f"Client requesting asset type: {asset_type}. Using template: {template}")

    return render_template(
        template,
        portfolio_element=portfolio_element,
        previous_element=portfolio.get_element_before(portfolio_element),
        next_element=portfolio.get_element_after(portfolio_element),
    )


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    print("Application starting.")
    print("Loading configs.")
    config_manager.load_configs(app)
    # DEBUG
    print(f"Config loaded: {config_manager._config_dict}")

    print("Building portfolio structure.")
    portfolio = Portfolio()

    print("Schedule browser to open in 1 second.")
    Timer(1, open_browser).start()  # Non-blocking delay before opening the page to let the server start, since the server itself is blocking

    print("Starting Flask server...")
    app.run(debug=True, use_reloader=False)
