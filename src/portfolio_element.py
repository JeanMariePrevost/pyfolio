import os

import markdown

import path_util


class PortfolioElement:
    """
    Represents a single portfolio element.
    All paths are relative to the portfolio folder.
    """

    def __init__(self, absolute_asset_path: str):
        self._absolute_asset_path = absolute_asset_path

    def get_path_relative_to_portfolio(self) -> str:
        return path_util.derive_relative_path(self._absolute_asset_path, path_util.resolve_path("portfolio"))

    def get_extension(self) -> str:
        """Return the file extension of the asset."""
        return os.path.splitext(self._absolute_asset_path)[1]

    def get_asset_type(self) -> str:
        """Return the type of the asset based on the file extension."""
        extension = self.get_extension()
        if extension in [".jpg", ".png", ".gif"]:
            return "image"
        elif extension in [".mp4", ".webm"]:
            return "video"
        else:
            return "unsupported"

    def get_absolute_asset_path(self) -> str:
        """Return the absolute asset path."""
        return self._absolute_asset_path

    def get_file_name(self) -> str:
        """Return just the file name without the directory."""
        return os.path.basename(self._absolute_asset_path)

    def get_file_name_without_extension(self) -> str:
        """Return just the file name without the directory and extension."""
        return os.path.splitext(self.get_file_name())[0]

    def get_element_page_url(self) -> str:
        """Return the absolute URL for the asset."""
        return "/portfolio/" + self.get_file_name_without_extension()

    def get_caption_html(self) -> str:
        """Returns the content of the markdown caption file rendered as HTML."""
        raw_markdown = self.get_caption_raw()
        return markdown.markdown(raw_markdown)

    def get_caption_raw(self) -> str:
        """Return the content of the relevant md file if present, an empty string otherwise."""
        asset_text_file_path = self.get_caption_file_path()
        if os.path.isfile(asset_text_file_path):
            with open(asset_text_file_path, "r") as file:
                return file.read()
        else:
            return self.get_file_name_without_extension()

    def get_identifier(self) -> str:
        """Return the identifier of the asset, which is the directories below /portfolio/ and the filename without extension."""
        relative_path = path_util.derive_relative_path(self._absolute_asset_path, path_util.resolve_path("portfolio"))
        return os.path.splitext(relative_path)[0]

    def get_caption_file_path(self) -> str:
        """Return the path to the optional caption file."""
        return os.path.splitext(self.get_absolute_asset_path())[0] + ".md"
