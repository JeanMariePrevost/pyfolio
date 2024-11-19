"""
Launch the app from this module instead of app.py to instead bake the website into a static site.
"""

import os
import app as main_app_module
from portfolio import Portfolio

OUTPUT_DIR = "bake_website_output"


def bake_site():
    """
    Generates static HTML files for the entire Flask app.
    """
    main_app_module.setup_environment()

    flask_app = main_app_module.app

    # Render then save all of the site's pages, which include home, gallery, all custom pages, and all portfolio elements pages
    # Special pages with defaults
    with flask_app.test_client() as client:
        home = client.get("/").data.decode("utf-8")
        process_and_save_file("index.html", home)
        gallery = client.get("/gallery").data.decode("utf-8")
        process_and_save_file("gallery.html", gallery)

    # Get all ".md" files in the custom_pages folder via os
    md_files = [f for f in os.listdir(main_app_module.path_util.resolve_path("custom_pages")) if f.endswith(".md")]

    for md_file in md_files:
        with flask_app.test_client() as client:
            page_name = md_file.split(".")[0]
            custom_page = client.get(f"/{page_name}").data.decode("utf-8")
            process_and_save_file(f"{page_name}.html", custom_page)

    # Get all portfolio elements
    portfolio_elements = Portfolio.get_instance().get_elements()
    for element in portfolio_elements:
        with flask_app.test_client() as client:
            portfolio_element_page = client.get("portfolio/" + element.get_identifier()).data.decode("utf-8")
            process_and_save_file("portfolio/" + element.get_identifier() + ".html", portfolio_element_page)


def process_and_save_file(file_path, content):
    """
    Fix links and other particularities, then save to the output folder.
    """
    content = fix_relative_links(content)
    save_to_output_folder(file_path, content)


def fix_relative_links(content) -> str:
    """
    Fix links that are missing the "./" or ".html" in the href or src attributes needed for static sites.
    """
    import re

    # Start by finding all relative links matches
    matches = re.findall('((href|src)="([^\.\#\?"][^:"<>\.]*?)")', content, flags=re.MULTILINE)

    # Remove duplicates to not replace the same string multiple times
    matches = list(set(matches))

    for match in matches:
        # if match has no extension, add .html
        processed_match = match[0]
        if match[2] == "/":
            # Special case for home, aka index.html
            processed_match = processed_match.replace('="/', '="./index.html')
        if "." not in processed_match:
            # add ".html" to the match before the closing quote
            processed_match = processed_match[:-1] + '.html"'
        # if match is relative, add "./"
        if '="/' in processed_match:
            # replace '="/' with '="./'
            processed_match = processed_match.replace('="/', '="./')
        # If the link is not a hash, query, or protocol, add "./"
        if all(sub not in processed_match for sub in ['="#', '="?', '=".']):
            processed_match = processed_match.replace('="', '="./')
        # replace the match in the content
        content_with_fixed_links = content.replace(match[0], processed_match)

    return content_with_fixed_links


def save_to_output_folder(file_path, content):
    """
    Save the content to the specified file path.
    """
    # ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Ensure subdirectories exist if present
    file_path = os.path.join(OUTPUT_DIR, file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


if __name__ == "__main__":
    bake_site()
    print("Site baked successfully!")
