from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import openai
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# 
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

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5001)