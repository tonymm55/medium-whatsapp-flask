from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from flask import jsonify

import os
import openai
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_NUMBER')
to_number = os.getenv('USER_NUMBER')
client = Client(account_sid, auth_token)


message = client.messages.create(
                              from_=f'whatsapp:{twilio_number}',
                              body='Hi, its Nat from We Finance Any Car. Great news your car finance has been approved! Are you still interested?',
                              to=f'whatsapp:{to_number}'
                          )
print(message.sid)


# Function to generate message response
def generate_answer(question):
    model_engine = "gpt-3.5-turbo"
    # Define the initial message from the assistant
    initial_message = "Hi, it's Nat from We Finance Any Car. Great news, your car finance has been approved! Are you still interested?"

    # Structure the messages array
    messages = [
        {"role": "system", "content": "You are a helpful assistant, named Nat."},
        {"role": "assistant", "content": initial_message},
        {"role": "user", "content": question}
    ]

    try:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=messages
        )

        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating answer: {e}"
    

# Flask API Endpoints
    
# This /chatgpt route is defined to handle POST requests from Twilio 
@app.route('/chatgpt', methods=['POST']) # Post request from Twilio URL (user SMS).
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print(incoming_que)

    answer = generate_answer(incoming_que)
    print(answer)
    
    # Send response back to User via Twilio URL
    bot_resp = MessagingResponse() # Response object is created
    msg = bot_resp.message()  
    msg.body(answer) # Generated answer added to response as body of a message

    return str(bot_resp) # Response converted to string and returned. Twilio handles SMS

@app.route('/', methods=['GET'])
def home():
    return 'Hello, World!'

@app.route('/send-initial-message', methods=['GET'])
def initial_message():
    try:
        message = client.messages.create(
            from_=f'whatsapp:{twilio_number}',
            body='Hi, it\'s Nat from We Finance Any Car. Great news, your car finance has been approved! Are you still interested?',
            to=f'whatsapp:{to_number}'
        )
        print(message.sid)
        return jsonify({"status": "success", "message_sid": message.sid}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5001)