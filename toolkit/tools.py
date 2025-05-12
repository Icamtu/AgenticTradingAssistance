import os
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults
from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_community.agent_toolkits.polygon.toolkit import PolygonToolkit
from langchain_community.tools.bing_search import BingSearchResults 
from data_models.models import RagToolSchema
from langchain_pinecone import PineconeVectorStore
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from dotenv import load_dotenv
from pinecone import Pinecone
import streamlit as st
from langchain_core.tools import BaseTool
from typing import List, Dict, Any, Callable, Optional, Union

load_dotenv()

api_wrapper = PolygonAPIWrapper()
model_loader=ModelLoader()
config = load_config()



@tool(args_schema=RagToolSchema)
def retriever_tool(question: str):
    """Use this tool when you need to retrieve information from a knowledge base."""
    try:
        # Import model loader inside function to avoid circular imports
        from utils.model_loader import ModelLoader
        model_loader = ModelLoader()
        
        pinecone_api_key = os.getenv("PINECONE_API_KEY", st.session_state.get("PINECONE_API_KEY", ""))
        if not pinecone_api_key:
            return "Error: Pinecone API key not found."
        
        pc = Pinecone(api_key=pinecone_api_key)
        vector_store = PineconeVectorStore(
            index=pc.Index(config["vector_db"]["index_name"]), 
            embedding=model_loader.load_embeddings()
        )
        
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": config["retriever"]["top_k"],
                "score_threshold": config["retriever"]["score_threshold"]
            }
        )
        
        retriever_result = retriever.invoke(question)
        return retriever_result
    except Exception as e:
        return f"Error using retriever tool: {str(e)}"

@tool(description="Search the web for information using Tavily")
def tavily_tool(question: str):
    """Use this tool to search the web for recent or specific information."""
    try:
       
        tavily_api_key = os.getenv("TAVILY_API_KEY",st.session_state.get("PINECONE_API_KEY", ""))
        
        
        search_tool = TavilySearchResults(
            api_key=tavily_api_key, 
            max_results=config["tools"]["tavily"]["max_results"],
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True
        )
        
        results = search_tool.invoke(question)
        return results
    except Exception as e:
        return f"Error using Tavily search: {str(e)}. Please ensure the Tavily API key is valid and the service is available."

@tool(description="Get financial market data including stock prices, company financials, and market news")
def Polygon_tool(question: str):
    """Use this tool for financial data requests like stock prices, company information, and market news.
    
    This tool automatically routes your query to the appropriate financial data API. Examples:
    - "Get the stock price for AAPL over the last week"
    - "Find the latest news about Tesla"
    - "What were the daily aggregates for GOOGL from May 10-17?"
    """
    try:
        polygon_api_key = os.getenv("POLYGON_API_KEY")
        if not polygon_api_key:
            return "Error: Polygon API key not found."
        
        api_wrapper = PolygonAPIWrapper()
        toolkit = PolygonToolkit.from_polygon_api_wrapper(api_wrapper)
        tools = toolkit.get_tools()
        
        # Create a dictionary of polygon tools by name
        polygon_tools = {tool.name: tool for tool in tools}
        
        # Determine which tool to use based on the query
        result = _route_query_to_polygon_tool(question, polygon_tools)
        return result
    except Exception as e:
        return f"Error using Polygon tools: {str(e)}"

def _route_query_to_polygon_tool(question: str, polygon_tools: Dict[str, BaseTool]) -> Any:
    """Route the financial query to the appropriate Polygon tool."""
    query_lower = question.lower()
    
    # Extract ticker - used by most tools
    import re
    ticker_match = re.search(r'\b([A-Z]{1,5})\b', question)
    ticker = ticker_match.group(1) if ticker_match else None
    
    if not ticker:
        return "No stock ticker found in query. Please specify a stock symbol like AAPL, GOOGL, etc."
    
    # Handle news requests
    if "news" in query_lower and "polygon_ticker_news" in polygon_tools:
        try:
            return polygon_tools["polygon_ticker_news"].invoke({"ticker": ticker})
        except Exception as e:
            return f"Error getting news for {ticker}: {str(e)}"
    
    # Handle financials requests
    if any(kw in query_lower for kw in ["financial", "statement", "earnings", "revenue", "profit"]):
        if "polygon_ticker_financials" in polygon_tools:
            try:
                return polygon_tools["polygon_ticker_financials"].invoke({"ticker": ticker})
            except Exception as e:
                return f"Error getting financials for {ticker}: {str(e)}"
    
    # Handle aggregates/price data requests (default)
    if "polygon_aggregates" in polygon_tools:
        try:
            params = _extract_aggregate_params(question, ticker)
            
            # Ensure timespan_multiplier is an integer
            if "timespan_multiplier" in params:
                params["timespan_multiplier"] = int(params["timespan_multiplier"])
            
            return polygon_tools["polygon_aggregates"].invoke(params)
        except Exception as e:
            return f"Error getting price data for {ticker}: {str(e)}"
    
    return f"Unable to process financial query for {ticker}. Please try a different query format."

def _extract_aggregate_params(question: str, ticker: str) -> Dict[str, Any]:
    """Extract parameters for aggregates API from natural language."""
    from datetime import datetime, timedelta
    
    # Default parameters
    params = {
        "ticker": ticker,
        "timespan": "day",
        "timespan_multiplier": 1,
        "to_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Set from_date to 7 days ago by default
    from_date = datetime.now() - timedelta(days=7)
    params["from_date"] = from_date.strftime("%Y-%m-%d")
    
    query_lower = query.lower()
    
    # Look for date ranges
    if "last week" in query_lower or "past week" in query_lower:
        from_date = datetime.now() - timedelta(days=7)
        params["from_date"] = from_date.strftime("%Y-%m-%d")
    elif "last month" in query_lower or "past month" in query_lower:
        from_date = datetime.now() - timedelta(days=30)
        params["from_date"] = from_date.strftime("%Y-%m-%d")
    elif "last year" in query_lower or "past year" in query_lower:
        from_date = datetime.now() - timedelta(days=365)
        params["from_date"] = from_date.strftime("%Y-%m-%d")
        
    # Look for timespan
    if any(kw in query_lower for kw in ["minute", "hourly", "hour"]):
        params["timespan"] = "hour"
    elif any(kw in query_lower for kw in ["weekly", "week"]):
        params["timespan"] = "week"
    elif any(kw in query_lower for kw in ["monthly", "month"]):
        params["timespan"] = "month"
        
    # Try to extract specific date ranges using regex
    # This is a simple implementation - could be enhanced
    import re
    date_pattern = r'from (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})'
    date_match = re.search(date_pattern, question)
    if date_match:
        params["from_date"] = date_match.group(1)
        params["to_date"] = date_match.group(2)
    
    return params