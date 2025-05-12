import os
from langchain.tools import tool
from langchain_community.tools import TavilySearchResults
from langchain_community.tools.polygon.financials import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults 
from data_models.models import RagToolSchema
from langchain_pinecone import PineconeVectorStore
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from dotenv import load_dotenv
from pinecone import Pinecone
import streamlit as st
import os

load_dotenv()

api_wrapper = PolygonAPIWrapper()
model_loader=ModelLoader()
config = load_config()

@tool(args_schema=RagToolSchema)
def retriever_tool(question):
    """this is retriever tool"""
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=pinecone_api_key)
    vector_store = PineconeVectorStore(index=pc.Index(config["vector_db"]["index_name"]), 
                            embedding= model_loader.load_embeddings())
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": config["retriever"]["top_k"] , "score_threshold": config["retriever"]["score_threshold"]},
    )
    retriever_result=retriever.invoke(question)
    
    return retriever_result

@tool(description="this is tavily search tool to search web")
def tavily_search_tool():
    """this is tavily tool to search web
    
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY", st.session_state.get("TAVILY_API_KEY", ""))
    max_results=config["tavily"]["max_results"]
    search_depth="advanced"
    include_answer=True
    include_raw_content=True
    
    return TavilySearchResults(
        api_key=tavily_api_key, max_results=max_results, search_depth=search_depth, include_answer=include_answer, include_raw_content=include_raw_content)

@tool(description= """ This is polygon financials tool for real-time financial data""")
def Polygon_tool():
     """ This is polygon financials tool for real-time financial data"""
     return PolygonFinancials(api_wrapper=api_wrapper)
