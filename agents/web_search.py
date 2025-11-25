from duckduckgo_search import DDGS
import json

class WebSearch:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query, max_results=5):
        """
        Performs a web search and returns results.
        """
        print(f"Searching web for: {query}")
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def get_formatted_results(self, query):
        results = self.search(query)
        if not results:
            return "No results found."
        
        formatted = ""
        for i, r in enumerate(results):
            formatted += f"{i+1}. {r['title']}\n   {r['href']}\n   {r['body']}\n\n"
        return formatted

if __name__ == "__main__":
    # Test
    ws = WebSearch()
    print(ws.get_formatted_results("latest ai news"))
