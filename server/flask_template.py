# how to use css in python_ flask
# flask render_template example
import os
from flask import Flask, render_template
import webbrowser
 
# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='client', static_folder='staticfiles')
port = int(os.getenv("PORT", 8081))
# @app.route('/')
# def welcome():
#     return "This is the home page of Flask Application"
 
@app.route('/')
def index():
    return render_template('index1.html')
 
if __name__=='__main__':
    webbrowser.open_new_tab(f"http://localhost:{port}")
    app.run(port=port)