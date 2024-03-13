from flask import Flask, render_template, request, jsonify
from db_utils import *
import openai
import os, re
import uuid
app = Flask(__name__)

# Load your OpenAI API key from an environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
snippets = []

def sanitize_input(user_input):
    """
    A basic example of sanitizing input by removing unwanted characters
    and limiting the input length. Expand this based on your specific needs.
    """
    # Remove anything that isn't a word character, space, or common punctuation
    sanitized = re.sub(r'[^\w\s,.?!]', '', user_input)
    # Limit input length to avoid overly complex inputs
    max_length = 500
    return sanitized[:max_length]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-code', methods=['POST'])
def generate_code():

    data = request.get_json()
    description = data['coding_problem']
    description = sanitize_input(description)
    try:
        client = openai.OpenAI(api_key=openai_api_key)

        # Constructing the prompt with new examples
        prompt_with_examples = f"""
            You are an advanced coding aid, capable of generating code snippets for various programming tasks. You answer non-coding questions with an error message. Here are some examples of how you should respond:
    
            Example 1:
            Customer: What's the weather like in Paris?
            Agent: Invalid request. Please provide a programming-related question.
    
            Example 2:
            Customer: Generate a Python function to check if a number is prime.
            Agent: def is_prime(n):
                      if n <= 1:
                          return False
                      for i in range(2, int(n**0.5) + 1):
                          if n % i == 0:
                              return False
                      return True
    
            Example 3:
            Customer: Generate a Python function to find the factorial of a number.
            Agent: Sure! Here's a simple Python function to find the factorial of a number using recursion:
            def factorial(n):
                if n == 0:
                    return 1
                else:
                    return n * factorial(n-1)
    
            After these examples, when the customer asks a question, you should respond appropriately based on whether it's a programming-related question.
            """
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # Use the constructed prompt for the model
            messages=[
                {"role": "system", "content": prompt_with_examples},
                {"role": "user", "content": description}
            ]
        )
        # Navigate through the response
        choice_content = dict(dict(dict(completion)['choices'][0])['message'])['content']

        parts = choice_content.split("```")


        # Contains the code snippet, also removing "python" at the beginning if it exists
        code_snippet = parts[1].strip().lstrip("python\n") if len(parts) > 1 else ""
        snippet_id = str(uuid.uuid4())
        snippet = {'id': snippet_id, 'code': code_snippet}
        snippets.append(snippet)
        return jsonify({"code": choice_content})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/snippets', methods=['GET'])
def list_snippets():
    return jsonify(snippets)

@app.route('/delete-snippet/<snippet_id>', methods=['DELETE'])
def delete_snippet(snippet_id):
    global snippets
    snippets = [snippet for snippet in snippets if snippet['id'] != snippet_id]  # Filter out the deleted snippet
    return jsonify({'status': 'success', 'message': 'Snippet deleted'})

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    feedback_data = request.get_json()  # Make sure to use get_json() for JSON data
    if feedback_data:  # Ensure there's data
        result = save_feedback(feedback_data)
        if result:
            return jsonify({"message": "Feedback received"}), 200
        else:
            return jsonify({"error": "Failed to save feedback"}), 500
    else:
        return jsonify({"error": "No data received"}), 400
if __name__ == '__main__':
    app.run(debug=True)