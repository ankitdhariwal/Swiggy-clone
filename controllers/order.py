from flask import Flask, request, jsonify
from config import ORDER_TABLE, ORDER_ITEM_TABLE
from utils.files import writeFile, appendFile, readFile
import os, json
import sys

dirname = os.path.dirname
parent_dir = os.path.abspath(os.path.join(dirname(__file__), '..'))
sys.path.append(parent_dir)

file_path_order = os.path.abspath(os.path.join(parent_dir, "db/{}".format(ORDER_TABLE)))
file_path_order_item = os.path.abspath(os.path.join(parent_dir, "db/{}".format(ORDER_ITEM_TABLE)))



def createNewOrder(new_order_data, order_items):
    # Insert in order table, order_item table will take place
    if not new_order_data:
        return False

    existing_data = readFile(file_path_order)
    existing_data.append(new_order_data)
    json_string = json.dumps(existing_data)
    writeFile(file_path_order, json_string)
    
    for item in order_items:
        new_order_item = {
            'order_id': 123, # new_order_data order table ID
            'item_id': item['item_id'],
            'quantity': item['quantity'],
            'price': item['price']
        }
        existing_data = readFile(file_path_order_item)
        existing_data.append(new_order_item)
        json_string = json.dumps(existing_data)
        writeFile(file_path_order_item, json_string)
    
    return True



def getAllOrderByUser(user_id=None):
    existing_data = readFile(file_path_order)

    if len(existing_data) == 0:
        raise Exception("No orders found for this user")

    all_orders = []
    for index in range(len(existing_data)):
        if int(existing_data[index].get('user_id')) == user_id:
            all_orders.append(existing_data[index])

    return all_orders



