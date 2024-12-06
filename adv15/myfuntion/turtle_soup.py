import openai
import json
import random
import os
import sys


class TurtleSoupGame:
    def __init__(self, openai_client: openai):
        self.openai_client = openai_client
        self.game = {}
        self.questions = []

    def load_questions(self):
        try:
            os.chdir(sys.path[0])
            json_path = "turtle_soup.json"
            with open(json_path, "r", encoding="utf-8") as f:
                self.questions = json.load(f)
        except Exception as e:
            print(f"載入遊戲問題時發生錯誤:{str(e)}")
            self.questions = [
                {
                    "question": "一個人在沙漠中發生了一具屍體，旁邊有一根燒過的火柴。發生了甚麼事?：",
                    "answer": "她參加了熱氣球比賽，為了減重需要有人跳下去，他抽到了最短的火柴，只好跳下。",
                    "solved": False,
                }
            ]

    def start_game(self, channel_id):
        if channel_id in self.game:
            return False, "這個頻道已經有正愛進行的遊戲!"
        self.load_questions()
        selected_question = random.choice(self.questions).copy()
        self.game[channel_id] = {
            "game_data": selected_question,
            "history": [],
        }
        return True, self.games[channel_id]["game_data"]["question"]

    def end_game(self, channel_id):
        if channel_id in self.game:
            self.game.pop(channel_id)
            return True
        return False

    async def process_answer(self, channel_id, user_input):
        if channel_id not in self.games:
            return None, "沒有進行中的遊戲"
        game_data = self.games[channel_id]
        history = game_data.setdefault("history", [])
        history.append({"role": "user", "content": user_input})
        messages = (
            [
                {
                    "role": "system",
                    "content": f"""
你是一個海龜湯遊戲的主持人，根據以下謎題回答玩家的提問。
妳的回應只能是[是]、[不是]、[無可奉告]、[恭喜答對!]，並盡可能簡短。
當玩家要求提示的時候，你可以提供一些"關鍵字"當作提示。
謎題：{game_data["game_data"]["question"]}
解答:{game_data["game_data"]["answer"]}
                    """,
                }
            ]
            + history
        )
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.5,
            )
            answer = response.choices[0].message.content
            if answer == "恭喜答對!":
                game_data["game_data"]["solved"] = True
                self.end_game(channel_id)
                return True, answer
            else:
                history.append({"role": "assistant", "content": answer})
                return False, answer
        except Exception as e:
            return None, f"處理回答時發生錯誤:{str(e)}"

    def is_active_game(self, channel_id):
        return channel_id in self.games
