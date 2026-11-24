import json
import os

RECORD_PATH = os.path.join(os.path.dirname(__file__), "record.json")


def load():
    try:
        with open(RECORD_PATH) as f:
            return json.load(f)
    except (OSError, ValueError):

        return {"best_time": 0, "clear_time": 0}


def save(rec):
    with open(RECORD_PATH, "w") as f:
        json.dump(rec, f)
