"""
Search Tools Module - Day 3-4 Concepts
Provides search functionality for the AI agent
"""

from typing import List, Any


class SearchTool:
    """
    Encapsulates search functionality for the agent.
    Uses text search from minsearch index.
    """

    def __init__(self, index):
        """
        Initialize search tool with an index.

        Args:
            index: minsearch Index object
        """
        self.index = index

    def search(self, query: str) -> List[Any]:
        """
        Perform a text-based search on the index.

        Args:
            query (str): The search query string.

        Returns:
            List[Any]: A list of up to 5 search results returned by the index.
        """
        return self.index.search(query, num_results=5)
