import os
import re
import sys
import time
import pickle
import logging
import openai
import tiktoken
from flask import Flask, request, render_template, jsonify, make_response
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from colorama import init, Fore, Style
from flask_redis import FlaskRedis
from redis.exceptions import ConnectionError
from flask_cors import CORS

init(autoreset=True)

app = Flask(__name__)

app.config['REDIS_URL'] = 'redis://localhost:6379/0'
redis_client = FlaskRedis(app)
CORS(app)

# Configure the logging module
logger = logging.getLogger(__name__)
logging.basicConfig(filename='chatbot.log', level=logging.INFO)
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
#openai.api_key =  os.getenv('OPENAI_API_KEY')

# functions
messages = []

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

def read_from_webpages_url():
    """
    Read content from web pages listed in the WEBPAGES_URLS environment variable
    """
    webpages_urls = os.getenv("WEBPAGES_URLS")
    if webpages_urls:
        urls = webpages_urls.split(",")
        raw_text = []
        for url in urls:
            url = url.strip()
            raw_text.extend(read_from_web(url))
        return raw_text
    else:
        warning_msg = "WEBPAGES_URLS environment variable not set or empty."
        logger.warning(Fore.YELLOW + warning_msg)
        return []

def read_from_PDF():
    """
    Read all PDF files in the document store directory and concatenate the text
    """
    if not DOCUMENT_STORE_DIRECTORY:
        raise ValueError("DOCUMENT_STORE_DIRECTOR environment variable not set")
    if not os.path.isdir(DOCUMENT_STORE_DIRECTORY):
        raise ValueError(f"{DOCUMENT_STORE_DIRECTORY} is not a directory")

    raw_text = []
    # Gather files
    pdf_files = [filename for filename in os.listdir(DOCUMENT_STORE_DIRECTORY) if filename.lower().endswith('.pdf')]

    if pdf_files:
        for filename in pdf_files:
            filepath = os.path.join(DOCUMENT_STORE_DIRECTORY, filename)
            pdf_loader = PyPDFLoader(filepath)
            raw_text.extend(pdf_loader.load())
    else:
        warning_msg = "No PDF files found in the document store directory."
        logger.warning(Fore.YELLOW + warning_msg)

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

def create_index(texts, embeddings):
    """
    Create a FAISS index for the text chunks
    """
    try:
        if not texts or not embeddings:
            warning_msg = "No texts or embeddings found. Skipping index creation."
            logger.warning(Fore.YELLOW + warning_msg)
            return None

        docsearch = FAISS.from_documents(texts, embeddings)
        return docsearch
    except Exception as e:
        error_msg = f"An error occurred during index creation: {e}"
        logger.error(Fore.RED + error_msg)
        return None

def read_embeddings():
    """
    Read the embeddings from file
    """
    index_path = os.path.join(INDEX_STORE_DIRECTORY, 'Index.pkl')
    with open(index_path, 'rb') as f:
        embeddings = pickle.load(f)
    return embeddings

def search_documents(query, docsearch):
    """
    Search the documents for the given query
    """
    if docsearch is None:
        warning_msg = "No index available for searching documents. Skipping search."
        logger.warning(Fore.YELLOW + warning_msg)
        return []

    try:
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
    except Exception as e:
        error_msg = f"An error occurred during document search: {e}"
        logger.error(Fore.RED + error_msg)
        return []

def answer_question(docs, query):
    """
    Answer the given question using OpenAI's GPT model and searching our own knowledge base. Returns the answer with the SOURCE of the answer.
    """
    from langchain.chains.qa_with_sources import load_qa_with_sources_chain
    chain = load_qa_with_sources_chain(OpenAI(model_name=OPENAI_MODEL_NAME, temperature=OPENAI_TEMPERATURE), chain_type="stuff")
    result = chain.run(input_documents=docs, question=query).strip()

    return result

def get_prompt(input):
    """
    Create the prompt for the OpenAI GPT model as required by the Chat Completion endpoint.
    """
    role_name = 'CFOgpt'
    prompt = 'Act as a professional and knowledgeable peroson'
    context = []
    messages.append(input.strip())
    role_content = redis_client.hget('roles', role_name)
    if role_content:
        prompt = role_content.decode()
        
    print("Prompt : ", prompt)
    for index, message in enumerate(messages):
        if index % 2 == 0:
            context.append({"role": "system", "content": prompt})
            context.append({"role": "user", "content": message})
        else:
            context.append({"role": "assistant", "content": message})
    return context

