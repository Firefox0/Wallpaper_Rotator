import json


def load_json(path: str) -> dict:
    d = {}
    try:
        f = open(path, "r")
    except Exception as e:
        print(e)
    else:
        d = json.load(f)
        f.close()
    return d
