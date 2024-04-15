from flask import Flask, request, jsonify



@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    history = request.json.get('history', [])
    
    response, updated_history = prompt_gpt(client, user_input, history)
    return jsonify({"history": updated_history, "answer": response})

def prompt_gpt(client, user_input, history):
    with open('EV_data.json', 'r') as file:
        data = json.load(file)

    # Ensure all messages are appended correctly
    messages = [
        {"role": "system", "content": "You are a sales expert for a startup company that sells electric vehicles online. The company is called 'YEO' (Your EV Online). You will provide users with data about the cars in JSON format. Display confidence, charisma, and empathy. Be achievement-oriented and goal-oriented."},
        {"role": "system", "content": json.dumps(data)}
    ] + history

    # Append the new user message
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    # Append the bot's response to the history for future context
    if response.choices and response.choices[0].message:
        messages.append({"role": "assistant", "content": response.choices[0].message['content']})

    return response.choices[0].message['content'], messages

if __name__ == "__main__":
    app.run(debug=True)
