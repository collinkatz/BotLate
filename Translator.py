import os
import six
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech

def supported_speech_langs():
    """
    :return: dict of supported speech languages language->code
    """
    ret = {}
    langs = ["Arabic", "Bengali", "Chinese", "Danish", "Dutch", "English", "French", "German", "Hindi", "Italian", "Japenese", "Korean", "Russian", "Spanish", "Telugu"]
    codes = ["af-ZA", "bn-IN", "yue-HK", "da-DK", "nl-NH", "en-US", "fr-FR", "de-DE", "hi-IN", "it-IT", "ja-JP", "ko-KR", "ru-RU", "es-ES", "ta-IN"]
    for i, lang in enumerate(langs):
        ret[lang] = codes[i]
    return ret

class Translator:
    def __init__(self):
        """
        Initialize the translator object. Load in the accepted languages. Make sure key is valid.
        :param key: the Google Project API Key
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'botlate-b3e46cfde885.json'
        self.detected_lang = "" #stores the detected language
        self.translate_client = translate.Client()
        self.speech_client = texttospeech.TextToSpeechClient()

        #Different genders for voice
        self.male = texttospeech.SsmlVoiceGender.MALE
        self.female = texttospeech.SsmlVoiceGender.FEMALE
        self.neutral = texttospeech.SsmlVoiceGender.NEUTRAL

        #Create a dictionary of language_code -> name
        self.lang_dict = {} #code -> name
        self.lang_dict_rev = {} #name -> code
        translate_client = translate.Client()
        all_langs = translate_client.get_languages()
        for pair in all_langs:
            self.lang_dict[pair["language"]] = pair["name"]
            self.lang_dict_rev[pair["name"]] = pair["language"]

        self.speech_langs = supported_speech_langs()


    def translate(self, target_lang, text):
        """
        Translates the text to the target language
        :param target_lang: the language to tranlate into
        :param text: text to translate
        :return: the text in the target language (en for English)
        """

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = self.translate_client.translate(text, target_language=target_lang)

        #print(u"Text: {}".format(result["input"]))
        #print(u"Translation: {}".format(result["translatedText"]))
        #print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

        self.detected_lang = result["detectedSourceLanguage"]
        return result["translatedText"]

    def speak(self, language, text, gender="neutral"):
        """
        Generates a .mp3 audio file based on the input language code
        (ex. en-US) and text (ex. I love coding).
        :param language: google text-to-speech language code (differnet from translate API)
        :param text: the raw text to speak
        :param gender: neutral, male, or female
        :return: None
        """
        voice_input = texttospeech.SynthesisInput(text=text)

        if language not in self.speech_langs.values():
            raise ValueError("Language not supported by Speech API")

        #voice settings
        if (gender.lower() == "female"):
            voice = texttospeech.VoiceSelectionParams(language_code=language, ssml_gender=self.female)
        elif (gender.lower() == "male"):
            voice = texttospeech.VoiceSelectionParams(language_code=language, ssml_gender=self.male)
        else:
            voice = texttospeech.VoiceSelectionParams(language_code=language, ssml_gender=self.neutral)

        #MP3 encoding, need to test if .WAV will work
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        #PERFORM MAGIC
        response = self.speech_client.synthesize_speech(input=voice_input, voice=voice, audio_config=audio_config)

        #TODO: see if this binary data can be directly passed to discord bot
        #for now, write a .mp3 file
        with open("audio_data/output.mp3", "wb", 0) as out:
            out.write(response.audio_content)


    def name_to_code(self, name):
        #TODO: Add ability to find closest match
        for n in self.lang_dict_rev.keys():
            if n == name or (name in n):
                return self.lang_dict_rev[n]




    #May need to add methods for plaintext_language_to_api, preprocess_text
