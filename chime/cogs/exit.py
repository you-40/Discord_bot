# ボイスチャットからの退出

async def exit_channel(message):
    if message.content == '/exit':
        await message.guild.voice_client.disconnect()
   