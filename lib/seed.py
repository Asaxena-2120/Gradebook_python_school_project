from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Course



if __name__=='__main__':
    engine = create_engine('sqlite:///gradebook.db')
    Session = sessionmaker(engine)
    session = Session()