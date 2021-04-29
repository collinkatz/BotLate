import discord
from Translator import Translator


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-bl join'):
        try:
            channel = message.author.voice.channel
            voice_channel = await channel.connect()
        except discord.errors.ClientException:
            await message.channel.send("I'm already connected to a channel!")

    if message.content.startswith('-bl play'):
        voice_client = client.voice_clients[0]
        voice_client.stop()
        encoded_audio = discord.FFmpegOpusAudio("./audio_data/output.mp3")
        voice_client.play(encoded_audio)

    if message.content.startswith('-bl leave'):
        voice_client = client.voice_clients[0]
        await voice_client.disconnect()


client.run('ODM2ODAyNjAwMjg0MDYxNzA1.YIjTJg.NH1Y0Ki3Hxx82uQZH9Wv44yiVfI')
