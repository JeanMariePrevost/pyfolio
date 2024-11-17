import os


class Portfolio:
    """
    The class that builds and holds the "metadata" of the portfolio built from the assets found in the portfolio folder.

    Paths are relative to the portfolio folder.
    """

    IGNORED_EXTENSIONS = [".md", ".txt"]

    def __init__(self):
        self.elements = self._discover_portfolio_elements()

        # DEBUG: Print the elements found in the portfolio
        print("Portfolio scan complete. Found the following elements:")
        print(self.elements)

    def _discover_portfolio_elements(self):
        """
        Parses the portfolio folder and returns a list of all the elements found in it.
        """
        elements = []
        scan_directory = os.path.join(os.path.dirname(__file__), "portfolio")  # Finds the portfolio folder relative to the script file
        for subdirectory, _, files in os.walk(scan_directory):
            for file in files:
                if not any(file.endswith(ext) for ext in self.IGNORED_EXTENSIONS):
                    elements.append(os.path.relpath(os.path.join(subdirectory, file), scan_directory))
        return elements
