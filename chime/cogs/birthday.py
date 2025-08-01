# 特定ユーザー入室時に曲を流す

import discord

# target_user入室時に指定の音楽を流す
async def birthday(member, before, after, target_user_id, client, ffmpeg_path):
    # 対象ユーザーかどうか
    if member.id != target_user_id:
        return
    # ユーザーがボイスチャンネルに入ったとき
    if before.channel is None and after.channel is not None:
        voice_channel = after.channel

        # Botが既にVCにいたらスキップ（複数再生防止）
        if any(client.user.id == m.id for m in voice_channel.members):
            return

        # ボイスチャンネルに接続
        await voice_channel.connect()

        # 音声を再生
        audio_source = discord.FFmpegPCMAudio("media/happy-birthday.mp3", executable=ffmpeg_path)
        audio_source = discord.PCMVolumeTransformer(audio_source, volume=0.1)
        member.guild.voice_client.play(audio_source)

        # # 再生が終わるまで待機して切断
        # while vc.is_playing():
        #     await asyncio.sleep(1)
        # await vc.disconnect()