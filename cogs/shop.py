from discord.ext import commands
import discord
import json
from utils.data_manager import load_users, save_users, load_json,ensure_user_fields
SHOP_ITEMS = load_json('data/items.json')
class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Shop", description="Các vật phẩm có sẵn để mua", color=0x00ff00)

        for item_key, item in SHOP_ITEMS.items():
            embed.add_field(name=item["name"], value=f"Giá: {item['price']} gold", inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    async def buy(self, ctx, item_name):
        user_id = str(ctx.author.id)

        users = load_users()
        if user_id not in users:
            await ctx.send("Bạn chưa bắt đầu trò chơi, hãy sử dụng lệnh !begin để bắt đầu.")
            return
        
        user = users[user_id]
        ensure_user_fields(user)

        if item_name not in SHOP_ITEMS:
            await ctx.send("Vật phẩm không tồn tại trong shop!")
            return
        
        price = SHOP_ITEMS[item_name]["price"]

        if user["gold"] < price:
            await ctx.send("Bạn không đủ gold để mua vật phẩm này!")
            return
        
        user["gold"] -= price
        if "inventory" not in user:
            user["inventory"] = []
        user["inventory"].append(item_name)

        save_users(users)

        await ctx.send(f"Bạn đã mua {SHOP_ITEMS[item_name]['name']} thành công!")
    @commands.command()
    async def help_shop(self, ctx):
        embed = discord.Embed(title="Hướng dẫn lệnh shop", color=0x00ff00)
        embed.add_field(name="!shop", value="Xem các vật phẩm có sẵn để mua trong shop.", inline=False)
        embed.add_field(name="!buy <item_name>", value="Mua một vật phẩm từ shop nếu bạn có đủ vàng.", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))