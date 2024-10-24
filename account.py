from database import User,Message, Session
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from utils import email_is_valid, password_is_varified
from utils import Hash

account = Blueprint("account", __name__)


@account.route("/account/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_email = request.form['email']
        user_password = request.form['password']


        if email_is_valid(user_email):
            session['email'] = user_email
            check = password_is_varified(user_password, user_email)
            if check[0]:
                session["user"] = check[1]
                return redirect(url_for("main.home"))
            
        flash("Sorry, email or password is not correct")
        return redirect(url_for('account.login'))
    else:
        return render_template('login.html')



@account.route('/account/create', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['user']
        email = request.form['email']
        password = request.form['password']

        found_user = Session.query(User).filter(User.name == name).first()
        found_email = Session.query(User).filter(User.email == email).first()
        if found_user or found_email:
            flash("User already exist")        
        else:
            session["user"] = name
            session["email"] = email
            if email_is_valid(email):
                new_user = User(name, email, Hash.hash_password(password))
                Session.add(new_user)
                Session.commit()
                
                return redirect(url_for("main.home"))
            else:
                flash("Invalid Email")

    return render_template('create-account.html')



@account.route("/account/logout")
def logout():
    session.pop('user', None)
    session.pop('email', None)
                
    flash("You're logged out")
    return redirect(url_for("main.home"))



@account.route("/account/delete")
def delete_account():
    usr = Session.query(User).filter(User.name == session['user']).first()
    msgs = Session.query(Message).filter(Message.writer == usr.id).all()
    Session.delete(usr)
    for msg in msgs:
        Session.delete(msg)
    Session.commit()

    session.pop('user', None)
    session.pop('email', None)
                
    flash("You're account has been deleted")
    return redirect(url_for("main.home"))

