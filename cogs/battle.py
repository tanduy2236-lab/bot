import discord
from discord.ext import commands
import random
import json
from utils.data_manager import load_users, save_users, load_json
from utils.level_system import check_level_up
ENEMIES = load_json('data/enemies.json')

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    try:
        @commands.command()
        async def fight(self, ctx, enemy_name):
            user_id = str(ctx.author.id)

            users = load_users()

            if user_id not in users:
                await ctx.send("Bạn chưa bắt đầu trò chơi, hãy sử dụng lệnh !begin để bắt đầu.")
                return
        
            user = users[user_id]

            if enemy_name not in ENEMIES:
                await ctx.send("Không tìm thấy kẻ thù này!")
                return
        
            enemy = ENEMIES[enemy_name]

            player_damage = random.randint(5, 15)
            enemy_damage = random.randint(1, enemy["attack"])

            user["hp"] -= enemy_damage

            if user["hp"] <= 0:
                user["hp"] = 0

            user["exp"] += enemy["exp"]
            user["gold"] += enemy["gold"]

            level_up = check_level_up(user)
            if level_up:
                message = f"Chúc mừng bạn đã lên cấp {user['level']}!"
            await ctx.send(message)
            save_users(users)

            embed = discord.Embed(title="Bạn chiến đấu với " + enemy["name"], color=0x00ff00)

            embed.add_field(name="Bạn gây sát thươmng", value=f"{player_damage} damage", inline=False)

            embed.add_field(name=f"{enemy['name']} gây sát thương", value=f"{enemy_damage} damage", inline=False)

            embed.add_field(name="Phần thưởng", value=f"EXP: {enemy['exp']}, Gold: {enemy['gold']}", inline=False)

            embed.add_field(name="HP hiện tại", value=f"{user['hp']}/{user.get('max_hp', 100)}", inline=False)

            await ctx.send(embed=embed)
    except Exception as e:
        print(f"Lỗi trong lệnh fight: {e}")

async def setup(bot):
    await bot.add_cog(Battle(bot))
