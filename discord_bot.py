import discord
from Translator import Translator
from Content import Content
import time


client = discord.Client()
README = "TODO\n"


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

        else:
            if message.lower() not in quiz_dict.keys():
                await message.channel.send("Invalid quiz name\n")
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


client.run('ODM2ODAyNjAwMjg0MDYxNzA1.YIjTJg.NH1Y0Ki3Hxx82uQZH9Wv44yiVfI')
