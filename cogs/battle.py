import discord
from discord.ext import commands
import random
import json
from utils.data_manager import *
from utils.level_system import check_level_up
ENEMIES = load_json('data/enemies.json')

class Battle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def fight(self, ctx, enemy_name):
            user_id = str(ctx.author.id)

            users = load_users()

            battle_data = load_battles()

            if user_id not in users:
                await ctx.send("Bạn chưa bắt đầu trò chơi, hãy sử dụng lệnh !begin để bắt đầu.")
                return
        
            user = users[user_id]
            ensure_user_fields(user)
            save_users(users)

            if enemy_name not in ENEMIES:
                await ctx.send("Không tìm thấy kẻ thù này!")
                return
            
            if user_id not in battle_data:
                
                enemy_data = ENEMIES[enemy_name]

                battle_data[user_id] = {
                    "enemy": enemy_name,
                    "enemy_hp": enemy_data["health"]
                }

            battle = battle_data[user_id]
            enemy = ENEMIES[battle["enemy"]]

            player_damage = random.randint(max(1, user["attack"] - 5), user["attack"])

        
            battle["enemy_hp"] -= player_damage

            if battle["enemy_hp"] <= 0:
                user["exp"] += enemy["exp"]
                user["gold"] += enemy["gold"]

                level_up = check_level_up(user)

                save_users(users)

                del battle_data[user_id]

                save_battles(battle_data)

                embed = discord.Embed(title="Bạn đã đánh bại " + enemy["name"] + "!", color=0x00ff00)

                embed.add_field(name="Phần thưởng", value=f"EXP: {enemy['exp']}, Gold: {enemy['gold']}", inline=False)

                await ctx.send(embed=embed)

                if level_up:
                    await ctx.send(f"Chúc mừng bạn đã lên cấp! Bạn hiện tại là cấp {user['level']} với {user['hp']} HP, {user['attack']} Attack và {user['defense']} Defense.")
                return

            enemy_damage = random.randint(1, enemy["attack"])

            enemy_damage = max(1, enemy_damage - user["defense"])

            user["hp"] -= enemy_damage
            if user_id in battle_data:
                    current_enemy = battle_data[user_id]["enemy"]
                    if current_enemy != enemy_name:
                     await ctx.send("Bạn đang chiến đấu với một kẻ thù khác! Hãy hoàn thành trận chiến hiện tại trước khi chiến đấu với kẻ thù mới.")
                     return
            if user["hp"] <= 0:
                user["hp"] = 0

                save_users(users)

                del battle_data[user_id]

                save_battles(battle_data)

                save_users(users)

                await ctx.send(f"Bạn đã bị " + enemy["name"] + " đánh bại! Hãy cố gắng hơn lần sau.")
                return
            save_users(users)
            save_battles(battle_data)

            embed = discord.Embed(title=f"Đang chiến đấu với {enemy['name']}", color=0x00ff00)

            embed.add_field(name="Bạn gây ra", value=f"{player_damage} damage", inline=False)

            embed.add_field(name=f"{enemy['name']} còn lại", value=f"{battle['enemy_hp']} HP", inline=False)

            embed.add_field(name=f"{enemy['name']} phản đòn", value=f"{enemy_damage} damage", inline=False)

            embed.add_field(name="HP của bạn", value=f"{user['hp']} HP", inline=False)


            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Battle(bot))