def create_chat_completion(emb_results, user_input):    
    sentences = ["I am sorry",
                 "I don't know",
                 "I don't understand",
                 "Sorry, I cannot suggest",
                 "Sorry,",
                 "I'm sorry,",
                 "I cannot provide an answer", 
                 "I don't have enough information",
                 "There is no information",
                 "No, there is no information",
                 "The given context does not provide"]
    
    # Use a list comprehension to create a list of compiled regex patterns
    patterns = [re.compile(re.escape(sentence)) for sentence in sentences]
    # Check if any pattern matches at the beginning of emb_results
    if any(pattern.match(emb_results) for pattern in patterns):
        print("I am here User Inpute:", user_input, "Embeddinds Result: ", emb_results )
        try: 
            completion = openai.ChatCompletion.create(
                model=OPENAI_MODEL_NAME,
                messages=get_prompt(user_input),
                temperature=OPENAI_TEMPERATURE,
                max_tokens=1500,
                n=1
            )
            messages.append(completion.choices[0].message.content)
            return completion.choices[0].message.content
        except Exception as e:
            print("Error: ", e)
            response = "OpenAI API Error: ChatCompletion"
    else:
        response = emb_results
    return response

def tokens_calc():
    enc = tiktoken.get_encoding("cl100k_base")
    count_tokens = len(enc.encode(" ".join(messages)))
    cost = count_tokens / 1000 * 0.002
    return "Used tokens: " + str(count_tokens) + " (" + format(cost, '.5f') + " USD)"

# Logic
raw_text = read_from_webpages_url()
raw_text.extend(read_from_PDF())
texts = split_text(raw_text)
embeddings = create_embeddings(texts)
embeddings = read_embeddings()
docsearch = create_index(texts, embeddings)

# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/roles')
def roles():
    return render_template('roles.html')

@app.route('/webpage', methods=['POST'])
def submit_webpage():
    import traceback
    while True:
        try:
            global raw_text, texts, embeddings, docsearch
            
            data = request.get_json()
            webpage = data.get('webpage')
            new_content = read_from_web(webpage)
            raw_text.extend(new_content)
            
            texts = split_text(raw_text)
            embeddings = create_embeddings(texts)
            embeddings = read_embeddings()
            docsearch = create_index(texts, embeddings)
            return jsonify({"status": "success", "message": "New URL submitted successfully to your embeddings."})

        except Exception as Oops:
            print(traceback.format_exc())
            print(Oops)
            return jsonify({"status": "error", "message": "An error occurred while processing the webpage. Please try again."}), 400
        
@app.route('/chat', methods=['POST'])
def chat():
        try:
            user_input = request.json.get('input')
            #print("----User Input----: ", user_input)
            # Queries 
            docs = search_documents( user_input, docsearch)
            emb_result = answer_question(docs, user_input)
            completion = create_chat_completion(emb_result, user_input)
            token_info = tokens_calc()
            return jsonify({"response": completion, "token_info": token_info})  
        except Exception as Oooooops:
            print(Oooooops)
            return jsonify({"response": "Huston we have a problem!!!!!!!! %s" %"}"})

@app.errorhandler(ConnectionError)
def handle_connection_error(e):
    return 'Redis server not available', 500

@app.route('/Create_New_Role', methods=['POST'])
def create_new_role():
    try:
        role_name = request.form['Role_name']
        role_content = request.form['Role_content']
        if redis_client.hexists('roles', role_name):
            return 'Role with this name already exists', 400
        else:
            redis_client.hset('roles', role_name, role_content)
            return 'Role created', 201
    except ConnectionError as e:
        return handle_connection_error(e)

@app.route('/Get_Roles', methods=['GET'])
def get_roles():
    try:
        name = request.args.get('name')
        if name:
            role_content = redis_client.hget('roles', name)
            if role_content:
                print(role_content.decode())
                return {name: role_content.decode()}
            else:
                return 'Role not found', 404
        else:
            roles = redis_client.hgetall('roles')
            roles_dict = {k.decode(): v.decode() for k, v in roles.items()}
            return roles_dict
    except ConnectionError as e:
        return handle_connection_error(e)
    
@app.route('/Delete_Role', methods=['POST'])
def delete_role():
    try:
        role_name = request.form['Role_name']
        if redis_client.hexists('roles', role_name):
            redis_client.hdel('roles', role_name)
            return 'Role deleted', 200
        else:
            return 'Role not found', 404
    except ConnectionError as e:
        return handle_connection_error(e)

if __name__ == '__main__':
    app.run(debug=True)