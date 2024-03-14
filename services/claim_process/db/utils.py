from sqlmodel import Session
from db.database import engine


# Utility to start a DB session
def start_session():
    """
    Used to create a new DB session.
    :return: Session
    """
    return Session(engine)
