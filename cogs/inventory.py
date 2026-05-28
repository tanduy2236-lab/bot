import discord
from discord.ext import commands
import json
from utils.data_manager import load_users, save_users, load_json
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
    @commands.command()
    async def equip(self, ctx, item_name):
        user_id = str(ctx.author.id)

        users = load_users()

        if user_id not in users:
            await ctx.send("Bạn chưa bắt đầu trò chơi, hãy sử dụng lệnh !begin để bắt đầu.")
            return
        
        user = users[user_id]
        items = load_json('data/items.json')
        if item_name not in items:
            await ctx.send("Vật phẩm này không tồn tại!")
            return

        if item_name not in user.get("inventory", []):
            await ctx.send("Bạn không có vật phẩm này trong kho đồ!")
            return

        if items[item_name]["type"] == "weapon":
            if user.get("equipped_weapon"):
                await ctx.send(f"Bạn đã trang bị {user['equipped_weapon']}, hãy tháo nó ra trước khi trang bị {item_name}.")
                return
            else:
                user["equipped_weapon"] = item_name
                user["attack"] += items[item_name].get("attack_power", 0)
                save_users(users)
                await ctx.send(f"Bạn đã trang bị {item_name} và tăng {items[item_name].get('attack_power', 0)} điểm tấn công!")
        elif items[item_name]["type"] == "armor":
            if user.get("equipped_armor"):
                await ctx.send(f"Bạn đã trang bị {user['equipped_armor']}, hãy tháo nó ra trước khi trang bị {item_name}.")
                return
            else:
                user["equipped_armor"] = item_name
                user["defense"] += items[item_name].get("defense_power", 0)
                save_users(users)
                await ctx.send(f"Bạn đã trang bị {item_name} và tăng {items[item_name].get('defense_power', 0)} điểm phòng thủ!")
        else:
            await ctx.send("Vật phẩm này không thể trang bị được!")
        save_users(users)

        await ctx.send(f"Bạn đã trang bị {item_name} thành công!")

async def setup(bot):
    await bot.add_cog(Inventory(bot))