---
title: AgenticTradingAssistant
emoji: 🐨
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 5.29.0
app_file: streamlit_ui.py
pinned: false
license: mit
short_description: Refined AgenticTradingAssistant
---





# Agentic Trading Assistance

A project to assist with trading decisions using AI agents.

## Project Overview

The Agentic Trading Assistant is designed to provide AI-powered assistance for trading decisions. It leverages a Large Language Model (LLM) equipped with a suite of tools to offer comprehensive and context-aware responses to user queries.

Key features include:
- **Trading-related Question Answering:** Addresses user questions about trading strategies, market analysis, and financial instruments.
- **Advanced Tool Integration:** Utilizes a retriever for searching through user-uploaded documents, Polygon for accessing real-time and historical financial data, and Tavily for performing web searches to gather relevant information.
- **Contextual Document Uploads:** Allows users to upload their own documents, enabling the assistant to provide responses that are tailored to the specific context provided.
- **LangGraph-Powered Workflow:** The agent's decision-making process and tool utilization are defined and managed using LangGraph.
- **Web Interface:** Features a FastAPI backend for robust API services and a Streamlit frontend for an interactive user experience.

## Architecture

The Agentic Trading Assistant is composed of several key components that work together to provide its functionality:

- **FastAPI Backend (`main.py`):** This component serves as the entry point for API requests. It handles incoming queries from the user and manages file uploads, interacting with the agent workflow and data ingestion pipeline as needed.
- **Streamlit UI (`streamlit_ui.py`):** The Streamlit application provides a user-friendly web interface. Users can submit their trading-related questions, upload documents for contextual analysis, and view the assistant's responses through this UI.
- **Agent Workflow (`agent/workflow.py`):** This is the core of the assistant. It's built using LangGraph and orchestrates the Large Language Model (LLM) along with a suite of tools. These tools include:
    - `retriever_tool`: For fetching relevant information from user-uploaded documents.
    - `Polygon_tool`: For accessing financial data (e.g., stock prices, market news).
    - `tavily_tool`: For performing web searches to gather external information.
    The workflow processes user queries, decides which tools to use, and generates a comprehensive response.
- **Data Ingestion (`data_ingestion/ingestion_pipeline.py`):** This pipeline is responsible for processing files uploaded by the user. It prepares these documents (e.g., by chunking, embedding) and stores them in a vector database, making them searchable by the `retriever_tool`.
- **Configuration (`config/config.yaml` and `.env`):** Application settings, including API keys for external services (Polygon, Tavily, LLM providers), model parameters, and other operational configurations are managed through a `config.yaml` file and environment variables stored in a `.env` file.

## Setup

### Start the Backend Server

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Start the User Interface

```
streamlit run streamlit_ui.py
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Create Conda Environment

```
conda create -p env python=3.10 -y
```

### Activate Conda Environment (Command Prompt)

```
conda activate <env_path>
```

### Activate Conda Environment (Git Bash)

```
source activate ./env
```

## Configuration

Proper configuration is essential for the Agentic Trading Assistant to function correctly. This involves setting up environment variables for API keys and optionally adjusting parameters in the `config/config.yaml` file.

### Environment Variables (`.env` file)

The application requires a `.env` file in the root project directory to store sensitive API keys. Create this file and add the following keys with your respective values:

```
POLYGON_API_KEY=your_polygon_api_key
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

-   **`POLYGON_API_KEY`**: Used to access financial data (stock prices, news, etc.) from Polygon.io.
-   **`GOOGLE_API_KEY`**: Required for accessing Google AI services, such as Google's Large Language Models (e.g., Gemini).
-   **`TAVILY_API_KEY`**: Enables the Tavily search tool for performing web searches to gather external information.
-   **`GROQ_API_KEY`**: Required for using Large Language Models provided by Groq.
-   **`PINECONE_API_KEY`**: Used for connecting to the Pinecone vector database, which stores and retrieves document embeddings.

### YAML Configuration (`config/config.yaml`)

The `config/config.yaml` file contains settings for various components of the application, allowing you to customize its behavior. You might want to adjust these settings based on your specific needs or preferences.

Key configuration groups include:

-   **`vector_db`**: Defines settings for the vector database.
    ```yaml
    vector_db:
      index_name: "trading-bot"
    ```
