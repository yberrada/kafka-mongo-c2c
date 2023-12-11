from bbutil import Util
import logging
from pymongo import MongoClient
from faker import Faker
faker = Faker()
from random import randint
import random
import datetime

bb = Util()


def generate_claims(num):
    claims = [None] * num
    for i in range(0, num):
        # listings = {}
        print(f'Object {i} generated')
        claims[i] = {
            "claimstatusdate": faker.date(),
            "claimtype":"Medical",
            "claimstatus":randint(1, 100000),
            "placeofservice":random.choice(['Pharmacy', 'Online']),
            "__deleted":random.choice([True, False]),
            "claim_id": "C-" + str(randint(1, 100000)),
            "principaldiagnosis": randint(1, 100000),
            "receiveddate": faker.date(),
            "servicefacility_id": "P-" + str(randint(1, 100000)),
            "priorauthorization": random.choice(['T', 'F']),
            "subscriber_id": "M-" + str(randint(1, 100000)),
            "serviceenddate": faker.date(),
            "supervisingprovider_id": "P-" + str(randint(1, 100000)),
            "attendingprovider_id": "P-" + str(randint(1, 100000)),
            "patient_id": "M-" + str(randint(1, 100000)),
            "renderingprovider_id": "P-" + str(randint(1, 100000)),
            "servicefromdate": faker.date(),
            "id": randint(1, 100000),
            "modified_at": faker.date(),
            "lastxraydate": faker.date()
        }
    logging.debug(f"Claim objects generated")
    return claims

def timer(starttime,cnt = 1, ttype = "sub"):
    elapsed = datetime.datetime.now() - starttime
    secs = elapsed.seconds
    msecs = elapsed.microseconds
    if secs == 0:
        elapsed = msecs * .001
        unit = "ms"
    else:
        elapsed = secs + (msecs * .000001)
        unit = "s"
    if ttype == "sub":
        logging.debug(f"query ({cnt} recs) took: {'{:.3f}'.format(elapsed)} {unit}")
    else:
        logging.debug(f"# --- Complete: query took: {'{:.3f}'.format(elapsed)} {unit} ---- #")
        logging.debug(f"#   {cnt} items {'{:.3f}'.format((elapsed)/cnt)} {unit} avg")
        