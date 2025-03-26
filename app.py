import time
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from llama import get_llama_response
from gpt import get_gpt_response
from response_log import log_to_csv


# Flask backend setup
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session handling
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit


@app.route("/")
def home():
    # If user is already logged in, redirect to the chatbot page
    if 'logged_in' in session:
        return redirect(url_for('chatbot'))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == 'test' and password == 'prep4prep':
        session['logged_in'] = True
        return redirect(url_for('chatbot'))
    else:
        flash("Invalid credentials. Please try again.")
        return redirect(url_for('home'))

@app.route("/chatbot")
def chatbot():
    if 'logged_in' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('home'))

@app.route("/chat", methods=["POST"])
def chat():
    model = "Llama-3.1-8B-Instruct"
    user_message = request.json.get("message")
    language_level = request.json.get("language_level")
    # Collect Llama data
    # start_time = time.time()
    # llama_response = get_llama_response(user_message)
    # llama_time = time.time() - start_time
    # log_to_csv("Llama-3.1-8B-Instruct", user_message, llama_response, llama_time)

    # Collect GPT response data
    start_time = time.time()
    gpt_response = get_gpt_response(user_message, language_level)
    gpt_time = time.time() - start_time
    log_to_csv("GPT", user_message, gpt_response, gpt_time, language_level)

    return jsonify({
        # "llama_response": llama_response,
        "gpt_response": gpt_response
    })

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

#Define the application variable as app
application = app
