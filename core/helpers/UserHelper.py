from db.model import User, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

class UserHelper:

    @staticmethod
    def createUser(name, lastname, email, role):
        user = User()
        user.firstName = name
        user.lastName = lastname
        user.email = email
        user.role = role

        session.add(user)
        session.commit()

    @staticmethod
    def deleteUser(id):
        user = session.query(User).filter(User.id == id).first()
        session.delete(user)
        session.commit()

    @staticmethod
    def editItem(id, name=None, lastname=None, email=None, role=None):
        user = session.query(User).filter(User.id == id).first()
        if name:
            user.name = name
        if lastname:
            user.lastName = lastname
        if email:
            user.email = email
        if role:
            user.role = role

        session.commit()

    @staticmethod
    def login(id, name, role):
        user = session.query(User).filter(User.id == id).first()
        if not user:
            return "User not found"
        if name == user.firstName and role == user.role:
            return user
        else:
            return "Wrong name/ role"

