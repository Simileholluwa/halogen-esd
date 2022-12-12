from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "1e4485553cad7487a6f08a97"

from email_spam import routes
