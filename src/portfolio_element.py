import os


class PortfolioElement:
    """
    Represents a single portfolio element.

    All paths are relative to the portfolio folder.
    """

    def __init__(self, asset_path: str):
        self._asset_path = asset_path

    def get_asset_identifier(self) -> str:
        """The path of the asset, relative to the portfolio folder, without the file extension."""
        return os.path.splitext(self._asset_path)[0]

    def get_asset_path(self) -> str:
        return self._asset_path

    def get_asset_text(self) -> str:
        # If file exists on server, read and return its contents, otherwise return an empty string
        asset_text_file_path = self.get_asset_identifier() + ".md"
        if os.path.isfile(asset_text_file_path):
            with open(asset_text_file_path, "r") as file:
                return file.read()
        else:
            return ""
