# Chatbot

An AI-powered chatbot that uses OpenAI's GPT-4 model for generating conversational responses. It's built using Flask, OpenAI API, and Tiktoken.

## Description
This chatbot leverages the power of OpenAI's GPT-4 model to generate human-like conversational responses. It receives input from the user and returns an appropriate response using the OpenAI API. It also calculates the cost of used tokens during the conversation, which helps in estimating the usage cost of the API.

## How it Works
The application has a simple web interface powered by Flask. When the user submits an input, the chatbot uses the OpenAI API to generate a response based on the input and previous conversation context. The response is then displayed in the interface. Tiktoken is used to calculate token usage and estimate the assosiated cost.

## Installation
Installation

1. Clone the repository:

```git clone https://github.com/username/ai-chatbot.git

cd Chatbot
```

2. Install the prerequisites
   `pip install -r requirements.txt`

3. Get OpenAI API credentials by following [these instructions](https://beta.openai.com/docs/developer-quickstart/your-api-keys).

4. Create a `.env` file in the same directory as the script, and add the following variables(feel free to use the env-sample file). Availble models `text-embedding-ada-002`, `text-davinci-003`, `gpt-3.5-turbo`, `GPT-4`, and more. 	

```
OPENAI_API_KEY=<YOU OPENAI API KEY>
OPENAI_MODEL_NAME = 
```

5. Run the application:

`flask -A Flask_chatbot_app.py`

6. Open your web browser and navigate to http://127.0.0.1:5000/


## Usage
Enter your input in the text field on the web interface and click the "Send" button.
The chatbot will generate a response based on your input and display it in the conversation window.
The token usage and associated cost for the conversation will be displayed below the conversation window.
To end the conversation or start a new one, refresh the page.
Disclaimer
This project is for educational and demonstration purposes only. The author is not responsible for any misuse of the code or any damages that may occur. Users are responsible for their own actions while using the chatbot and must adhere to OpenAI's usage policies.

## Disclaimer
This project serves solely as a learning resource and a showcase of its capabilities. The creator bears no liability for any improper usage of the code or any harm that may ensue. Users must assume responsibility for their actions when operating the chatbot and comply with OpenAI's usage guidelines. The project is distributed on an "as-is" basis, devoid of any warranties or assurances regarding its efficacy, appropriateness, or dependability. The developers and contributors of this project disclaim any responsibility for damage, loss, or disruption to data, equipment, or business that might arise from utilizing this project. Proceed at your own peril.
## License
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.