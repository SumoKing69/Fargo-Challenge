from flask import Flask, request, jsonify, render_template, session, url_for
from flask_session import Session
import backend as bk

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/' , methods=['GET' , 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        url = data['url'] 
        mode = data['mode']

        if url and mode:
            session['url'] = url
            session['mode'] = mode
            #Setup the backend i.e the vectorspaces after webscraping the url provided
            bk.setup(url)

            if mode == 'text':
                return jsonify({'redirect': url_for('tchat')})
            
            elif mode == 'voice':
                return jsonify({'redirect': url_for('vchat')})
            
            
    return render_template('index.html')


@app.route('/chatbot_text' , methods=['GET' , 'POST'])
def tchat():
    url = session['url']
    mode = session['mode']
    
    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('user_message')  # Get message from AJAX request
        chatbot_response = session.get('chatbot_response', ["Hello! I am a chatbot assistant. Ask me anything!"])  # Fetch existing session responses
        print(f"User message: {user_message}")
        try:
            # Process the user message using backend logic
            response, chatbot_response = bk.get_response(user_message, chatbot_response)
            session['chatbot_response'] = chatbot_response  # Update session with new responses
            # Send response back to frontend
            return jsonify({'bot_response': response})
        except Exception as e:
            print(f"Error while generating a response: {e}")
            return jsonify({'bot_response': "Error while generating a response."})
    
    return render_template('chatbot_text.html', url=url, mode=mode)

@app.route('/chatbot_voice' , methods=['GET' , 'POST'])
def vchat():
    url = session['url']
    mode = session['mode']
    
    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('user_message')  # Get message from AJAX request
        chatbot_response = session.get('chatbot_response', ["Hello! I am a chatbot assistant. Ask me anything!"])  # Fetch existing session responses
        print(f"User message: {user_message}")
        try:
            # Process the user message using backend logic
            response, chatbot_response = bk.get_response(user_message, chatbot_response)
            session['chatbot_response'] = chatbot_response  # Update session with new responses
            # Send response back to frontend
            return jsonify({'bot_response': response})
        except Exception as e:
            print(f"Error while generating a response: {e}")
            return jsonify({'bot_response': "Error while generating a response."})
    
    return render_template('chatbot_voice.html', url=url, mode=mode)


if __name__ == '__main__':
    app.run(debug=True)

