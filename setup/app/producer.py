import json
import logging
from faker import Faker
from bbutil import Util
faker = Faker()
from random import randint
import sys
import datetime
from pymongo import MongoClient
import random
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Producer

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("faker").setLevel(logging.ERROR)

from utils import generate_claims, timer

def produce_claims(producer, num,batch_size):
    iteration = int(num/batch_size)
    topic = "<TOPIC>"
    for i in range(iteration):
        claims = generate_claims(iteration) 
        producer.produce(topic, json.dumps(claims[0]), callback=delivery_callback)

def delivery_callback(err, msg):
    if err:
        print('ERROR: Message failed delivery: {}'.format(err))
    else:
        print("Produced event to topic {topic}".format(
            topic=msg.topic()))


if __name__ == "__main__":
    bb = Util()
    ARGS = bb.process_args(sys.argv)
    batch_size = 5
    config = dict({"bootstrap.servers":"broker:29092"})
    producer = Producer(config)

    if ARGS["action"] == "produce":
        produce_claims(producer, 50,batch_size)
#        producer.poll(10000)
 #       producer.flush()