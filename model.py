from sqlalchemy import Column, Integer, String, Date, Boolean, MetaData, create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, create_session, relationship
from datetime import datetime


uri = "sqlite:///database.db"
engine = create_engine(uri, kwargs={"check_same_thread": False})
Base = declarative_base()
Meta = MetaData()
Session = create_session(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(64))

    group_id = Column(Integer, ForeignKey('group.id'))
    attendance = relationship('Attendance', backref='student', lazy='dynamic')
    profile = relationship('Profile', backref='user', lazy='dynamic', uselist=False)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    surname = Column(String(64))
    parent_phone_number = Column(String(32))

    user_id = Column(Integer, ForeignKey('user.id'))

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    students = relationship('User', backref='group', lazy='dynamic')
    attendances = relationship('Attendance', backref='group', lazy='dynamic')

class Attendace(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True)
    data = Column(Date, default=datetime.now)
    state = Column(Boolean, default=False)

    group_id = Column(Integer, ForeignKey('group.id'))
    student_id = Column(Integer, ForeignKey('student.id'))
    

if __name__=='__main__':
    session.meta.create_all()
    session.meta.drop_all()