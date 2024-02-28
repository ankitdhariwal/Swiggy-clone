from flask import Flask, request, jsonify
import os, json
import sys, random


def checkDuplicateRider(existing_rider_data, incoming_rider_data):
    email = incoming_rider_data.get('email')
    phone_number = incoming_rider_data.get('phone_number')

    for rider_data in existing_rider_data:
        if str(rider_data.get('email')) == str(email):
            raise Exception("email already exists")

        if int(rider_data.get('phone_number')) == int(phone_number):
            raise Exception("phone_number already exists")

