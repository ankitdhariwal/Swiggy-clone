from flask import Flask, request, jsonify
import os, json
import sys, random


def checkDuplicateUser(existing_user_data, incoming_user_data):
    email = incoming_user_data.get('email')
    phone_number = incoming_user_data.get('phone_number')

    for user_data in existing_user_data:
        if str(user_data.get('email')) == str(email):
            raise Exception("email already exists")

        if int(user_data.get('phone_number')) == int(phone_number):
            raise Exception("phone_number already exists")

