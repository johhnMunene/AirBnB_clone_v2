#!/usr/bin/python3
""" Define the FileStorage class.
"""

import json
from models.base_model import BaseModel
from datetime import datetime

class FileStorage:
    """ This class serializes and deserializes instances
        to and from JSON format.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Returns a dictionary of __objects.
        """
        if cls is None:
            return self.__objects
        else:
            filtered_objects = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    filtered_objects[key] = value
            return filtered_objects

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file.
        """
        serialized_objects = {}
        for key, value in self.__objects.items():
            serialized_objects[key] = value.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """ Deserializes the JSON file to __objects.
        """
        try:
            with open(self.__file_path, 'r') as file:
                deserialized_objects = json.load(file)
                for key, value in deserialized_objects.items():
                    class_name, obj_id = key.split('.')
                    obj_dict = value
                    obj_dict['__class__'] = class_name
                    obj_dict['created_at'] = datetime.strptime(
                        obj_dict['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
                    if 'updated_at' in obj_dict:
                        obj_dict['updated_at'] = datetime.strptime(
                            obj_dict['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
                    self.new(BaseModel(**obj_dict))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Deletes obj from __objects if it's inside.
            If obj is equal to None, the method does nothing.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def update(self, obj):
        """ Updates an object in __objects.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        if key in self.__objects:
            self.__objects[key] = obj
        else:
            raise ValueError("Object not found in __objects.")

