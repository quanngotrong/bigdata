from flask import Flask, request, jsonify
import json
from flask_cors import CORS
from kafka import KafkaConsumer, KafkaProducer

app = Flask(__name__)

TOPIC_NAME = 'daily-weather'
KAFKA_SERVER = 'localhost:9092'

producer = KafkaProducer