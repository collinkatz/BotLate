import os
import six
from google.cloud import translate_v2 as translate

class Translator:
    def __init__(self):
        """
        Initialize the translator object. Load in the accepted languages. Make sure key is valid.
        :param key: the Google Project API Key
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'botlate-b3e46cfde885.json'
        self.detected_lang = "" #stores the detected language

        #Create a dictionary of language_code -> name
        self.lang_dict = {} #code -> name
        self.lang_dict_rev = {} #name -> code
        translate_client = translate.Client()
        all_langs = translate_client.get_languages()
        for pair in all_langs:
            self.lang_dict[pair["language"]] = pair["name"]
            self.lang_dict_rev[pair["name"]] = pair["language"]


    def translate(self, target_lang, text):
        """
        Translates the text to the target language
        :param origin_lang: the orign language (from detect_language)
        :param text: text to translate
        :return: the text in English
        """

        translate_client = translate.Client()

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(text, target_language=target_lang)

        #print(u"Text: {}".format(result["input"]))
        #print(u"Translation: {}".format(result["translatedText"]))
        #print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

        self.detected_lang = result["detectedSourceLanguage"]
        return result["translatedText"]

    def name_to_code(self, name):
        #TODO: Add ability to find closest match
        for n in self.lang_dict_rev.keys():
            if n == name or (name in n):
                return self.lang_dict_rev[n]




    #May need to add methods for plaintext_language_to_api, preprocess_text
