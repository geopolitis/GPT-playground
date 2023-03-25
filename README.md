

# Q & A Document and websites using GPT models

This Python scripts using the langchain library to search a directory for relevant PDF documents, extract their text, and store their embeddings using OpenAI's GPT language model. Then performs a similarity search on the stored embeddings to retrieve the most relevant documents for a given query. Finally, it uses OpenAI's GPT model to answer a user's question including the retrieved documents.

Within this repository there are several scripts created prograsivly during my tests. 

## Scripts

|Name|Description|
|----|---|
|document_search.py|Simple script loading PDF files|
|pdf_and_webpage_search.py| Stript stuctured in funtions, with some error handlers|
|Flask_pdf_webpages_search.py| Flask application|
|--|---|


## Prerequisites

- Python 3.x
- langchain library (`pip install langchain`)
- FAISS library (`pip install faiss`)
- python-dotenv library (`pip install python-dotenv`)
- OpenAI library (`pip install openai`)
- Pickle library (`pip install pickle`)
- Flask (`pip install flaks`)
- OpenAI API credentials

## Setup

1. Install the prerequisites

2. Get OpenAI API credentials by following [these instructions](https://beta.openai.com/docs/developer-quickstart/your-api-keys).

3. Create a `.env` file in the same directory as the script, and add the following variables(feel free to use the env-sample file). Availble models `text-embedding-ada-002`, `text-davinci-003`, `gpt-3.5-turbo`, `GPT-4`, and more. 	

```
OPENAI_API_KEY=<your-api-key>
OPENAI_API_KEY=<YOU OPENAI API KEY>
DOCUMENT_STORE_DIRECTOR=/path/to/your/documents/
INDEX_STORE_DIRECTORY=/path/to/your/index/
OPENAI_MODEL_NAME = 
```

5. Save your PDF files tha you wantto discuss with your GPT in the directory specified by `DOCUMENT_STORE_DIRECTORY`.

6. Run the script and enter your query when prompted.

## Usage

1. Make sure you have files in the `DOCUMENT_STORE_DIRECTORY`
2. Run the script using `python pdf_and_webpage_search.py`.
3. For Flask run `flask -A Flask_pdf_webpages_search.py run`
4. Ender website when prompted from CLI or http://127.0.0.1:5000
5. Enter your query when prompted.
6. The script will return the answer to your question based on the most relevant documents found in the specified directory.

## Notes

- The script stores document embeddings in a pickle file for faster retrieval. If the script is run again with the same PDF files, the embeddings will be read from this file instead of being recalculated.
- The script uses the FAISS library for similarity search, which requires significant memory resources. If you have a large number of PDF files, you may need to adjust the `chunk_size` and `chunk_overlap` parameters in `CharacterTextSplitter` to avoid running out of memory.
- The script caches API responses to avoid making redundant requests. Cached responses are stored in a pickle file specified by `cache_path`. If the script is run again with the same query, the cached response will be used instead of making a new API request.
- The script uses OpenAI's text-davinci-003 model for question answering, but other models can be used by changing the `model_name` parameter in `OpenAI()`.

Here's a brief overview of what each function in the script does:

- ']`read_from_web()` Reads content from a given web page URL (default: None) using the WebBaseLoader module from langchain.document_loaders.
- `read_from_PDF():` Reads all PDF files in the document store directory specified by the DOCUMENT_STORE_DIRECTORY environment variable, using the PyPDFLoader module from langchain.document_loaders.
- `split_text():` Splits the raw text into smaller chunks of text using the CharacterTextSplitter module from langchain.text_splitter.
- `create_embeddings():` Generates OpenAI embeddings for each text chunk using the OpenAIEmbeddings module from langchain.embeddings.
- `read_embeddings():` Reads the embeddings from file.
- `create_index():` Creates a FAISS index for the embeddings using the FAISS module from langchain.vectorstores.
- `search_documents():` Searches the documents for a given query using the FAISS index generated in the previous step and returns a list of documents.
- `answer_question():` Uses OpenAI's GPT model to answer the given question using the documents returned in the previous step and returns the answer.
- `main():` Runs the entire process and allows the user to input the web page URL and the question they want to ask.

## Disclaimer 
This project is experimental and provided as-is, without any warranty or guarantee of its effectiveness, suitability or reliability. The developers and contributors of this project will not be held responsible for any damage, loss or disruption of data, equipment or business that may arise from the use of this project. Use it at your own risk.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.