from discord.ext import commands
import json
import os
from datetime import datetime, timedelta
from utils.data_manager import load_users, save_users,ensure_user_fields
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def daily(self, ctx):
        try:
        
            user_id = str(ctx.author.id)

            if not os.path.exists('data/users.json'):
                await ctx.send("Bạn chưa bắt đầu trò chơi, hãy sử dụng lệnh !begin để bắt đầu.")
                return

            users = load_users()

            if user_id not in users:
                await ctx.send("Bạn chưa bắt đầu trò chơi, hãy sử dụng lệnh !begin để bắt đầu.")
                return
            users[user_id] = ensure_user_fields(users[user_id])

            last_daily = users[user_id].get("last_daily", "")
            now = datetime.now()

            if last_daily:
                last_daily_time = datetime.strptime(last_daily, "%Y-%m-%d %H:%M:%S")
                if now - last_daily_time < timedelta(hours=24):
                    remaining_time = timedelta(hours=24) - (now - last_daily_time)
                    await ctx.send(f"Bạn đã nhận phần thưởng hàng ngày rồi! Hãy thử lại sau {remaining_time}.")
                    return

            reward_gold = 50
            users[user_id]["gold"] += reward_gold
            users[user_id]["last_daily"] = now.strftime("%Y-%m-%d %H:%M:%S")

            save_users(users)

            await ctx.send(f"Bạn đã nhận được {reward_gold} vàng từ phần thưởng hàng ngày!")
        except Exception as e:
            await ctx.send("Đã xảy ra lỗi khi nhận phần thưởng hàng ngày. Vui lòng thử lại sau.")
            print(f"Lỗi trong lệnh daily: {e}")

async def setup(bot):
    await bot.add_cog(Economy(bot))