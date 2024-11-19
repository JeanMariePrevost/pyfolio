"""
This module contains helper functions for rendering custom pages and processing markdown documents.
"""

import random
from flask import render_template
import markdown
import markdown.postprocessors

import app_logger
import config_manager
from portfolio import Portfolio

CAROUSEL_TAG = "{{pyfolio-carousel}}"
GALLERY_TAG = "{{pyfolio-gallery}}"


def render_custom_page_from_markdown_file(path_to_markdown_file: str):
    """
    Processes a markdown file and returns the rendered HTML content to be injected into custom pages.
    Also replaces custom tags found in the markdown with the appropriate content, e.g. {{pyfolio-carousel}} or {{pyfolio-gallery}}.
    Returns None if the file is not found or an error occurs during processing.
    """
    try:
        with open(path_to_markdown_file, "r", encoding="utf-8") as file:
            markdown_text = file.read()

        return render_custom_page_from_markdown_text(markdown_text, path_to_markdown_file)
    except FileNotFoundError:
        app_logger.error(f"Markdown file not found: {path_to_markdown_file}")
        return None
    except Exception as e:
        app_logger.error(f"Error processing markdown file [{path_to_markdown_file}]: {e}")
        return None


def render_custom_page_from_markdown_text(markdown_text: str, source_file_path: str | None = None):
    """
    Processes a markdown text and returns the rendered HTML content to be injected into custom pages.
    Also replaces custom tags found in the markdown with the appropriate content, e.g. {{pyfolio-carousel}} or {{pyfolio-gallery}}.
    Returns None if an error occurs during processing.
    """
    try:
        frontmatter_str, content_str = split_frontmatter_from_content(markdown_text)
        frontmatter_dict = process_frontmatter(frontmatter_str)

        # Provide a default title if none is specified
        if "title" not in frontmatter_dict:
            nameFromPath = source_file_path.split("/")[-1].split(".")[0]
            nameFromPath = nameFromPath.replace("_", " ").title()
            try:
                site_title = config_manager.get_config().get("metadata").get("title")
                nameFromPath = nameFromPath + " - " + site_title
            except:
                app_logger.warning("No site title found in config.toml")
            frontmatter_dict["title"] = nameFromPath

        preprocessed_markdown = apply_preprocessing_to_markdown(content_str)
        rendered_markdown = markdown.markdown(preprocessed_markdown, extensions=["nl2br"])

        # process the markdown text to inject carousel elements
        rendered_markdown = process_custom_pyfolio_tags(rendered_markdown)
        return render_template("text_page.jinja", rendered_markdown_content=rendered_markdown, frontmatter_dict=frontmatter_dict)
    except Exception as e:
        app_logger.error(f"Error processing markdown text: {e}")
        return None


def apply_preprocessing_to_markdown(markdown_text: str) -> str:
    """
    Applies preprocessing to a markdown text before rendering it.
    """

    # Respects multiple line breaks in the markdown text by replacing them with <br> tags
    processed_text = markdown_text.replace("\n\n", "<br>\n")

    return processed_text


def get_random_portfolio_image_elements(amount: int):
    image_elements = [element for element in Portfolio.get_instance().get_elements() if element.get_asset_type() == "image"]
    return random.sample(image_elements, k=min(amount, len(image_elements)))


def process_custom_pyfolio_tags(markdown_text: str):
    processed_markdown = markdown_text.replace(
        CAROUSEL_TAG, render_template("carousel_component.jinja", carousel_elements=get_random_portfolio_image_elements(3))
    )

    processed_markdown = processed_markdown.replace(
        GALLERY_TAG, render_template("gallery_component.jinja", portfolio_elements=Portfolio.get_instance().get_elements())
    )
    return processed_markdown


def split_frontmatter_from_content(markdown_text: str) -> tuple:
    """
    Splits the frontmatter from the content of a markdown document and returns a (frontmatter, content) strings tuple.
    """
    if not contains_a_frontmatter_block(markdown_text):
        return "", markdown_text

    lines = markdown_text.split("\n")
    frontmatter = "\n".join(lines[: lines.index("---", 1) + 1])
    content = "\n".join(lines[lines.index("---", 1) + 1 :])

    return frontmatter, content


def process_frontmatter(frontmatter_str: str):
    """
    Processes the frontmatter of a markdown document and returns the frontmatter as a dictionary.
    """
    if not contains_a_frontmatter_block(frontmatter_str):
        return {}

    frontmatterDictionary = {}
    lines = frontmatter_str.split("\n")
    for line in lines[1 : lines.index("---", 1)]:
        key, value = line.split(": ", 1)
        frontmatterDictionary[key] = value

    # Convert incorrectly structured arrays for html
    for key in frontmatterDictionary:
        if frontmatterDictionary[key].startswith("[") and frontmatterDictionary[key].endswith("]"):
            # Remove brackets
            frontmatterDictionary[key] = frontmatterDictionary[key].replace("[", "").replace("]", "").replace(", ", ",")
            # remove internal quotes
            frontmatterDictionary[key] = frontmatterDictionary[key].replace('"', "")
            print(frontmatterDictionary[key])

    return frontmatterDictionary


def contains_a_frontmatter_block(markdown_text: str):
    """
    Returns True if the markdown text contains a frontmatter block, False otherwise.
    """
    lines = markdown_text.split("\n")
    return lines[0] == "---" and "---" in lines[1:]
