import os


class PortfolioElement:
    """
    Represents a single portfolio element.
    All paths are relative to the portfolio folder.
    """

    def __init__(self, relative_asset_path: str):
        self._relative_asset_path = relative_asset_path

    def get_asset_identifier(self) -> str:
        """The path of the asset, relative to the portfolio folder, without the file extension."""
        return os.path.splitext(self._relative_asset_path)[0]

    def get_extension(self) -> str:
        """Return the file extension of the asset."""
        return os.path.splitext(self._relative_asset_path)[1]

    def get_asset_type(self) -> str:
        """Return the type of the asset based on the file extension."""
        extension = self.get_extension()
        if extension in [".jpg", ".png", ".gif"]:
            return "image"
        elif extension in [".mp4", ".webm"]:
            return "video"
        else:
            return "unsupported"

    def get_asset_path(self) -> str:
        """Return the relative asset path."""
        return self._relative_asset_path

    def get_file_name(self) -> str:
        """Return just the file name without the directory."""
        return os.path.basename(self._relative_asset_path)

    def get_absolute_url(self, base_url: str = "/portfolio/") -> str:
        """Return the absolute URL for the asset."""
        return base_url + self._relative_asset_path

    def get_asset_text(self) -> str:
        """Return the markdown text content if available, or an empty string."""
        asset_text_file_path = self.get_asset_identifier() + ".md"
        if os.path.isfile(asset_text_file_path):
            with open(asset_text_file_path, "r") as file:
                return file.read()
        else:
            return self.get_file_name()
