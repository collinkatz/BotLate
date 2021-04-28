from Translator import Translator

if __name__ == '__main__':
    trans = Translator()

    text = trans.translate("es", "it is time to eat")
    print(trans.detected_lang)
    print(trans.name_to_code("Spanish"))

    print(text)
    trans.speak("es-ES", text, "female")