from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini AI
GOOGLE_API_KEY = "AIzaSyDZUVJN1XEJMcEwiTHJbvzPFJr_7uddvnw"  # Replace with your actual API key
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error initializing Gemini AI: {str(e)}")
    model = None

def get_health_response(user_input):
    if model is None:
        return "I'm having trouble connecting to the health assistant. Please try again later."
    
    try:
        # Generate response with health-focused context
        prompt = f"""You are a concise health assistant. Always respond in one sentence or ask one-line questions. 
        Focus on specific advice about:
        1. Medical tests needed
        2. Essential nutrients required
        3. Diet recommendations
        4. Immediate actions to take
        Keep responses brief and to the point. Always end with a question to continue the conversation.
        
        User: {user_input}"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "I'm having trouble processing your request. Please try again with a different question."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        response = get_health_response(user_message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'response': "I'm having trouble processing your request. Please try again."})

if __name__ == '__main__':
    app.run(debug=True) 