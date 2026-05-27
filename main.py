import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# Đọc file .env để lấy token của bot
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Khai báo intents để bot có thể đọc nội dung tin nhắn
intents = discord.Intents.default()
intents.message_content = True
# Tạo bot với prefix là '!' và sử dụng intents đã khai báo
bot = commands.Bot(command_prefix='!', intents=intents)

# Khi bot đã sẵn sàng, in ra thông báo và tên của bot
@bot.event
async def on_ready():
    print(f'Bot đã sẵn sàng! Đăng nhập với tên: {bot.user}')
    print("Các lệnh hiện có:")
    for command in bot.commands:
        print(f" - {command.name}")

@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)


async def main():
    async with bot:
        await bot.load_extension('cogs.profile')
        await bot.load_extension('cogs.economy')
        await bot.load_extension('cogs.inventory')
        await bot.load_extension('cogs.shop')
        await bot.load_extension('cogs.battle')
        await bot.start(TOKEN)
  
@bot.event
async def on_message(message):
    print(f"Nhận được: {message.content}")
    await bot.process_commands(message)

asyncio.run(main())
  