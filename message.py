from flask import Blueprint,request, redirect, url_for,session
from database import Message, User, Session

message = Blueprint("message", __name__)

@message.route("/message/create", methods=['POST'] )
def create_message():
    writer = Session.query(User).filter(User.name == session['user']).first()
    msg = request.form['content']
    
    if msg != "":
        new_msg = Message(msg, writer.id)
        Session.add(new_msg)
        Session.commit()
    return redirect(url_for("main.home"))


@message.route("/message/delete/<msg_id>", methods=['POST'])
def delete_message(msg_id):
    msg = Session.query(Message).filter(Message.id == msg_id).first()
    if msg:
        Session.delete(msg)
    Session.commit()
    return redirect(url_for('main.home'))

@message.route("/message/delete-all")
def delete_all_msgs():
    msgs = Session.query(Message).filter().all()
    for msg in msgs:
        Session.delete(msg)
    Session.commit()
    return redirect(url_for('main.home'))
