import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ToDoFlask.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False