#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
import os
import models
from models.city import City
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")

    else:
        @property
        def cities(self):
            """"""
            list_cities = []
            for item in models.storage.all(City).values():
                if item.state_id == self.id:
                    list_cities.append(item)
            return list_cities
