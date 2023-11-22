#!/usr/bin/python3
"""This is the user class"""
from models.base_model import BaseModel

class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    email = ''
    password = ''
    first_name = ''
    last_name = ''
