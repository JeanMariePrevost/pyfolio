"""
This module contains helper functions for rendering custom pages and processing markdown documents.
"""

import random
from flask import render_template
import markdown

import app_logger
from portfolio import Portfolio


def render_custom_page_from_markdown_file(path_to_markdown_file: str):
    """
    Processes a markdown file and returns the rendered HTML content to be injected into custom pages.
    Also replaces custom tags found in the markdown with the appropriate content, e.g. {{pyfolio-carousel}} or {{pyfolio-gallery}}.
    Returns None if the file is not found or an error occurs during processing.
    """
    try:
        with open(path_to_markdown_file, "r", encoding="utf-8") as file:
            markdown_text = file.read()
            rendered_markdown = markdown.markdown(markdown_text)

            # process the markdown text to inject carousel elements
            rendered_markdown = process_custom_pyfolio_tags(rendered_markdown)
        return render_template("text_page.jinja", rendered_markdown_content=rendered_markdown)
    except FileNotFoundError:
        app_logger.error(f"Markdown file not found: {path_to_markdown_file}")
        return None
    except Exception as e:
        app_logger.error(f"Error processing markdown file [{path_to_markdown_file}]: {e}")
        return None


def get_random_portfolio_image_elements(amount: int):
    image_elements = [element for element in Portfolio.get_instance().get_elements() if element.get_asset_type() == "image"]
    return random.sample(image_elements, k=min(amount, len(image_elements)))


def process_custom_pyfolio_tags(markdown_text: str):
    processed_markdown = markdown_text.replace(
        "{{pyfolio-carousel}}", render_template("carousel_component.jinja", carousel_elements=get_random_portfolio_image_elements(3))
    )
    # TODO: Also add gallery component
    return processed_markdown
