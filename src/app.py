import os
from flask import Flask, render_template, send_from_directory
import webbrowser
from threading import Timer
import markdown

from portfolio import Portfolio
from portfolio_element import PortfolioElement

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.jinja", text_block="This is a block of plain text passed from app.py.")


@app.route("/gallery")
def gallery():
    print("User")
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


@app.route("/portfolio/<path:asset_identifier>.<ext>")
def serve_portfolio(asset_identifier, ext):
    """Serve the portfolio assets files directly when there is an extension, e.g. allow direct access to images."""
    print(f"Requesting portfolio fiel directly: {asset_identifier}.{ext}")
    return send_from_directory("portfolio", asset_identifier + "." + ext)


@app.route("/portfolio/<path:asset_identifier>")
def element(asset_identifier):
    """Render a single portfolio element's page."""
    print(f"Requesting portfolio element's page: {asset_identifier}")
    portfolio_element: PortfolioElement = portfolio.get_element_by_identifier(asset_identifier)

    if not portfolio_element:
        return render_template(
            "text_page.jinja",
            page_title="Element not found",
            markdown_content=markdown.markdown("The requested portfolio element was not found.\n\n[Return to the gallery](/gallery)"),
        )

    # Determine asset type based on file extension
    extension = portfolio_element.get_extension()
    asset_type = portfolio_element.get_asset_type()

    return render_template(
        "portfolio_element_page.jinja",
        page_title=portfolio_element.get_file_name(),
        asset_url=portfolio_element.get_absolute_url("/portfolio/"),
        asset_type=asset_type,
        asset_extension=extension,
        markdown_content=portfolio_element.get_asset_text(),
    )


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
