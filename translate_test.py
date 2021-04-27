from Translator import Translator

if __name__ == '__main__':
    trans = Translator()

    print(trans.translate("ja", "es hora de comer"))
    print(trans.detected_lang)

    print(trans.lang_dict)
    print(trans.name_to_code("Japanese"))