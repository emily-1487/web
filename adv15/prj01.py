######################模組####################
import discord
import os
from dotenv import load_dotenv
from myfuntion.myfuntion import WeatherAPI
import openai

#####################初始化###################
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)
weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")


# 333333
####################事件###################
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await tree.sync()


channel_games = {}


@bot.event
async def on_message(message):
    channel_id = message.channel.id
    if message.author == bot.user:
        return
    if message.content == "hello":
        await message.channel.send("Hey!")
    elif channel_id in channel_games:
        user_input = message.content.strip()
        if user_input == "結束遊戲":
            channel_games.pop(channel_id)
            await message.channel.send("遊戲已結束，期待下次再玩")
        else:
            game_data = channel_games[channel_id]["game_data"]
            if "history" not in [channel_id]["game_data"]:
                channel_games[channel_id]["history"] = []
            history = channel_games[channel_id]["history"]
            history.append({"role": "user", "content": user_input})
            messages = (
                [
                    {
                        "role": "system",
                        "content": f"""
你是一個海龜湯遊戲的主持人，根據以下的謎題回答玩家的提問。
妳的回應只能是[是]、[不是]、[無可奉告]、[恭喜答對]，並盡可能簡短。
當玩家要求提示的時候，你可以回答"關鍵字"當作提示。
謎題:{game_data["question"]}
解答:{game_data["answer"]}
                    """,
                    }
                ]
                + history
            )
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.5,
                )
                answer = response.choices[0].message.content
                if answer == "恭喜答對":
                    game_data["solved"] = True
                    await message.channel.send("恭喜你們，答對了!遊戲結束！")
                    channel_games.pop(channel_id)
                else:
                    history.append({"role": "assistant", "content": answer})
                    channel_games[channel_id]["history"] = history
                    await message.channel.send(answer)
                    print(messages)
            except Exception as e:
                await message.channel.send(f"抱歉，發生錯誤：{e}")
    else:
        await bot.proses_command(message)


##############指令###################
@tree.command(name="hello", description="Say hello to your bot!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hey!")


@tree.command(name="weather", description="取得天氣資訊")
async def weather(
    interaction: discord.Interaction,
    city: str,
    forrecast: bool = False,
    ai: bool = False,
):
    await interaction.response.defer()
    unit_symbol = "C" if weather_api.units == "metric" else "F"
    if not forrecast:
        info = weather_api.get_current_weather(city)
        if "weather" in info and "main" in info:
            current_temprature = info["main"]["temp"]
            weather_description = info["weather"][0]["description"]
            icon_code = info["weather"][0]["icon"]
            icon_url = weather_api.get_icon_url(icon_code)
            embed = discord.Embed(
                title=f"{city}的當前天氣",
                description=f"描述:{weather_description}",
                color=0x1E90FF,
            )
            embed.set_thumbnail(url=icon_url)
            embed.add_field(
                name="溫度", value=f"{current_temprature}度{unit_symbol}", inline=False
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"找不到**{city}**的天氣資訊。")
    else:
        info = weather_api.get_forecast(city)
        if "list" in info:
            if not ai:
                forrecast_list = info["list"][:10]
                embeds = []
                for forrecast in forrecast_list:
                    dt_txt = forrecast["dt_txt"]
                    temp = forrecast["main"]["temp"]
                    description = forrecast["weather"][0]["description"]
                    icon_code = forrecast["weather"][0]["icon"]
                    icon_url = weather_api.get_icon_url(icon_code)
                    embed = discord.Embed(
                        title=f"{city}天氣預報-{dt_txt}",
                        decription=f"描述{description},color=0x1E90FF",
                    )
                    embed.set_thumbnail(url=icon_url)
                    embed.add_field(
                        name="溫度", value=f"{temp}度{unit_symbol}", inline=False
                    )
                    embeds.append(embed)
                await interaction.followup.send(embeds=embeds)
            else:
                try:
                    reponse = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {
                                "role": "system",
                                "content": "你是一個專業的氣象分析師，請根據用戶的輸入，回答用戶的問題。",
                            },
                            {
                                "role": "user",
                                "content": f"以下是{city}的未來天氣預報。請根據這些數據提供詳細的天氣預報。\n{info}",
                            },
                        ],
                        temperature=0.2,
                    )
                    analysis = reponse.choices[0].message.content
                    await interaction.followup.send(
                        "**{city}**的天氣分析:\n{analysis}。"
                    )
                except Exception as e:
                    await interaction.followup.send(f"發生錯誤：{e}")
        else:
            await interaction.followup.send(f"找不到**{city}**的天氣預報。")


@tree.command(name="turtle_soup", description="開始海龜湯遊戲")
async def turtle_soup(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    if channel_id in channel_games:
        await interaction.response.send_message(
            "這個頻道已經有正在進行的遊戲", ephemeral=True
        )
    else:
        channel_games[channel_id] = {
            "games_data": {
                "question": "一個人在沙漠中發現了一具屍體，旁邊有一根繞過的火柴。發生了甚麼事?",
                "answer": "她參加了熱氣球比賽，為了減重需要有人跳下去，他抽到了最短的火柴，只好跳下。",
                "solved": False,
            },
            "history": [],
        }
        await interaction.response.send_message(
            f"""
遊戲開始!
題目:{channel_games[channel_id]["game_data"]["question"]}
請大家開始提問，輸入ˋ結束遊戲ˋ可結束遊戲。  
我的回應只會是[是],[不是]或[無可奉告]。
            """
        )


#####################啟動#####################
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()
