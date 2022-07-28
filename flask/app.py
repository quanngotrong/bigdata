from xml.dom.minidom import Document
from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient
import os
import csv
from prepocessing_data import preprocessing_from_csv

MONGODB_URL = os.environ.get('MONGODB_URL')
app = Flask(__name__)

def get_db():
  client = MongoClient(MONGODB_URL)
  db = client['weather-database']
  return db

## class
weather_validator = {
  "$jsonSchema": {
      "bsonType": "object",
      "required": [ "time", "temperature", "dew_point", "humidity", "wind", "wind_speed", "wind_gust", "pressure", "precip", "condition" ],
      "properties": {
        "time": {
            "bsonType": "string",
            "description": "must be a string and is required"
        },
        "temperature": {
            "bsonType": "int",
            "description": "must be an integer and is required"
        },
        "dew_point": {
            "bsonType": "int",
            "description": "must be an integer and is required"
        },
        "humidity": {
            "bsonType": "int",
            "description": "must be an integer and in percen and is required"
        },
        "wind": {
            "bsonType": "string",
            "description": "must be an integer and is required"
        },
        "wind_speed": {
            "bsonType": "int",
            "description": "must be a string and is required"
        },
        "wind_gust": {
            "bsonType": "int",
            "description": "must be an integer and is required"
        },
        "pressure": {
            "bsonType": "double",
            "description": "must be an integer and is required"
        },
        "precip": {
            "bsonType": "double",
            "description": "must be an integer and is required"
        },
        "Condition": {
            "bsonType": "string",
            "description": "must be an integer and is required"
        }
      }
  }
}

def create_weather_collection(db):
  try:
    db.create_collection('weather')
  except Exception as e:
    print(e)
  
  db.command('collMod', 'weather', validator=weather_validator)

@app.route('/')
def ping_server():
  return "welcome to the world of animals 123 deaswdf"

@app.route('/weathers')
def get_stored_weathers():
  print('tst')
  db=""
  try:
    print('test')
    db = get_db()
    
    # check if database has collection or not
    collist = db.list_collection_names()
    if "weather" not in collist:
      create_weather_collection(db)

    weather = db.weather
    
    data = []
    # read data from csv
    print("aaaa")
    with open('flask/data/HCMC2021-01-01.csv') as csv_file:
      print("bbb")
      csv_reader = csv.reader(csv_file, delimiter=',')
      print(csv_reader)
      data = []
      for row in csv_reader:
        document = preprocessing_from_csv(row)
        data.append(document)
    
    weather.insert_many(data)
    
    return "insert successfully " + " documents"
  except:
    pass
  finally:
    if type(db) == MongoClient:
      db.close()

if __name__=='__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
  