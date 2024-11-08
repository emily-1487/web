####################################模組####################################
import discord
import os
from dotenv import load_dotenv
from myfuntion.myfuntion import WeatherAPI

####################################初始化########################################
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)
weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))


####################################事件####################################
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await tree.sync()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello":
        await message.channel.send("Hey!")


####################################指令####################################
@tree.command(name="hello", description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hey!")


@tree.command(name="Weather", description="取得天氣資訊")
async def weather(interaction: discord.Integration, city: str, forecast: bool = False):
    await interaction.response.defer()
    unit_symbol = "C" if weather_api.units == "metric" else "F"


####################################啟動##################################
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


# 主程式
if __name__ == "__main__":
    main()

# test s
