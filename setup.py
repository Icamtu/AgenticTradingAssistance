from setuptools import setup, find_packages # type: ignore

setup(
    name="Agentic-Trading-Assistant",
    version="0.1.0",
    author="Kamaleswar Mohanta",
    author_email="kamaleswarmohanta@outlook.com",
    description="An AI-powered trading assistant for stock market analysis and decision-making.",
    
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
                        "langchain",                        
                        "langgraph",
                        "tavily-python",
                        "polygon",
                        "langchain_community",
                        "langchain_google_genai",
                        "streamlit",
                        "fastapi[all]",
                        "uvicorn",
                        "langchain-pinecone",
                        "pypdf",

                    ]


)
