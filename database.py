from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
date = datetime.strptime("15:30", "%H:%M")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key = True)

    name = Column("name", String, nullable = False)
    email = Column("email", String, nullable = False)
    password = Column("password", String, nullable = False)

    def __init__(self, name, email, password):
        last_user = Session.query(User).order_by(User.id.desc()).first()
        
        self.id= last_user.id + 1 if last_user != None else 1
        self.name= name
        self.email= email
        self.password= password

    def __repr__(self):
        return f"<User {self.id} {self.name} {self.email}>"


class Message(Base):
    __tablename__ = "messages"

    id = Column("id", Integer, primary_key = True)
    content = Column("content", String, nullable = False)
    writer = Column(Integer, ForeignKey("users.id"))
    date = Column("date", String, nullable = False)
    time = Column("time", String, nullable = False)

    def __init__(self, content, writer):
        last_msg = Session.query(Message).order_by(Message.id.desc()).first()
        date = datetime.now()

        self.id= last_msg.id + 1 if last_msg != None else 1
        self.content = content
        self.writer = writer
        self.date = str(date.day)  +"/"+  str(date.month)
        self.time = date.strftime("%I:%M %p")

    def __repr__(self):
        return f"<{self.writer}'s {self.id} {self.content} at {self.date} {self.time}>"

    

db = create_engine('sqlite:///data.db', echo = True)
Base.metadata.create_all(bind = db)

SESSION = sessionmaker(bind = db)
Session = SESSION()
