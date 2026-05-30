import json 
import os

USER_DATA_FILE = 'data/users.json'

def load_users():
    print("LOAD FROM:", os.path.abspath(USER_DATA_FILE))
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, 'r') as file:
        return json.load(file)

def save_users(users):
    print("SAVE TO:", os.path.abspath(USER_DATA_FILE))
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

def load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def ensure_user_fields(user):

    user.setdefault("max_hp", 100)
    user.setdefault("hp", 100)
    user.setdefault("attack", 10)
    user.setdefault("defense", 5)
    user.setdefault("equipped_weapon", None)
    user.setdefault("equipped_armor", None)

    return user

BATTLE_DATA_FILE = 'data/battles.json'

def load_battles():
   return load_json(BATTLE_DATA_FILE)
def save_battles(battle_data):
    with open(BATTLE_DATA_FILE, 'w') as file:
        json.dump(battle_data, file, indent=4)

def ensure_battle_fields(battle):
    battle.setdefault("player_turn", True)
    battle.setdefault("defending", False)
    return battle