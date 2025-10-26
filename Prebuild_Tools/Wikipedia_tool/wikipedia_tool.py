"""
Wikipedia Tool for Codemni Agents

This module provides a Wikipedia search and retrieval tool that allows
Codemni agents to access Wikipedia content programmatically.
"""

import wikipedia
from typing import Optional, Dict, Any


class WikipediaTool:
    """
    A tool for searching and retrieving content from Wikipedia.
    
    This tool provides methods to:
    - Search Wikipedia articles
    - Get article summaries
    - Retrieve full article content
    - Get page information
    
    Example:
        wiki = WikipediaTool()
        
        # Search for topics
        results = wiki.search("Python programming")
        
        # Get a summary
        summary = wiki.get_summary("Python (programming language)", sentences=3)
        
        # Get full content
        content = wiki.get_page_content("Artificial Intelligence")
    """
    
    def __init__(self, language: str = "en"):
        """
        Initialize the Wikipedia tool.
        
        Args:
            language: Wikipedia language code (default: "en" for English)
        """
        self.language = language
        wikipedia.set_lang(language)
    
    def search(self, query: str, results: int = 10) -> list:
        """
        Search Wikipedia for articles matching the query.
        
        Args:
            query: Search query string
            results: Maximum number of results to return (default: 10)
            
        Returns:
            List of article titles matching the query
            
        Example:
            >>> wiki = WikipediaTool()
            >>> wiki.search("quantum computing")
            ['Quantum computing', 'Quantum computer', 'Timeline of quantum computing', ...]
        """
        try:
            search_results = wikipedia.search(query, results=results)
            return search_results
        except Exception as e:
            return [f"Error searching Wikipedia: {str(e)}"]
    
    def get_summary(self, title: str, sentences: int = 3) -> str:
        """
        Get a summary of a Wikipedia article.
        
        Args:
            title: Title of the Wikipedia article
            sentences: Number of sentences to include in summary (default: 3)
            
        Returns:
            Summary text of the article
            
        Example:
            >>> wiki = WikipediaTool()
            >>> wiki.get_summary("Machine Learning", sentences=2)
            'Machine learning (ML) is a field of study in artificial intelligence...'
        """
        try:
            summary = wikipedia.summary(title, sentences=sentences, auto_suggest=True)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            # When multiple pages match, return options
            options = ", ".join(e.options[:5])
            return f"Multiple articles found. Please be more specific. Options include: {options}"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{title}'. Try searching first."
        except Exception as e:
            return f"Error retrieving summary: {str(e)}"
    
    def get_page_content(self, title: str) -> str:
        """
        Get the full content of a Wikipedia article.
        
        Args:
            title: Title of the Wikipedia article
            
        Returns:
            Full text content of the article
            
        Example:
            >>> wiki = WikipediaTool()
            >>> content = wiki.get_page_content("Neural Network")
        """
        try:
            page = wikipedia.page(title, auto_suggest=True)
            return page.content
        except wikipedia.exceptions.DisambiguationError as e:
            options = ", ".join(e.options[:5])
            return f"Multiple articles found. Please be more specific. Options include: {options}"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{title}'. Try searching first."
        except Exception as e:
            return f"Error retrieving page content: {str(e)}"
    
    def get_page_info(self, title: str) -> Dict[str, Any]:
        """
        Get detailed information about a Wikipedia article.
        
        Args:
            title: Title of the Wikipedia article
            
        Returns:
            Dictionary containing page information (title, url, summary, categories, links)
            
        Example:
            >>> wiki = WikipediaTool()
            >>> info = wiki.get_page_info("Deep Learning")
            >>> print(info['url'])
        """
        try:
            page = wikipedia.page(title, auto_suggest=True)
            return {
                "title": page.title,
                "url": page.url,
                "summary": page.summary,
                "categories": page.categories,
                "links": page.links[:20],  # Limit links to first 20
                "references": len(page.references)
            }
        except wikipedia.exceptions.DisambiguationError as e:
            options = ", ".join(e.options[:5])
            return {"error": f"Multiple articles found. Options include: {options}"}
        except wikipedia.exceptions.PageError:
            return {"error": f"No Wikipedia page found for '{title}'."}
        except Exception as e:
            return {"error": f"Error retrieving page info: {str(e)}"}
    
    def quick_lookup(self, query: str) -> str:
        """
        Quick lookup that searches and returns a summary in one call.
        This is the most convenient method for agents.
        
        Args:
            query: Search query or article title
            
        Returns:
            Summary of the most relevant article
            
        Example:
            >>> wiki = WikipediaTool()
            >>> result = wiki.quick_lookup("Albert Einstein")
        """
        try:
            # First try direct summary (handles auto-suggest)
            summary = wikipedia.summary(query, sentences=5, auto_suggest=True)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            # If multiple results, try the first option
            try:
                first_option = e.options[0]
                summary = wikipedia.summary(first_option, sentences=5)
                return f"Found: {first_option}\n\n{summary}"
            except:
                options = ", ".join(e.options[:5])
                return f"Multiple articles found: {options}. Please be more specific."
        except wikipedia.exceptions.PageError:
            # If not found, try searching first
            try:
                search_results = wikipedia.search(query, results=1)
                if search_results:
                    summary = wikipedia.summary(search_results[0], sentences=5)
                    return f"Found: {search_results[0]}\n\n{summary}"
                else:
                    return f"No Wikipedia articles found for '{query}'."
            except:
                return f"No Wikipedia articles found for '{query}'."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def add_to_agent(self, agent) -> None:
        """
        Add all Wikipedia tools to a Codemni agent.
        
        Args:
            agent: A Codemni agent instance (ToolCallingAgent, etc.)
            
        Example:
            >>> from Agents.TOOL_CALLING_AGENT import Create_ToolCalling_Agent
            >>> from llm.OpenAI_llm import Create_OpenAI_LLM
            >>> from Prebuild_Tools.Wikipedia_tool import WikipediaTool
            >>> 
            >>> llm = Create_OpenAI_LLM(api_key="your-key", model="gpt-4")
            >>> agent = Create_ToolCalling_Agent(llm=llm, verbose=True)
            >>> wiki = WikipediaTool()
            >>> wiki.add_to_agent(agent)
            >>> 
            >>> response = agent.invoke("Tell me about quantum computing")
        """
        # Add wikipedia_search tool
        agent.add_tool(
            name="wikipedia_search",
            description="Search Wikipedia for articles. Returns a list of article titles matching the search query. Use this to find relevant Wikipedia pages. Parameters: query (str), results (int, default=10)",
            function=self.search
        )
        
        # Add wikipedia_summary tool
        agent.add_tool(
            name="wikipedia_summary",
            description="Get a summary of a Wikipedia article. Provide the article title to get a concise summary (default 3 sentences). Use this for quick information retrieval. Parameters: title (str), sentences (int, default=3)",
            function=self.get_summary
        )
        
        # Add wikipedia_content tool
        agent.add_tool(
            name="wikipedia_content",
            description="Get the full content of a Wikipedia article. Provide the article title to retrieve complete article text. Use this when you need detailed information. Parameters: title (str)",
            function=self.get_page_content
        )
        
        # Add wikipedia_info tool
        agent.add_tool(
            name="wikipedia_info",
            description="Get detailed information about a Wikipedia article including title, URL, summary, categories, and links. Use this to get comprehensive metadata about a page. Parameters: title (str)",
            function=self.get_page_info
        )
        
        # Add wikipedia_quick_lookup tool (most convenient)
        agent.add_tool(
            name="wikipedia_quick_lookup",
            description="Quick Wikipedia lookup that searches and returns a summary in one call. This is the most convenient method - just provide a topic or query and get a summary. Use this for general Wikipedia queries. Parameters: query (str)",
            function=self.quick_lookup
        )


# Convenience function for quick integration
def create_wikipedia_tool(language: str = "en") -> WikipediaTool:
    """
    Factory function to create a WikipediaTool instance.
    
    Args:
        language: Wikipedia language code (default: "en")
        
    Returns:
        WikipediaTool instance
        
    Example:
        >>> wiki = create_wikipedia_tool()
        >>> result = wiki.quick_lookup("Python programming")
    """
    return WikipediaTool(language=language)
