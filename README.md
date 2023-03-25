# Document Search and Question Answering using GPT

This Python script uses the langchain library to search a directory of PDF files for relevant documents, extract their text, and store their embeddings using OpenAI's GPT language model. It then performs a similarity search on the stored embeddings to retrieve the most relevant documents for a given query. Finally, it uses OpenAI's text-davinci-003 model to answer a user's question including the retrieved documents.

## Prerequisites

- Python 3.x
- langchain library (`pip install langchain`)
- FAISS library (`pip install faiss`)
- python-dotenv library (`pip install python-dotenv`)
- OpenAI library (`pip install openai`)
- OpenAI API credentials

## Setup

1. Install Python 3.x and the necessary libraries by running the following command:

2. pip install langchain faiss python-dotenv openai

3. Get OpenAI API credentials by following [these instructions](https://beta.openai.com/docs/developer-quickstart/your-api-keys).

4. Create a `.env` file in the same directory as the script, and add the following variables:

DOCUMENT_STORE_DIRECTORY=/path/to/your/documents

INDEX_STORE_DIRECTORY=/path/to/your/index

OPENAI_API_KEY=<your-api-key>


5. Save your PDF files in the directory specified by `DOCUMENT_STORE_DIRECTORY`.

6. Run the script and enter your query when prompted.


## Usage

1. Run the script using `python document_search.py`.

2. Enter your query when prompted.

3. The script will return the answer to your question based on the most relevant documents found in the specified directory.

## Notes

- The script stores document embeddings in a pickle file for faster retrieval. If the script is run again with the same PDF files, the embeddings will be read from this file instead of being recalculated.
- The script uses the FAISS library for similarity search, which requires significant memory resources. If you have a large number of PDF files, you may need to adjust the `chunk_size` and `chunk_overlap` parameters in `CharacterTextSplitter` to avoid running out of memory.
- The script caches API responses to avoid making redundant requests. Cached responses are stored in a pickle file specified by `cache_path`. If the script is run again with the same query, the cached response will be used instead of making a new API request.
- The script uses OpenAI's text-davinci-003 model for question answering, but other models can be used by changing the `model_name` parameter in `OpenAI()`.


