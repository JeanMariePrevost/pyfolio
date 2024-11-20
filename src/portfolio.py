import asyncio
import os
from pathlib import Path

import app_logger
import path_util
from portfolio_element import PortfolioElement


class Portfolio:
    """
    The class that builds and holds the "metadata" of the portfolio built from the assets found in the portfolio folder.

    Paths are relative to the portfolio folder.
    """

    __instance = None

    @staticmethod
    def get_instance():
        if Portfolio.__instance is None:
            Portfolio.__instance = Portfolio.__create_instance()  # Bypass the __new__ method to not raise an exception
            Portfolio.__instance.__init__()  # Initialize the instance manually as __new__ was bypassed
        return Portfolio.__instance

    @staticmethod
    def __create_instance():
        return object.__new__(Portfolio)

    def __new__(cls):
        raise Exception("Portfolio is a singleton. Use Portfolio.get_instance() to access the instance.")

    IGNORED_EXTENSIONS = [".md", ".txt"]

    def __init__(self):
        self._elements = self._discover_portfolio_elements()

        app_logger.info(f"Portfolio: Found {len(self._elements)} supported assets in the portfolio folder.")

    def _discover_portfolio_elements(self) -> list[PortfolioElement]:
        """
        Parses the portfolio folder synchronously but uses async for internal processing.
        Returns a list of all the elements found in the portfolio folder.
        """
        elements = []
        scan_directory = path_util.resolve_path("portfolio")

        try:
            # Non-recursive listing
            files = os.listdir(scan_directory)
        except FileNotFoundError:
            app_logger.error(f"Portfolio folder not found: {scan_directory}")
            return elements

        # Define async processing for a single file
        async def process_file(file):
            absolute_file_path = path_util.resolve_path(os.path.join(scan_directory, file))

            # Skip ignored extensions early
            if any(file.endswith(ext) for ext in self.IGNORED_EXTENSIONS):
                app_logger.debug(f"Portfolio initial scan: Skipping non-asset file: {file}")
                return None

            # Process valid asset files
            app_logger.debug(f"Portfolio initial scan: Including asset: {file}")
            new_element = PortfolioElement(absolute_asset_path=absolute_file_path)

            # Check for identifier collisions
            collision = next((element for element in elements if element.get_identifier() == new_element.get_identifier()), None)
            if collision:
                app_logger.warning(
                    f"Multiple portfolio elements cannot have the same identifier:\n"
                    f"- {collision.get_absolute_asset_path()}\n"
                    f"- {new_element.get_absolute_asset_path()}\n"
                    f"{new_element.get_absolute_asset_path()} will not be included."
                )
                return None

            return new_element

        # Synchronous wrapper for async processing
        async def process_all_files():
            tasks = [process_file(file) for file in files if Path(scan_directory, file).is_file()]
            results = await asyncio.gather(*tasks)
            return [result for result in results if result]

        # Run the async processing
        elements = asyncio.run(process_all_files())
        return elements

    def get_elements(self):
        return self._elements

    def get_element_before(self, element: PortfolioElement) -> PortfolioElement:
        """Returns the element before the given element in the portfolio."""
        index = self._elements.index(element)
        if index == 0:
            return None
        return self._elements[index - 1]

    def get_element_after(self, element: PortfolioElement) -> PortfolioElement:
        """Returns the element after the given element in the portfolio."""
        index = self._elements.index(element)
        if index == len(self._elements) - 1:
            return None
        return self._elements[index + 1]

    def get_element_by_asset_path(self, absolute_asset_path: str) -> PortfolioElement:
        """Finds a PortfolioElement by its absolute asset path."""
        for element in self._elements:
            if element.get_identifier() == absolute_asset_path:
                return element
        return None

    def get_element_by_identifier(self, asset_identifier: str) -> PortfolioElement:
        """Finds a PortfolioElement by its identifier, i.e. the relative path from the portfolio folder, excluding extensions."""
        for element in self._elements:
            if element.get_identifier() == asset_identifier:
                return element
        return None
