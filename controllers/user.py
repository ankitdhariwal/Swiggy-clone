from flask import Flask, request, jsonify
from config import USER_TABLE
from utils.files import writeFile, appendFile, readFile
from utils.user_helper import checkDuplicateUser
import os, json
import sys

dirname = os.path.dirname
parent_dir = os.path.abspath(os.path.join(dirname(__file__), '..'))
sys.path.append(parent_dir)

file_path = os.path.abspath(os.path.join(parent_dir, "db/{}".format(USER_TABLE)))


def registerUser(user_data):
    if not user_data:
        return False

    existing_data = readFile(file_path)
    checkDuplicateUser(existing_data, user_data)
    existing_data.append(user_data)
    json_string = json.dumps(existing_data)
    writeFile(file_path, json_string)
    return True

