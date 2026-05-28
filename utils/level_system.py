from discord.ext import commands
import json

def get_exp_to_next_level(level):
    return 100 * level
def check_level_up(user):
    level_up = False
    while user["exp"] >= get_exp_to_next_level(user["level"]):

        user["exp"] -= get_exp_to_next_level(user["level"])
        user["level"] += 1
        
        user["max_hp"] += 20
        user["attack"] += 5
        user["defense"] += 5

        user["hp"] = user["max_hp"]

        level_up = True
    return level_up