-   **`retriever`**: Contains parameters for the document retriever.
    ```yaml
    retriever:
      top_k: 3
      score_threshold: 0.5
    ```
-   **`embedding_model`**: Specifies the text embedding model to be used.
    ```yaml
    embedding_model:
      provider: "google"
      model_name: "models/text-embedding-004"
    ```
-   **`llm`**: Configures the Large Language Models used by the agent.
    ```yaml
    llm:
      google:
        provider: "google"
        model_name: "gemini-2.0-flash"
      groq:
        provider: "groq"
        model_name: "deepseek-r1-distill-llama-70b"
    ```
-   **`tools`**: Settings for specific tools integrated with the agent. For example, the `tavily` tool configuration might specify the maximum number of search results to consider.
    ```yaml
    tools:
      tavily:
        max_results: 5
    ```

Note: The examples above reflect the structure in the project's `config/config.yaml` file. Refer to the actual file for the most current and complete configuration options.

## Usage

Once the setup is complete, follow these steps to use the Agentic Trading Assistant:

1.  **Activate the Environment:**
    Ensure your Conda environment is activated. Refer to the "Activating the Environment" subsection within the "Setup" section for the correct command based on your shell (cmd or Git Bash).

2.  **Run the Backend Service:**
    Start the FastAPI server. Open your terminal, navigate to the project directory, and run:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
    This will make the backend API accessible.

3.  **Run the User Interface:**
    In a new terminal window or tab (while the backend is still running), start the Streamlit application. Navigate to the project directory and run:
    ```bash
    streamlit run streamlit_ui.py
    ```
    This will open the application in your web browser.

4.  **Interacting with the Application:**
    *   **Ask Questions:** Use the chat interface in the Streamlit UI to ask trading-related questions.
    *   **Upload Documents:** You can upload documents (e.g., PDF, DOCX) through the Streamlit UI. Alternatively, you can use the `/upload` API endpoint provided by the FastAPI backend. The agent will use the content of these documents to provide more contextually relevant answers.
    *   **Get Answers:** The agent will process your query using its Large Language Model (LLM) and integrated tools (Polygon for financial data, Tavily for web searches, and a retriever for your uploaded documents) to generate a comprehensive response.

## Dependencies

The Agentic Trading Assistant relies on several key Python libraries and frameworks to deliver its functionality. Below is a list of the most important ones:

-   **`langchain`**: The core library used for developing applications powered by Large Language Models (LLMs). It provides modules and abstractions for interacting with LLMs, managing prompts, and chaining components.
-   **`langgraph`**: An extension of Langchain, used to build robust and stateful multi-agent applications. It allows defining agent workflows as graphs.
-   **`tavily-python`**: The official Python client for the Tavily Search API, enabling the agent to perform web searches and gather external information.
-   **`polygon`**: The Python client for Polygon.io, used to fetch real-time and historical financial data, such as stock prices, aggregates, and news.
-   **`streamlit`**: A fast and easy way to build interactive web applications for Python. It's used for creating the user interface of the trading assistant.
-   **`fastapi`**: A modern, fast (high-performance) web framework for building APIs with Python. It's used for the backend services of the application.
-   **`uvicorn`**: An ASGI (Asynchronous Server Gateway Interface) server, used to run the FastAPI application.
-   **`langchain-pinecone`**: Provides integration with the Pinecone vector database, allowing for efficient storage and retrieval of document embeddings for the retriever tool.
-   **Document Loaders (`pypdf`, `pymupdf`, `docx2txt`):** These libraries are used to load and extract text content from various document formats (PDFs, DOCX files) during the data ingestion process. `pypdf` and `pymupdf` handle PDF files, while `docx2txt` is used for Microsoft Word documents.

For a complete list of all dependencies and their specific versions, please refer to the `requirements.txt` file in the root of the project. You can install all necessary dependencies by running `pip install -r requirements.txt`.

## Troubleshooting

This section addresses common issues you might encounter while setting up or running the Agentic Trading Assistant.

