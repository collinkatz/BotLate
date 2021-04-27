import os
import six
from google.cloud import translate_v2 as translate

class Translator:
    def __init__(self):
        """
        Initialize the translator object. Make sure key is valid.
        :param key: the Google Project API Key
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'botlate-b3e46cfde885.json'
        self.detected_lang = "" #stores the detected language

    def translate(self, origin_lang, text):
        """
        Translates the text to English
        :param origin_lang: the orign language (from detect_language)
        :param text: text to translate
        :return: the text in English
        """

        translate_client = translate.Client()

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(text, target_language=origin_lang)

        #print(u"Text: {}".format(result["input"]))
        #print(u"Translation: {}".format(result["translatedText"]))
        #print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

        self.detected_lang = result["detectedSourceLanguage"]
        return result["translatedText"]




    #May need to add methods for plaintext_language_to_api, preprocess_text
