from discord.ext import commands
import discord
import json
import os
from utils.data_manager import load_users, save_users
from utils.level_system import get_exp_to_next_level
class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="begin")
    async def start_game(self,ctx):
        
        print("Đã vào lệnh start")
        user_id = str(ctx.author.id)

        if not os.path.exists('data/users.json'):
            users = {}
        else:
            users = load_users()

        if user_id in users:
            await ctx.send("Bạn đã bắt đầu trò chơi rồi!")
            return
        
        users[user_id] = {
            "name": ctx.author.name,
            "level": 1,
            "exp":0,
            "gold": 100,
            "last_daily": "",
            "inventory": [],
            "hp": 100,
            "max_hp": 100,
            "attack": 10,
            "defense": 5,
            "equipped_weapon": None,
            "equipped_armor": None
        }
        save_users(users)
        await ctx.send("Bạn đã bắt đầu trò chơi thành công!")

    @commands.command()
    async def profile(self, ctx):
        user_id = str(ctx.author.id)

        users = load_users()

        if user_id not in users:
            await ctx.send("Bạn chưa bắt đầu trò chơi, hãy sử dụng lệnh !begin để bắt đầu.")
            return  
        
        user = users[user_id]

        embed = discord.Embed(title=f"{user['name']}", description="Thông tin cơ bản", color=0x00ff00)
   
        embed.add_field(name="Level", value=f"{user['level']}", inline=False)
        
        embed.add_field(name="EXP", value=f"{user['exp']} / {get_exp_to_next_level(user['level'])}", inline=False)

        embed.add_field(name="Attack", value=f"{user.get('attack', 10)}", inline=False)

        embed.add_field(name="Defense", value=f"{user.get('defense', 5)}", inline=False)

        embed.add_field(name="Gold", value=f"{user['gold']}", inline=False)

        embed.add_field(name="HP", value=f"{user.get('hp', 50)}/{user.get('max_hp', 100)}", inline=False)

        embed.add_field(name="Equipped Weapon", value=f"{user.get('equipped_weapon', 'None')}", inline=False)

        embed.add_field(name="Equipped Armor", value=f"{user.get('equipped_armor', 'None')}", inline=False)

        await ctx.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(Profile(bot))