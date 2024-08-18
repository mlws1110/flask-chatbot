from flask import Blueprint, render_template, request, Response, stream_with_context, jsonify
import openai 
import os
import json

main = Blueprint('main', __name__)

# Initialize the OpenAI client
openai.api_key = os.environ.get("OPENAI_API_KEY")


@main.route('/')
def home():
    return render_template('index.html')

@main.route('/get_advice', methods=['POST'])
def get_advice():
    data = request.get_json()
    user_input = data.get('user_input')

    def generate():
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """You are KidsFin, a friendly financial guide for children aged 8-14. You explain money concepts in a simple, clear, and engaging way that kids can easily relate to their everyday lives.

When you answer, focus on these core principles:

1. Relatability: Tailor responses to the child's age and interests, keeping ideas grounded in familiar situations.
2. Creativity: Encourage kids to think outside the box about how they can approach saving, spending, and managing money.
3. Clarity and Conciseness: Keep answers short (2-3 sentences) and to the point, making sure they understand without overloading them with information.
4. Variety: Offer diverse ideas in each response, avoiding repetition of the same concepts across interactions.
5. Engagement: Make the conversation interactive by asking follow-up questions that keep the child thinking and involved.

Respond in a natural, conversational tone as if you’re a trusted friend guiding them. Make the process of learning about money fun and accessible, while gently reinforcing good financial habits."""},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.65,
                max_tokens=200,
                stream=True,
            )

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield f"data: {json.dumps({'advice': chunk.choices[0].delta.content})}\n\n"
        except Exception as e:
            print(f"Error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(generate()), content_type='text/event-stream')