-   **API Key Issues:**
    *   **Symptom:** Errors related to authentication (e.g., "401 Unauthorized", "Invalid API Key"), or tools not working as expected (e.g., web searches return no results, financial data is missing, LLM calls fail).
    *   **Solution:**
        1.  Carefully double-check that all API keys (`POLYGON_API_KEY`, `GOOGLE_API_KEY`, `TAVILY_API_KEY`, `GROQ_API_KEY`, `PINECONE_API_KEY`) in your `.env` file are correct and valid.
        2.  Ensure there are no extra spaces or characters around the keys or their values.
        3.  Verify that the API keys have the necessary permissions or are enabled for the services they are intended for.
        4.  Make sure the `.env` file is located in the root directory of the project and is correctly formatted (e.g., `KEY=VALUE`).

-   **Python Environment and Dependencies:**
    *   **Symptom:** `ModuleNotFoundError` when trying to run the application, or unexpected behavior/errors from specific libraries.
    *   **Solution:**
        1.  Ensure your Conda environment (e.g., `env`) is activated. You should see the environment name in your terminal prompt (e.g., `(env) C:\Users\YourUser\AgenticTradingAssistant>`). If not, activate it using the commands in the "Setup" section.
        2.  Verify that all dependencies are installed correctly by running `pip install -r requirements.txt` within your activated Conda environment.
        3.  If problems persist, consider creating a fresh Conda environment and reinstalling the dependencies to rule out environment corruption.

-   **FastAPI Server Not Starting:**
    *   **Symptom:** The `uvicorn main:app --host 0.0.0.0 --port 8000 --reload` command fails, or the server isn't accessible at `http://localhost:8000`.
    *   **Solution:**
        1.  **Check for Port Conflicts:** Port 8000 might already be in use by another application. Try running the server on a different port, e.g., `uvicorn main:app --host 0.0.0.0 --port 8001 --reload`.
        2.  **Ensure Installation:** Verify that `fastapi` and `uvicorn` are installed in your activated Conda environment. Check `requirements.txt` and reinstall if necessary.
        3.  **Review Error Messages:** Look carefully at the error messages in the terminal output when you try to start the server. These often provide specific clues about the problem.

-   **Streamlit UI Not Loading:**
    *   **Symptom:** The Streamlit application page (`streamlit run streamlit_ui.py`) doesn't load in the browser, shows a "Connection refused" error, or displays other errors on the page.
    *   **Solution:**
        1.  **Ensure FastAPI Backend is Running:** The Streamlit UI relies on the FastAPI backend. Make sure the `uvicorn` server is running successfully in a separate terminal.
        2.  **Check Terminal for Errors:** Look for any error messages in the terminal where you ran the `streamlit run streamlit_ui.py` command.
        3.  **Verify Streamlit Installation:** Ensure Streamlit is correctly installed in your Conda environment.

-   **Data Ingestion Problems:**
    *   **Symptom:** Uploaded documents (PDFs, DOCX files) don't seem to be processed, or the retriever tool doesn't find information from these documents.
    *   **Solution:**
        1.  **Check FastAPI Server Logs:** Monitor the terminal output of the running FastAPI server (`uvicorn`) when you upload a file. Look for any error messages related to file processing, embedding generation, or vector database interaction.
        2.  **Verify Vector Database Configuration:** Ensure your vector database (e.g., Pinecone) is correctly configured in `config/config.yaml` and that the `PINECONE_API_KEY` in `.env` is correct and the service is accessible.
        3.  **Supported File Types:** Confirm that the uploaded file types are supported by the ingestion pipeline (typically PDF and DOCX).

-   **LLM/Tool Errors:**
    *   **Symptom:** The agent provides unexpected or nonsensical responses, logs errors related to Large Language Model (LLM) API calls, or specific tools (like Polygon or Tavily) fail during execution.
    *   **Solution:**
        1.  **Review `config/config.yaml`:** Check the `llm` and `tools` sections in `config/config.yaml` for any misconfigurations in model names, parameters, or tool settings.
        2.  **Verify API Keys for LLMs/Tools:** Ensure the API keys for the selected LLM provider (Google, Groq) and any external tools (Tavily, Polygon) are correctly set in the `.env` file and are active.
        3.  **Check Model Availability:** Some LLM models might have rate limits or specific access requirements. Check the respective provider's documentation if you suspect such issues.
        4.  **Examine Agent Logs:** If possible, inspect any detailed logging from the agent's execution flow, which might pinpoint where a tool or LLM call is failing.

## Contributing

Contributions are welcome! Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with clear, concise messages.
4.  Test your changes thoroughly.
5.  Submit a pull request.
