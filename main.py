from flask import Flask, render_template, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load your OpenAI API key from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_advice', methods=['POST'])
def get_advice():
    try:
        data = request.get_json()
        user_input = data.get('user_input')

        # Call the OpenAI API with the user input
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the appropriate model name
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor for children."},
                {"role": "user", "content": user_input},
            ]
        )

        # Extract the advice from the response
        advice = response.choices[0].message['content'].strip()

        return jsonify({'advice': advice})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
