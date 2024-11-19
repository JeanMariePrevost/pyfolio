"""
This module reads the TOML configuration file and provides the configuration to the application.
It also injects relevant configuration into the Jinja2 templates.
"""

from flask import Flask, url_for
import toml

import app_logger
import path_util

_config_dict = None


def load_configs(app: Flask):
    """
    Loads the configurations from the config.toml file.
    """
    config_path = path_util.resolve_path("config.toml")
    try:
        with open(config_path, "r") as config_file:
            global _config_dict
            _config_dict = toml.load(config_file)
            resolve_config_link_targets()
            parse_style_configs()
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at path: {config_path}")
    except toml.TomlDecodeError as e:
        raise ValueError(f"Error decoding the configuration file: {e}")
    except Exception as e:
        raise e

    # NOTE: Has to be inside the function because of temporal coupling with the app context having to be instantiated
    @app.context_processor
    def inject_config():
        """
        Injects the configuration into the Jinja2 templates.
        """
        return dict(config=_config_dict)


def parse_style_configs():
    """
    Parses the style configurations from the configuration dictionary to make it adequate for the Jinja2 templates and/or add extra behaviors
    """
    global _config_dict

    try:
        # Make None all empty strings or values of "default" as they are explicit "non-overrides"
        for key, value in _config_dict["style"].items():
            if value == "" or value == "default":
                _config_dict["style"] = None
    except KeyError:
        app_logger.warning("No style configuration found in the configuration file. All deleted/disabled?")
        # create an empty style configuration dictionary
        _config_dict["style"] = {}


def resolve_config_link_targets():
    """
    Resolves the link targets in the configuration to the correct URL (e.g. relative and special targets)
    """
    global _config_dict
    # Resolve the relative paths in both top_links and footer_links
    for link_dict in _config_dict["top_link"] + _config_dict["footer_link"]:
        try:
            target = link_dict["target"]
        except KeyError:
            app_logger.error(f"Link dictionary does not have a target key: [{link_dict}]. Typo or incomplete configuration?")
            continue

        if target.startswith("[") and target.endswith("]"):
            # Special target
            if target == "[home]":
                link_dict["target"] = "/"
            elif target == "[gallery]":
                link_dict["target"] = "/gallery"
            else:
                app_logger.error(f"Target is not a valid link nor a valid special tag: {link_dict}")
                raise ValueError(f"Invalid special target: {target}")
        elif "://" in target:
            # Absolute URL, nothing to change
            pass
        elif target.endswith(".md"):
            # Relative URL
            # Strip the ".md" portion to get the correct URL
            link_dict["target"] = target[:-3]
            pass
        else:
            app_logger.error(f"Target is not of a valid format: {link_dict}")
            raise ValueError(f"Invalid target: {target}")
