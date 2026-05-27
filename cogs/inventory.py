import discord
from discord.ext import commands
import json
from utils.data_manager import load_users, save_users
class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def inventory(self, ctx):
        user_id = str(ctx.author.id)

        users = load_users()

        if user_id not in users:
            await ctx.send("Bạn chưa bắt đầu trò chơi, hãy sử dụng lệnh !begin để bắt đầu.")
            return  
        user = users[user_id]

        inventory = user.get("inventory", [])

        if len(inventory) == 0:
            await ctx.send("Kho đồ của bạn đang trống!")
            return
        item_list = ""

        for item in inventory:
            item_list += f"- {item}\n"

        embed = discord.Embed(title=f"{user['name']}'s Inventory", description=item_list, color=0x00ff00)

        embed.add_field(name="Items", value=item_list, inline=False)

        await ctx.send(embed=embed)
    @commands.command()
    async def use(self, ctx, item_name):

        user_id = str(ctx.author.id)

        users = load_users()

        if user_id not in users:
            await ctx.send("Bạn chưa bắt đầu trò chơi, hãy sử dụng lệnh !begin để bắt đầu.")
            return
        
        user = users[user_id]

        inventory = user.get("inventory", [])

        if item_name not in inventory:
            await ctx.send("Bạn không có vật phẩm này trong kho đồ!")
            return
        
        if item_name == "potion":

            heal_amount = 50
            user["hp"] = min(user.get("hp", 100) + heal_amount, user.get("max_hp", 100))

            inventory.remove(item_name)

            save_users(users)

            await ctx.send(f"Bạn đã sử dụng {item_name} và hồi phục {heal_amount} HP!")

            return
        await ctx.send("Vật phẩm này không thể sử dụng được!")

async def setup(bot):
    await bot.add_cog(Inventory(bot))