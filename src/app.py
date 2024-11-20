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
    # Special case for the home page, has a default if no custom page is found
    if path_util.file_exists_relative("custom_pages/home.md"):
        app_logger.debug("app.server_home: Found home.md file. Serving custom home page.")
        return serve_custom_page("home")
    else:
        app_logger.warning("app.server_home: No home.md file found. Serving default.")
        return custom_pages_util.render_custom_page_from_markdown_text(
            "# Welcome to Pyfolio!\n\nThis is the default home page. You can customize it by creating a `home.md` file in the `custom_pages` folder.\n\n{{pyfolio-carousel}}"
        )


@app.route("/gallery")
def serve_gallery():
    # Special case for the gallery page, has a default if no custom page is found
    if path_util.file_exists_relative("custom_pages/gallery.md"):
        app_logger.debug("app.serve_gallery: Found gallery.md file. Serving custom gallery page.")
        return serve_custom_page("gallery")
    else:
        app_logger.info("app.serve_gallery: No gallery.md file found. Serving default.")
        return custom_pages_util.render_custom_page_from_markdown_text("# Gallery\n\n{{pyfolio-gallery}}")


@app.route("/<path:page>")
def serve_custom_page(page):
    markdown_file = path_util.resolve_path(f"custom_pages/{page}.md")
    app_logger.debug(f"Requesting custom page: {page}. Resolved markdown file path: {markdown_file}")
    rendered_page = custom_pages_util.render_custom_page_from_markdown_file(markdown_file)
    if rendered_page is None:
        app_logger.warning(f"Custom page not found: {page}.")
        abort(404)
    return rendered_page


@app.route("/portfolio/<path:path>")
def serve_portfolio(path):
    if "." in path:
        # "." Indicates a file request
        return serve_portfolio_file(path)
    else:
        # Is a page request
        return serve_portfolio_page(path)


def serve_portfolio_file(path):
    """Serve the portfolio assets files directly when there is an extension, e.g. allow direct access to images."""
    # app_logger.debug(f"Requesting portfolio file directly: {path}")
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


def setup_environment():
    app_logger.debug("Loading configs.")
    config_manager.load_configs(app)

    app_logger.debug("Building portfolio structure.")
    Portfolio.get_instance()  # Not needed but it pre-generates the portfolio


app_logger.info("Application starting. Setting up environment...")
setup_environment()

if __name__ == "__main__":
    app_logger.info("Application rnnning directly. Assuming local server.")

    # app_logger.warning("This is a local server. Schedule browser to open in 1 second.")
    # Timer(1, open_browser).start()  # Non-blocking delay before opening the page to let the server start, since the server itself is blocking

    app_logger.info("Starting Flask server...")
    app.run(debug=True, use_reloader=False)
    # app.run()
