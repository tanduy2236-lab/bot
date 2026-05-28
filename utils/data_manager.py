import json 
import os

USER_DATA_FILE = 'data/users.json'

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as file:
        return json.load(file)
    
def ensure_user_fields(user):

    user.setdefault("max_hp", 100)
    user.setdefault("attack", 10)
    user.setdefault("defense", 5)
    user.setdefault("equipped_weapon", None)
    user.setdefault("equipped_armor", None)

    return user