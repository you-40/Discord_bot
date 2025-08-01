import discord
import os
import imageio_ffmpeg
from datetime import datetime as dt
from dotenv import load_dotenv
from cogs.cat import cat
from cogs.exit import exit_channel
from cogs.timer import pomodoro_timer
from cogs.birthday import birthday

load_dotenv()
TOKEN = os.getenv("TOKEN") # ボットのトークンを入れる
# CHANNEL_ID = 0000000000000  # サーバーのIDを入れる（省略可）\
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()
intents.presences = True  # プレゼンス情報を取得
intents.members = True  # サーバーメンバー情報を取得
intents.message_content = True  # メッセージの内容を取得するために必要
client = discord.Client(command_prefix="/", intents=intents)

@client.event
# 起動時に動作する処理
async def on_ready():
    print(f"{client.user}としてログインしました！")


@client.event
# メッセージ受信時に動作する処理
async def on_message(message):
    if message.author.bot: # メッセージ送信者がBotだった場合は無視する
        return
    
    await cat(message)
    await exit_channel(message)
    await pomodoro_timer(message, ffmpeg_path)


@client.event
# 入退室時に動作する処理
async def on_voice_state_update(member, before, after):
    target_user_id = int(os.getenv("SHIBA"))
    await birthday(member, before, after, target_user_id, client, ffmpeg_path)

client.run(TOKEN)


