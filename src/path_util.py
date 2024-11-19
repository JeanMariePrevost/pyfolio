"""Utility module to reduce confusion about paths and CWD"""

import os

# Determine the project root based on the location of this file
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def resolve_path(relative_path: str) -> str:
    """
    Resolve a relative path into an absolute path within the project root.

    :param relative_path: Path relative to the project root.
    :return: Absolute path.

    e.g. resolve_path("src/app.py") -> "/path/to/project/src/app.py"
    """
    return os.path.join(PROJECT_ROOT, relative_path)


# Function to derive a relative path from a base directory
def derive_relative_path(absolute_path: str, base_directory: str) -> str:
    """
    Derive a relative path from a given absolute path with respect to a base directory.

    :param absolute_path: The full absolute path to process.
    :param base_directory: The base directory to calculate the relative path from.
    :return: The relative path derived from the base directory.
    """
    if not absolute_path.startswith(base_directory):
        raise ValueError(f"The path '{absolute_path}' is not within the base directory '{base_directory}'.")
    return os.path.relpath(absolute_path, base_directory)


def file_exists_relative(file_path: str) -> bool:
    """
    Check if a file exists at the given path.

    :param file_path: Path to the file.
    :return: True if the file exists, False otherwise.
    """
    return os.path.isfile(resolve_path(file_path))
