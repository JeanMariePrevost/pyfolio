import random
from flask import Flask, abort, render_template, send_from_directory
import webbrowser
from threading import Timer

import config_manager
import custom_pages_util
import app_logger
import path_util
from portfolio import Portfolio
from portfolio_element import PortfolioElement

app = Flask(__name__)  # Create the Flask app instance


@app.route("/")
def serve_home():
    # If there is a home.md file in the custom_pages folder, render it as the home page
    if path_util.file_exists_relative("custom_pages/home.md"):
        app_logger.debug("app.server_home: Found home.md file. Serving custom home page.")
        return serve_custom_page("home")
    else:
        app_logger.debug("app.server_home: No home.md file found. Serving default home page.")
        return render_template("home.jinja", carousel_elements=custom_pages_util.get_random_portfolio_image_elements(3))


@app.route("/gallery")
def serve_gallery():
    list_of_elements = Portfolio.get_instance().get_elements()
    return render_template("gallery.jinja", elements=list_of_elements)


@app.route("/<path:page>")
def serve_custom_page(page):
    markdown_file = path_util.resolve_path(f"custom_pages/{page}.md")
    app_logger.debug(f"Requesting custom page: {page}. Resolved markdown file path: {markdown_file}")
    return custom_pages_util.render_custom_page_from_markdown_file(markdown_file)
    # return render_template("text_page.jinja", rendered_markdown_content=rendered_markdown_content)
    # abort(404)


@app.route("/portfolio/<path:path>")
def serve_portfolio(path):
    # determine if direct file (has extension) or portfolio element
    if "." in path:
        return serve_portfolio_file(path)
    else:
        return serve_portfolio_page(path)


def serve_portfolio_file(path):
    """Serve the portfolio assets files directly when there is an extension, e.g. allow direct access to images."""
    app_logger.debug(f"Requesting portfolio file directly: {path}")
    return send_from_directory("portfolio", path)


def serve_portfolio_page(asset_identifier):
    """Render a single portfolio element's page."""
    app_logger.debug(f"Requesting portfolio element's page: {asset_identifier}")
    portfolio_element: PortfolioElement = Portfolio.get_instance().get_element_by_identifier(asset_identifier)

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

    app_logger.debug(f"Client requesting asset type: {asset_type}. Using template: {template}")

    return render_template(
        template,
        portfolio_element=portfolio_element,
        previous_element=Portfolio.get_instance().get_element_before(portfolio_element),
        next_element=Portfolio.get_instance().get_element_after(portfolio_element),
    )


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    app_logger.info("Application starting.")
    app_logger.debug("Loading configs.")
    config_manager.load_configs(app)
    # DEBUG
    app_logger.debug(f"Config loaded: {config_manager._config_dict}")

    app_logger.debug("Building portfolio structure.")
    Portfolio.get_instance()  # Not needed but it pre-generates the portfolio

    app_logger.warning("This is a local server. Schedule browser to open in 1 second.")
    Timer(1, open_browser).start()  # Non-blocking delay before opening the page to let the server start, since the server itself is blocking

    app_logger.info("Starting Flask server...")
    app.run(debug=True, use_reloader=False)
