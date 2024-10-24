from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from database import User, Message, Session

main = Blueprint("main", __name__)

@main.route("/", methods=["POST", "GET"])
def home():
    if 'user' in session and 'email' in session:
        user = Session.query(User).filter(User.name == session['user']).first()
        msgs = Session.query(Message).filter().all()

        return render_template('index.html', username=session['user'], email=session['email'],User=User,Message=Message, Session= Session, user=user, msgs=msgs)
    else:
        return redirect(url_for("account.create_account"))
    
