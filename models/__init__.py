#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


storage_t = getenv("HBNB_TYPE_STORAGE")

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    classes = DBStorage().classes
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    classes = FileStorage().classes
    storage = FileStorage()
storage.reload()
