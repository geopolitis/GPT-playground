'''
This test suite defines three test cases: test_index, test_submit_webpage, and test_chat. Each test case sends a request to the corresponding endpoint of your Flask application and checks whether the response is as expected.

test_index tests the root endpoint ('/') and checks if the status code of the response is 200 (success).
test_submit_webpage sends a POST request to the '/webpage' endpoint with a test URL and checks if the status code of the response is 200 and the response message is "URL submitted successfully."
test_chat sends a POST request to the '/chat' endpoint with a test input and checks if the status code of the response is 200 and if the response contains the "response" and "token_info" keys.
To run the tests, you can use the following command in your terminal:

  python -m unittest test_app.py

Keep in mind that these tests are just a starting point. 
You can add more test cases and improve the existing ones based on the specific requirements and expected behavior of your application. 
Additionally, consider using mock or unittest.mock libraries to mock external services or functions as needed to isolate your tests and avoid relying on external dependencies.
'''
import unittest
import json
from Chatbot import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_submit_webpage(self):
        test_url = "https://www.google.com"
        response = self.app.post('/webpage', json={"webpage": test_url})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), 'URL submitted successfully')

    def test_chat(self):
        test_input = "What is AI?"
        response = self.app.post('/chat', json={"input": test_input})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("response", data)
        self.assertIn("token_info", data)

if __name__ == '__main__':
    unittest.main()
