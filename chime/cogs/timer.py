# ポモドーロタイマーセット 

import discord
import asyncio
import re

async def pomodoro_timer(message, ffmpeg_path):
    # メッセージが"/数字"であった時の処理
    if re.match(r"^/\d+(\.\d+)?\s\d+(\.\d+)?(\s\d+(\.\d+)?)?$", message.content):
        # メッセージが送信されたサーバーのボイスチャンネルを探す
        voice_channel = None 
        if message.guild:  # サーバー内のメッセージであることを確認
            for channel in message.guild.voice_channels:
                if len(channel.members) > 0:  # 参加者がいるチャンネルを探す
                    voice_channel = channel
                    break
            else:
                await message.channel.send('ボイスチャンネルが静かだね...')
                return
            print(f'{voice_channel.name}に行くよ！')

            print(f"ボイスチャンネル {voice_channel.name} に {len(voice_channel.members)} 人が参加しています！")
            user_set_time = message.content.lstrip(message.content[0]) # 入力情報を取得
            parts = user_set_time.split(' ')
            if len(parts) <= 1 or len(parts) >= 4:
                await message.channel.send('集中時間(分) 休憩時間(分) 回数(回)を半角区切りで入力してね')
                await message.channel.send('回数はオプションだよ')
            elif len(parts) == 2:
                loop_count = 2
                work_time, break_time = parts
            elif len(parts) == 3:
                work_time, break_time, loop_count = parts

            if message.guild.voice_client is None: # まだ参加してなければ
                await voice_channel.connect()

            for n in range(1, int(loop_count) + 1):
                print(f'{work_time}分後にチャイムを鳴らすよ！')
                await message.channel.send(f"{work_time} 分がんばろう！",silent=True)
                await asyncio.sleep((float(work_time) * 60)/2)  # 分 → 秒に変換して待機
                # await message.channel.send('あと半分だよ！', silent=True)
                print("あと半分！")
                await asyncio.sleep((float(work_time) * 60)/2)  # 分 → 秒に変換して待機
                
                audio_source = discord.FFmpegPCMAudio("media/schoolchime_NHK.mp3", executable=ffmpeg_path)
                audio_source = discord.PCMVolumeTransformer(audio_source, volume=0.1)
                message.guild.voice_client.play(audio_source)

                # await message.channel.send(f"休憩は{break_time}分！", silent=True)
                print(f'休憩{break_time}分！')
                await asyncio.sleep(float(break_time) * 60)

                audio_source = discord.FFmpegPCMAudio("media/schoolchime_NHK.mp3", executable=ffmpeg_path)
                audio_source = discord.PCMVolumeTransformer(audio_source, volume=0.1)
                message.guild.voice_client.play(audio_source)

                # await message.channel.send(f"{n}クール目終了！", silent=True)

            # await message.channel.send("おつかれさまでした！", silent=True)
            print("おつかれ！")
        else:
            print('サーバー内のメッセージではありません')