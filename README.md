# BotLate
This discord bot translates a single english word to another language using wordreference-api and outputs the translated word to audio in the users channel.

Note: In order to run code, you need to put a Google Cloud Service .json credential file in the same directory and then update the name of the file in Translator.py. You also need FFmpeg in your PATH environment variable or the FFmpeg.exe binary in your bot's directory on Windows.

Run these commands inside the Python VM:
pip install google-cloud-translate==2.0.1
pip install --upgrade google-cloud-texttospeech
pip install --upgrade google-cloud-storage
pip install discord.py
