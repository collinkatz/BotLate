import discord
from Translator import Translator
from Content import Content
import time
import os
import time

trans = Translator()
supported_langs = trans.speech_langs
client = discord.Client()
README = "TODO\n"

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

def list_quizes():
    """Returns a string of available quizzes"""
    s = ""
    s += "Usage: -bl quiz occupations\n"
    s += "1) Occupations\n"
    # Write this with real code
    return s


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

    if message.content.startswith('-bl list_quizzes'):
        try:
            channel = message.author.voice.channel
            voice_channel = await channel.connect()
        except discord.errors.ClientException:
            await message.channel.send(list_quizes())

    if message.content.startswith('-bl quiz'):
        """
        Allows the user to take a quiz. Needs to get the quiz name,
        then the id from a dict. Then, create a Content object, and then get
        the specific Quiz. Then, the bot should speak verbally the question
        and allow the user the type to answer. The Quiz object will tell if its
        correct and then the bot can relay that info. If the quiz is done, the score
        shoud be displayed.
        """
        command = message.content.lstrip("-bl quiz")
        command = command.strip(' ')

        translator = Translator()

        cont = Content(translator)
        cont.load_quizzes()

        quiz_dict = {}
        quiz_dict["occupations"] = 1
        id = None

        if command == '':
            await message.channel.send(README)
            #TODO: exit method here

        else:
            if message.lower() not in quiz_dict.keys():
                await message.channel.send("Invalid quiz name\n")
                #TODO: exit method here
            else:
                id = quiz_dict[command]
            quiz = cont.get_quiz(id)

            num_qs = quiz.num_qs()
            for i in range(num_qs):
                await message.channel.send(quiz.ask())
                answer = await client.wait_for("message", check=lambda message: message.author == client.user)
                was_correct, right_answer = quiz.answer(translator, answer)
                if was_correct:
                    await message.channel.send("You got that correct!")
                else:
                    await message.channel.send("Unfortunately, that answer was wrong.\n")

            final_score = quiz.percent()
            await message.channel.send("You got a " + str(final_score) + "%!\n")





    if message.content.startswith('-bl leave'):
        voice_client = client.voice_clients[0]
        await voice_client.disconnect()
        # Translation commands below

        if command == 'translate':
            native_text = args[3]
            print("hi")
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
