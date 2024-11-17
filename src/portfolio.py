import os

import path_util
from portfolio_element import PortfolioElement


class Portfolio:
    """
    The class that builds and holds the "metadata" of the portfolio built from the assets found in the portfolio folder.

    Paths are relative to the portfolio folder.
    """

    IGNORED_EXTENSIONS = [".md", ".txt"]

    def __init__(self):
        self._elements = self._discover_portfolio_elements()

        # DEBUG: Print the elements found in the portfolio
        print("Portfolio scan complete. Found the following elements:")
        print(self._elements)

    def _discover_portfolio_elements(self):
        """
        Parses the portfolio folder and returns a list of all the elements found in it.
        """
        elements = []
        scan_directory = path_util.resolve_path("portfolio")
        for directory, _, files in os.walk(scan_directory):
            for file in os.listdir(directory):
                absolute_file_path = path_util.resolve_path(os.path.join(directory, file))

                # Skip ignored extensions early
                if any(file.endswith(ext) for ext in self.IGNORED_EXTENSIONS):
                    print(f"Portfolio: Skipping non-asset file: {file}")
                    continue

                # Process valid asset files
                print(f"Portfolio: Including asset: {file}")
                new_element = PortfolioElement(absolute_asset_path=absolute_file_path)

                # Check for identifier collisions
                collision = next((element for element in elements if element.get_identifier() == new_element.get_identifier()), None)
                if collision:
                    print(
                        f"Multiple portfolio elements cannot have the same identifier:\n"
                        f"- {collision.get_absolute_asset_path()}\n"
                        f"- {new_element.get_absolute_asset_path()}\n"
                        f"{new_element.get_absolute_asset_path()} will be ignored."
                    )
                    continue
                elements.append(new_element)
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
