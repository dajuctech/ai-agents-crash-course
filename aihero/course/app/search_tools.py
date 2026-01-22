from typing import List, Any

class SearchTool:
    def __init__(self, index):
        self.index = index
    
    def search(self, query: str) -> List[Any]:
        return self.index.search(query, num_results=5)