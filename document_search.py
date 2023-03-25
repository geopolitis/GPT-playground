
import pickle
import os
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

query = input("Enter your question: ")

raw_text = ''
for filename in os.listdir(os.getenv('DOCUMENT_STORE_DIRECTOR')):
    if filename.endswith('.pdf'):
        filepath = os.path.join(os.getenv('DOCUMENT_STORE_DIRECTOR'), filename)
        read = PyPDFLoader(filepath)
raw_text = read.load()

text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_documents(raw_text)
embeddings = OpenAIEmbeddings()

# Vectors are stored in a pickle file
index_dir = os.getenv('INDEX_STORE_DIRECTORY')
if not os.path.exists(index_dir):
    os.makedirs(index_dir)
index_path = os.path.join(index_dir, 'Index.pkl')

# Write embeddings to file
with open( index_path, 'wb') as f:
    pickle.dump(embeddings, f)

# Read embeddings from file
with open(index_path, 'rb') as f:
    new_docsearch = pickle.load(f)

docsearch = FAISS.from_documents(texts, new_docsearch)

# Caching API information
cache_path = os.path.join(index_dir, 'openai_cache.pkl')
if os.path.exists(cache_path):
    with open(cache_path, 'rb') as f:
        cache = pickle.load(f)
else:
    cache = {}
# check if data is in cache
if query in cache:
    docs = cache[query]
else:
    # make API request and save result to cache
    docs = docsearch.similarity_search(query)
    cache[query] = docs
    with open(cache_path, 'wb') as f:
        pickle.dump(cache, f)

chain = load_qa_chain(OpenAI(model_name='text-davinci-003', temperature=0), chain_type="stuff")
result = chain.run(input_documents=docs, question=query)
print(result)

