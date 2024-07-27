from flask import Blueprint, render_template, request, jsonify
import openai
import os

main = Blueprint('main', __name__)

# Load your OpenAI API key from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/get_advice', methods=['POST'])
def get_advice():
    try:
        data = request.get_json()
        user_input = data.get('user_input')

        # Call the OpenAI API with the user input
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use the appropriate model name
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor for children."},
                {"role": "user", "content": user_input},
            ]
        )

        # Extract the advice from the response
        advice = response.choices[0].message['content'].strip()

        return jsonify({'advice': advice})
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
