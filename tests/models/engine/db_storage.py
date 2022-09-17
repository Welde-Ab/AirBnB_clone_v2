#!/usr/bin/python3
"""DBStorage class"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Class DBStorage"""

    __engine = None
    __session = None

    def __init__(self):
        """Funny Init"""
        USER = getenv('HBNB_MYSQL_USER')
        PWD = getenv('HBNB_MYSQL_PWD')
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')
        ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            USER, PWD, HOST, DB, ENV), pool_pre_ping=True)

        if ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Method to retrieve objects"""
        from models.user import User
        from models.place import Place
        from models.city import City
        from models.base_model import BaseModel
        from models.state import State
        from models.review import Review
        from models.amenity import Amenity

        classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
        }
        if cls:
            new_dict = {}
            all_objects = self.__session.query(classes[cls]).all()
            for obj in all_objects:
                key = type(obj).__name__ + "." + obj.id
                new_dict[key] = obj
            return (new_dict)
        else:
            all_dicts = {}
            dict_list = []
            State = self.all('State')
            City = self.all('City')
            dict_list.append(State)
            dict_list.append(City)

            for dicts in dict_list:
                all_dicts.update(dicts)

            return(all_dicts)

    def new(self, obj):
        """method new"""
        self.__session.add(obj)

    def save(self):
        """saves commit"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes objects"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reloads """
        from models.user import User
        from models.place import Place
        from models.city import City
        from models.base_model import BaseModel
        from models.state import State
        from models.review import Review
        from models.amenity import Amenity
        Base.metadata.create_all(self.__engine)

        current_db_sess = sessionmaker(
            bind=self.__engine, expire_on_commit=False)

        Session = scoped_session(current_db_sess)
        self.__session = Session()

    def close(self):
        """Method Close"""
        self.__session.close()
