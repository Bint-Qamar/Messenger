from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'be2cbf248e11803e32db291ba0076886'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=7)


from main import main
from message import message
from account import account
from user_profile import profile

app.register_blueprint(main)
app.register_blueprint(message)
app.register_blueprint(account)
app.register_blueprint(profile)

if __name__ == "__main__":
    app.run(debug=True)
