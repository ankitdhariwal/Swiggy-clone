from flask import Flask, request, jsonify
from config import MENU_ITEM_TABLE
from utils.files import writeFile, appendFile, readFile
import os, json
import sys

dirname = os.path.dirname
parent_dir = os.path.abspath(os.path.join(dirname(__file__), '..'))
sys.path.append(parent_dir)

file_path = os.path.abspath(os.path.join(parent_dir, "db/{}".format(MENU_ITEM_TABLE)))


def fetchRestaurantMenu(restaurant_id):
    existing_data = readFile(file_path)
    for index in range(len(existing_data)):
        for key in existing_data[index]:
            if key == restaurant_id:
                return existing_data[index][key]
       
    return None
    

