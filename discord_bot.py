import discord
from Translator import Translator
import os
import time

trans = Translator()
supported_langs = trans.speech_langs
client = discord.Client()

COMMAND_PREFIX = '-bl'
CONFIG = {"lang": "Spanish", "voice_mode": "female"}
KEYWORDS = [COMMAND_PREFIX, 'join', 'leave', 'play', 'translate']


def is_key_word(word):
    for key_word in KEYWORDS:
        if word == key_word:
            return True
    return False


def parse_key_words(args):
    arglist, left_overs = parse_key_words_r(args, [])
    print(arglist, left_overs)
    return arglist, left_overs


def parse_key_words_r(args, arglist):
    print(args)
    word = args[0]
    if is_key_word(word):
        arglist.append(word)
        args.pop(0)
        return parse_key_words_r(args, arglist)
    else:
        return arglist, args


def parse_command_args(message):
    """
    This function separates out the command, arguments, and data from a user entered command
    :param message: The command message the user entered
    :return: command, A string: the command specified by the user, arg_list, A list of strings representing the arguments passed by the user, data, A string: the data after the arguments passed by the user
    """
    args = str(message.content).split(" ")
    args.pop(0) # removes command prefix
    arg_list, data = parse_key_words(args)
    data = ' '.join(data) # create data/sentence from leftover stuff in args
    command = arg_list.pop(0) # first arg in arglist is always command
    return command, arg_list, data


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


async def disconnect_vc(connected_voice_client):
    """
    Disconnects a specified voice client from a voice channel
    :param connected_voice_client: The currently connected voice client
    :return: None
    """
    try:
        await connected_voice_client.disconnect()
    except discord.errors.ClientException:
        print("Cannot disconnect: The specified voice client is not connected or does not exist")


async def connect_vc(message):
    """
    Connects the bot voice client to the voice channel of the message's author
    :param message: The message sent including a command that would require the bot to join a voice channel
    :return: The newly joined voice client
    """
    try:
        channel = message.author.voice.channel
        return await channel.connect()
    except discord.errors.ClientException:
        await message.channel.send("I'm already connected to a channel!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(COMMAND_PREFIX): # If a user has entered a command
        command, args, data = parse_command_args(message)
        print("command: ", command, "args: ", args, "data: ", data)

        if command == "join":
            await connect_vc(message)

        if command == 'leave':
            voice_client = client.voice_clients[0]
            await disconnect_vc(voice_client)

        if command == 'play':
            voice_client = client.voice_clients[0]
            encoded_audio = discord.FFmpegOpusAudio("./audio_data/output.mp3")
            voice_client.play(encoded_audio)

        # Translation commands below

        if command == 'translate':
            native_text = args[3]

            print(native_text)
            print(supported_langs[lang][0:2])
            text = trans.translate(supported_langs[lang][0:2], native_text)
            trans.speak(supported_langs[lang], text, "female")

            voice_client = client.voice_clients[0]
            encoded_audio = discord.FFmpegOpusAudio( "./audio_data/temp/output.ogg" )
            voice_client.play(encoded_audio)
            while voice_client.is_playing():
                time.sleep(1)
            os.remove( "./audio_data/temp/output.ogg" )



client.run('ODM2ODAyNjAwMjg0MDYxNzA1.YIjTJg.NH1Y0Ki3Hxx82uQZH9Wv44yiVfI')
