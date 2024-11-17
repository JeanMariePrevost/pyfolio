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
            for file in files:
                if not any(file.endswith(ext) for ext in self.IGNORED_EXTENSIONS):
                    abs_path = os.path.join(directory, file)
                    elements_with_same_name = [element for element in elements if element.get_absolute_asset_path() == abs_path]
                    if len(elements_with_same_name) == 0:
                        elements.append(PortfolioElement(absolute_asset_path=abs_path))
                    else:
                        raise ValueError(
                            f"Multiple portfolio elements cannot have the same name: {abs_path} and {elements_with_same_name[0].get_absolute_asset_path()}"
                        )
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
