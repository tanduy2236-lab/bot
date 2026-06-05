import discord 
from discord.ui import Select, View
import random
from utils.data_manager import load_json, save_users
ENEMIES = load_json('data/enemies.json')
from utils.data_manager import ensure_user_fields, load_battles, load_users, save_battles

class EnemySelect(Select):
    def __init__(self):
        options = []
        for enemy_key, enemy in ENEMIES.items():
            options.append(discord.SelectOption(label=enemy["name"],
                                                 description=f"HP: {enemy['health']} Attack: {enemy['attack']} Defense: {enemy['defense']}",
                                                 value=enemy_key))
        
        super().__init__(placeholder="Chọn một kẻ thù để chiến đấu...", options=options)

    async def callback(self, interaction: discord.Interaction):
        enemy_name = self.values[0]
     
        user_id = str(interaction.user.id)

        users = load_users()
        battle_data = load_battles()
        user = users[user_id]

        ensure_user_fields(user)
        save_users(users)
        enemy_data = ENEMIES[enemy_name]
        enemy = enemy_data.copy()
        enemy_level = max(1, user["level"] + random.randint(-1, 1))
        scaled_hp = enemy["health"] + (enemy_level - 1) * 10
        battle_data[user_id] = {
            "enemy": enemy_name,
            "enemy_level": enemy_level,
            "enemy_hp": scaled_hp,
            "player_turn": True,
            "defending": False,
            "cooldowns": {}
        }
        save_battles(battle_data)
        embed = discord.Embed(title=f"Bạn đã bắt đầu chiến đấu với {enemy['name']} L{enemy_level}!", color=0x00ff00)
        embed.add_field(name="HP của bạn", value=f"{user['hp']} HP", inline=False)
        embed.add_field(name=f"{enemy['name']} HP", value=f"{battle_data[user_id]['enemy_hp']} HP", inline=False)
        embed.add_field(name="Hành động", value="Sử dụng lệnh !attack để tấn công kẻ thù! hay !defend để phòng thủ! hay !skill <skill_name> để sử dụng kỹ năng!", inline=False)
        await interaction.response.send_message(embed=embed)
class EnemySelectView(View):
    def __init__(self): 
        super().__init__()
        self.add_item(EnemySelect())
        
