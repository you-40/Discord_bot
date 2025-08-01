# 「/neko」に「にゃーん」を返る

async def cat(message):
    if message.content == '/neko':
        await message.channel.send('にゃーん')
    