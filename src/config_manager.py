"""
This module reads the TOML configuration file and provides the configuration to the application.
It also injects relevant configuration into the Jinja2 templates.
"""

from flask import Flask, url_for
import toml

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
            print(f"Link dictionary does not have a target key: {link_dict}")
            continue

        if target.startswith("[") and target.endswith("]"):
            # Special target
            if target == "[home]":
                link_dict["target"] = "/"
            elif target == "[gallery]":
                link_dict["target"] = "/gallery"
            else:
                print(f"Unknown special target in link: {link_dict}")
                raise ValueError(f"Unknown special target in link: {link_dict}")
        elif "://" in target:
            # Absolute URL, nothing to change
            pass
        else:
            # Relative URL
            # link_dict["target"] = path_util.resolve_path(target)

            # Strip the ".md" portion
            link_dict["target"] = target[:-3]
            pass
