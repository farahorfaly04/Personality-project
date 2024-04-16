import os
from openai import OpenAI
import json
from flask import Flask, request, jsonify, send_from_directory

from dotenv import load_dotenv
load_dotenv() 

app = Flask(__name__, static_folder='')

api_key = os.getenv('OPENAI_API_KEY')
myclient = OpenAI(api_key=api_key)

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/test')
def test():
    return 'If you can see this, Flask is working!'

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    history = request.json.get('history', [])
    response, updated_history = prompt_gpt(myclient, user_input, history)
    return jsonify({"history": updated_history, "answer": response})

def prompt_gpt(client, user_input, history):
    with open('EV_data.json', 'r') as file:
        data = json.load(file)

    messages = [
        {"role": "system", "content": "You are a sales expert for a startup company that sells electric vehicles online.\
         The company is called 'YEO' (Your EV Online). You will given data about the cars sold in the company in JSON format. \
         Be confident, charismatic, and empathetic. Be achievement-oriented and goal-oriented. You also need to persuade users \
         to become potential customer. You need to sound like a sales person. Remove any quotations or * in your response and \
         never give the whole json data at once. Only give what the user asks."},
        {"role": "system", "content": json.dumps(data, indent=2)}
    ] + history

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content, messages

if __name__ == "__main__":
    app.run(debug=True)
