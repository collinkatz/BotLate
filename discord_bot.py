import discord
from Translator import Translator
from Content import Content
import time
import os
import time

translator = Translator()
supported_langs = translator.speech_langs
client = discord.Client()
README = "TODO\n"

COMMAND_PREFIX = '-bl'
CONFIG = {"lang": "Spanish", "voice_mode": "female"}
COMMANDS = {COMMAND_PREFIX: 0, 'join': 0, 'leave': 0, 'play': 0, 'translate': 1, 'list_quizzes': 0, 'quiz': 1, 'help': 0, '?': 0} # A dictionary of commands and the number of arguments taken by each command

Content = Content(translator, CONFIG["lang"])


def parse_command_args(message):
    """
    This function separates out the command, arguments, and data from a user entered command
    :param message: The command message the user entered
    :return: command, A string: the command specified by the user,
    arg_list, A list of strings representing the arguments passed by the user based on the number of arguments in COMMANDS,
    data, A string: the data after the arguments passed by the user
    """
    args = str(message.content).strip().lower().split(" ")
    arg_list = []
    args.pop(0) # removes command prefix
    command = args.pop(0)  # second arg in args is always command
    num_args = COMMANDS[command]
    i = 0
    while i < num_args:
        arg_list.append(args.pop(i))
        i += 1
    data = ' '.join(args) # create data/sentence from leftover stuff in args
    print("command: ", command, "args: ", arg_list, "data: ", data)
    return command, arg_list, data


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

def list_quizes():
    """Returns a string of available quizzes"""
    s = ""
    s += "To take a quiz, do -bl quiz [Name of Quiz] example: -bl quiz occupations\n"
    s += "``` Quiz List:\n"
    s += "1) Occupations\n"
    s += "```"
    # Write this with real code
    return s


async def talk(text):
    """
    Outputs audio to the discord bot in the detected language of the input text
    :param text: A string, the message to say in any supported language
    :return: None
    """
    try:
        message_in_english = translator.translate("en", text)
        print(translator.detected_lang)
        detected_lang_code = ""
        for lang_code in supported_langs.values():
            if lang_code[0:2] == translator.detected_lang:
                detected_lang_code = lang_code
                break
        print(detected_lang_code)
        voice_client = client.voice_clients[0]
        translator.speak(detected_lang_code, text, CONFIG["voice_mode"])
        encoded_audio = discord.FFmpegOpusAudio("./audio_data/temp/output.ogg")
        voice_client.play(encoded_audio)
        while voice_client.is_playing():
            time.sleep(1)
        os.remove("./audio_data/temp/output.ogg")
    except IndexError:
        print("Voice client not connected, translating without audio")

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
        print("Bot already connected to a channel")
    except AttributeError:
        print("User not connected to a channel")


@client.event
async def on_message(message):

    async def say(message_to_say):
        await message.channel.send(message_to_say)

    if message.author == client.user:
        return

    if message.content.startswith(COMMAND_PREFIX): # If a user has entered a command
        command, args, data = parse_command_args(message)
        print("command: ", command, "args: ", args, "data: ", data)

        if command == "join":
            await connect_vc(message)

        elif command == 'leave':
            voice_client = client.voice_clients[0]
            await disconnect_vc(voice_client)

        elif command == 'play':
            voice_client = client.voice_clients[0]
            encoded_audio = discord.FFmpegOpusAudio("./audio_data/output.mp3")
            voice_client.play(encoded_audio)

        elif command == 'translate':
            lang = args[0]
            if lang not in supported_langs.keys():
                data = args.pop(0) + " " + data
                lang = CONFIG["lang"]
            text = translator.translate(supported_langs[lang][0:2], data)
            await say("Your message translated into " + lang + " is:\n```" + text + "```")
            try:
                voice_client = client.voice_clients[0]
                translator.speak(supported_langs[lang], text, CONFIG["voice_mode"])
                encoded_audio = discord.FFmpegOpusAudio( "./audio_data/temp/output.ogg" )
                voice_client.play(encoded_audio)
                while voice_client.is_playing():
                    time.sleep(1)
                os.remove("./audio_data/temp/output.ogg")
            except IndexError:
                print("Voice client not connected, translating without audio")

        # TODO: Command to output config
        # TODO: Command to update config
        elif command == 'help' or command == '?':
            file_object = open("./command_list.txt", "r")
            s = "List of possible commands:\n```"
            for line in file_object:
                s += line
            s += "```"
            await say(s)

        elif command == 'list_quizzes':
            await connect_vc(message)
            await say(list_quizes())

        elif command == 'quiz':
            """
            Allows the user to take a quiz. Needs to get the quiz name,
            then the id from a dict. Then, create a Content object, and then get
            the specific Quiz. Then, the bot should speak verbally the question
            and allow the user the type to answer. The Quiz object will tell if its
            correct and then the bot can relay that info. If the quiz is done, the score
            shoud be displayed.
            """

            quiz_dict = {}
            quiz_dict["occupations"] = 1
            id = None

            if args[0] not in quiz_dict.keys():
                await say("Sorry, I don't have that quiz :(\n")
                return
            else:
                id = quiz_dict[args[0]]
            quiz = Content.get_quiz(id)

            num_qs = quiz.num_qs()
            for i in range(num_qs):
                question = quiz.ask()
                await say(question)
                await talk(question)
                answer = await client.wait_for("message", timeout=60)
                was_correct, right_answer = quiz.answer(translator, answer.content)
                if was_correct:
                    await say("You got that correct!")
                else:
                    await say("Unfortunately, that answer was wrong.\n")

            final_score = quiz.percent()
            await say("You got a " + str(final_score) + "%!\n")
            quiz.reset()



client.run('ODM2ODAyNjAwMjg0MDYxNzA1.YIjTJg.QyT9gAK6eLW2WROE1b7fKea2qbw')
