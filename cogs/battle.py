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
                "enemy_hp": enemy_data["health"],
                "player_turn": True,
                "defending": False
                }
            
            save_battles(battle_data)

        embed = discord.Embed(title=f"Bạn đã bắt đầu chiến đấu với {ENEMIES[enemy_name]['name']}!", color=0x00ff00)
        embed.add_field(name="HP của bạn", value=f"{user['hp']} HP", inline=False)
        embed.add_field(name=f"{ENEMIES[enemy_name]['name']} HP", value=f"{battle_data[user_id]['enemy_hp']} HP", inline=False)
        embed.add_field(name="Hành động", value="Sử dụng lệnh !attack để tấn công kẻ thù!", inline=False)
        await ctx.send(embed=embed)
    async def enemy_turn(self, ctx,user, enemy, battle):
            users = load_users()
     
            battle_data = load_battles()

            user_id = str(ctx.author.id)

            user = users[user_id]

            battle = battle_data[user_id]

            enemy_damage = random.randint(1, enemy["attack"])
            if battle["defending"]:
                enemy_damage //= 2
            enemy_damage = max(1, enemy_damage - user["defense"])
            user["hp"] -= enemy_damage
            battle["defending"] = False
            battle["player_turn"] = True

            if user["hp"] <= 0:
                user["hp"] = 0
                del battle_data[user_id]
                save_users(users)
                save_battles(battle_data)

                embed = discord.Embed(title="Bạn đã bị đánh bại bởi " + enemy["name"] + "!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            save_users(users)
            save_battles(battle_data)
            embed = discord.Embed(title=f"{enemy['name']} đã tấn công bạn!", color=0xff0000)
            embed.add_field(name=f"{enemy['name']} gây ra", value=f"{enemy_damage} damage", inline=False)
            embed.add_field(name="HP của bạn", value=f"{user['hp']} HP", inline=False)
            await ctx.send(embed=embed)


    @commands.command()
    async def attack(self, ctx):
            user_id = str(ctx.author.id)

            users = load_users()
            battle_data = load_battles()

            if user_id not in battle_data:
                await ctx.send("Bạn không đang chiến đấu với kẻ thù nào! Sử dụng lệnh !fight <enemy_name> để bắt đầu chiến đấu.")
                return
            
            user = users[user_id]
            ensure_user_fields(user)

            battle = battle_data[user_id]
            ensure_battle_fields(battle)
            if not battle["player_turn"]:
                await ctx.send("Chưa đến lượt bạn! Hãy chờ đối thủ tấn công xong.")
                return
            enemy = ENEMIES[battle["enemy"]]

            player_damage = random.randint(max(1, user["attack"] - 5), user["attack"])

            battle["enemy_hp"] -= player_damage
            battle["player_turn"] = False

            if battle["enemy_hp"] <= 0:
                battle["enemy_hp"] = 0

                user["exp"] += enemy["exp"]
                user["gold"] += enemy["gold"]

                level_up = check_level_up(user)
                save_users(users)

                del battle_data[user_id]
                save_battles(battle_data)

                embed = discord.Embed(title="Bạn đã đánh bại " + enemy["name"] + "!", color=0x00ff00)
                embed.add_field(name="Phần thưởng", value=f"EXP: {enemy['exp']}, Gold: {enemy['gold']}", inline=False)
                await ctx.send(embed=embed)
                return
            
      
            save_users(users)
            save_battles(battle_data)
            embed = discord.Embed(title=f"Đang chiến đấu với {enemy['name']}", color=0x00ff00)
            embed.add_field(name="Bạn gây ra", value=f"{player_damage} damage", inline=False)
            embed.add_field(name=f"{enemy['name']} còn lại", value=f"{battle['enemy_hp']} HP", inline=False)
            embed.add_field(name="HP của bạn", value=f"{user['hp']} HP", inline=False)
            embed.add_field(name="Hành động tiếp theo", value="Sử dụng lệnh !attack để tiếp tục tấn công kẻ thù!", inline=False)
            await ctx.send(embed=embed)
            await self.enemy_turn(ctx,user, enemy, battle)
    @commands.command()
    async def defend(self, ctx):
            user_id = str(ctx.author.id)

            users = load_users()
            battle_data = load_battles()

            if user_id not in battle_data:
                await ctx.send("Bạn không đang chiến đấu với kẻ thù nào! Sử dụng lệnh !fight <enemy_name> để bắt đầu chiến đấu.")
                return
            user = users[user_id]
            battle = battle_data[user_id]
            enemy_data = ENEMIES[battle["enemy"]]
            if not battle["player_turn"]:
                await ctx.send("Chưa đến lượt bạn! Hãy chờ đối thủ tấn công xong.")
                return
            battle["defending"] = True
            battle["player_turn"] = False
            save_battles(battle_data)

            embed = discord.Embed(title="Phòng thủ!", description="Bạn đang phòng thủ trước đòn tấn công của kẻ thù!", color=0x00ff00)
            embed.add_field(name=f"{enemy_data['name']} đang chuẩn bị tấn công bạn!", value="Hãy chờ đòn tấn công của kẻ thù!", inline=False)
            await ctx.send(embed=embed)
            await self.enemy_turn(ctx,user, enemy_data, battle)



async def setup(bot):
    await bot.add_cog(Battle(bot))
