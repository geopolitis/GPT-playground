import os
import sys
import time
import pickle
import logging
from flask import Flask, request, render_template, jsonify
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

app = Flask(__name__)

# Configure the logging module
logger = logging.getLogger(__name__)
logging.basicConfig(filename='embeddings_script.log', level=logging.INFO)
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Redirect stdout and stderr to the logging module
# sys.stdout = sys.stderr = logging.getLogger().info

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# If noe the .env file exists print a message
if not os.path.exists('.env'):
    print("No .env file found. Please create one and add the environment variables")
    exit()

DOCUMENT_STORE_DIRECTORY = os.getenv('DOCUMENT_STORE_DIRECTOR')
if not os.path.exists(DOCUMENT_STORE_DIRECTORY):
    os.makedirs(DOCUMENT_STORE_DIRECTORY)

INDEX_STORE_DIRECTORY = os.getenv('INDEX_STORE_DIRECTORY')
if not os.path.exists(INDEX_STORE_DIRECTORY):
    os.makedirs(INDEX_STORE_DIRECTORY)

OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME')
if not OPENAI_MODEL_NAME:
    raise ValueError("OPENAI_MODEL_NAME environment variable not set")

OPENAI_TEMPERATURE = 0


# functions
def read_from_web(webpage=None):
    """
    Read content from a web page
    """
    if webpage is None:
        return []
    web_loader = WebBaseLoader(webpage)     
    raw_text = []
    raw_text.extend(web_loader.load())
    return raw_text

def read_from_PDF():
    """
    Read all PDF files in the document store directory and concatenate the text
    """
    if not DOCUMENT_STORE_DIRECTORY:
        raise ValueError("DOCUMENT_STORE_DIRECTOR environment variable not set")
    if not os.path.isdir(DOCUMENT_STORE_DIRECTORY):
        raise ValueError(f"{DOCUMENT_STORE_DIRECTORY} is not a directory")
    raw_text = []
    for filename in os.listdir(os.getenv('DOCUMENT_STORE_DIRECTOR')):
        if filename.endswith('.pdf'):
            filepath = os.path.join(os.getenv('DOCUMENT_STORE_DIRECTOR'), filename)
            pdf_loader = PyPDFLoader(filepath)
            raw_text.extend(pdf_loader.load())
    return raw_text

def split_text(raw_text):
    """
    Split the raw text into chunks
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_documents(raw_text)
    return texts

def create_embeddings(texts):
    """
    Create OpenAI embeddings for the text chunks
    """
    if not INDEX_STORE_DIRECTORY:
        raise ValueError("INDEX_STORE_DIRECTORY environment variable not set check the file .env")
    if not os.path.isdir(INDEX_STORE_DIRECTORY):
        raise ValueError(f"{INDEX_STORE_DIRECTORY} is not a directory")
    embeddings = OpenAIEmbeddings()
    index_path = os.path.join(INDEX_STORE_DIRECTORY, 'Index.pkl')
    with open(index_path, 'wb') as f:
        pickle.dump(embeddings, f)
    return embeddings

def read_embeddings():
    """
    Read the embeddings from file
    """
    index_path = os.path.join(INDEX_STORE_DIRECTORY, 'Index.pkl')
    with open(index_path, 'rb') as f:
        embeddings = pickle.load(f)
    return embeddings

def create_index(texts, embeddings):
    """
    Create a FAISS index for the text chunks
    """
    docsearch = FAISS.from_documents(texts, embeddings)
    return docsearch

def search_documents(query, docsearch):
    """
    Search the documents for the given query
    """
    cache_path = os.path.join(INDEX_STORE_DIRECTORY, 'openai_cache.pkl')
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            cache = pickle.load(f)
    else:
        cache = {}
    if query in cache:
        docs = cache[query]
    else:
        docs = docsearch.similarity_search(query)
        cache[query] = docs
        with open(cache_path, 'wb') as f:
            pickle.dump(cache, f)
    return docs

def answer_question(docs, query):
    """
    Answer the given question using OpenAI's GPT model
    """
    chain = load_qa_chain(OpenAI(model_name=OPENAI_MODEL_NAME, temperature=OPENAI_TEMPERATURE), chain_type="stuff")
    result = chain.run(input_documents=docs, question=query)
    return result

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def answer():
    raw_text = read_from_PDF()
    webpage = request.form.get('webpage')
    web_text = read_from_web(webpage)
    raw_text.extend(web_text)
    texts = split_text(raw_text)
    embeddings = create_embeddings(texts)
    embeddings = read_embeddings()
    docsearch = create_index(texts, embeddings)
    query = request.form.get('query')
    docs = search_documents(query, docsearch)
    result = answer_question(docs, query)
    return render_template('answer.html', result=result)
