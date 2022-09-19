import json
import os
from mysql import connector
from flask import g

config_path = os.getenv("PYTHON_RESOURCES") + "/flask/login_register/database.json"
config_file = open(config_path, "r")
config_json = json.loads(config_file.read())
config = {'user': config_json['user'], 'password': config_json['password'], 'database': config_json['database'], 'host': config_json['host']}

def get_db():
    conn = None
    conn = connector.connect(**config)
    if conn is not None:
        return conn
    return None