from flask import Flask, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
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
# to_number = os.getenv('USER_NUMBER')
client = Client(account_sid, auth_token)

# Function to generate message response
def generate_answer(question):
    model_engine = "gpt-3.5-turbo"
    prompt = f"Q: {question}\nA:"

    try:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )

        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating answer: {e}"
    

# FLask API Endpoints
    
# This /chatgpt route is defined to handle POST requests from Twilio 
@app.route('/chatgpt', methods=['POST']) #Post request from Twilio URL (user SMS).
def chatgpt():
    incoming_que = request.values.get('Body', '').lower() #incoming message retrieved.
    logging.info(f"Received message: {incoming_que}")
    print(incoming_que)

    answer = generate_answer(incoming_que)
    logging.info(f"Generated answer: {answer}")
    print(answer)

    # Send response back to User via Twilio URL
    bot_resp = MessagingResponse() #response object is created
    msg = bot_resp.message()  
    msg.body(answer) #generated answer added to response as body of a message

    return str(bot_resp) #response converted to string and returned. Twilio handles SMS

# Route to send the initial message
@app.route('/send-initial-message', methods=['POST'])
def send_initial_message():
    # Extract phone number and initial message from the request
    to_number = request.form.get('phone_number')
    initial_message = request.form.get('message')
    
    try:
        # Send initial message to the user
        message = client.messages.create(
          body=initial_message,
          from_=twilio_number, # Your Twilio phone number
          to=to_number
        )
        return 'Initial message sent', 200

    except Exception as e:
        logging.error(f"Error sending initial message: {e}")
        return 'Error sending initial message', 500

@app.route('/')
def home():
    return 'Hello, World!'



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5001)