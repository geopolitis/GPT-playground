import os
import openai
import tiktoken
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
load_dotenv()

# If noe the .env file exists print a message
if not os.path.exists('.env'):
    print("No .env file found. Please create one and add the environment variables")
    exit()

OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME')
if not OPENAI_MODEL_NAME:
    raise ValueError("OPENAI_MODEL_NAME environment variable not set")

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

messages = []

def get_prompt(input):
    context = []
    messages.append(input)
    for index, message in enumerate(messages):
        if index % 2 == 0:
            context.append({"role": "user", "content": message})
        else:
            context.append({"role": "assistant", "content": message})
    return context

def create_chat_completion(input):
    completion = openai.ChatCompletion.create(
        model=OPENAI_MODEL_NAME,
        messages=get_prompt(input),
        temperature=0,
        max_tokens=1000,
    )
    messages.append(completion.choices[0].message.content)
    return completion.choices[0].message.content

def tokens_calc():
    enc = tiktoken.get_encoding("cl100k_base")
    count_tokens = len(enc.encode(" ".join(messages)))
    cost = count_tokens / 1000 * 0.002
    return "Used tokens: " + str(count_tokens) + " (" + format(cost, '.5f') + " USD)"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input')
    completion = create_chat_completion(user_input)
    token_info = tokens_calc()
    return jsonify({"response": completion, "token_info": token_info})

if __name__ == '__main__':
    app.run(debug=True)
