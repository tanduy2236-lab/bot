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
@bot.event
async def on_command_error(ctx, error):
    print("ERROR:", repr(error))
@bot.command()
async def tutorial(ctx):
    embed = discord.Embed(title="Hướng dẫn sử dụng bot", description="Các lệnh cơ bản để bắt đầu chơi game.", color=0x00ff00)
    embed.add_field(name="!begin", value="Bắt đầu trò chơi và tạo hồ sơ cho bạn.", inline=False)
    embed.add_field(name="!profile", value="Xem thông tin hồ sơ của bạn, bao gồm cấp độ, EXP, vàng, v.v.", inline=False)
    embed.add_field(name="!daily", value="Nhận phần thưởng hàng ngày (vàng). Có thể nhận lại sau 24 giờ.", inline=False)
    embed.add_field(name="!shop", value="Xem các vật phẩm có sẵn để mua trong shop.", inline=False)
    embed.add_field(name="!buy <item_name>", value="Mua một vật phẩm từ shop nếu bạn có đủ vàng.", inline=False)
    embed.add_field(name="!inventory", value="Xem kho đồ của bạn, bao gồm các vật phẩm và trang bị đang sử dụng.", inline=False)
    embed.add_field(name="!use <item_name>", value="Sử dụng một vật phẩm tiêu hao trong kho đồ của bạn.", inline=False)
    embed.add_field(name="!equip <item_name>", value="Trang bị một vũ khí hoặc áo giáp từ kho đồ của bạn để tăng thuộc tính.", inline=False)
    embed.add_field(name="!unequip <item_name>", value="Tháo một vũ khí hoặc áo giáp đang trang bị để giảm thuộc tính.", inline=False)
    embed.add_field(name="!fight <enemy_name>", value="Bắt đầu chiến đấu với kẻ thù đã chọn.", inline=False)
    embed.add_field(name="!attack", value="Tấn công kẻ thù trong lượt của bạn.", inline=False)
    embed.add_field(name="!defend", value="Phòng thủ để giảm sát thương từ đòn tấn công tiếp theo của kẻ thù.", inline=False)
    embed.add_field(name="!skill <skill_name>", value="Sử dụng kỹ năng đặc biệt (nếu có) để tấn công kẻ thù.", inline=False)
    await ctx.send(embed=embed)
   
asyncio.run(main())
  