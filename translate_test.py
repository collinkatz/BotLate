from Translator import Translator
from Content import Content

if __name__ == '__main__':
    trans = Translator()

    text = trans.translate("es", "Doctor")
    print(trans.detected_lang)
    print(trans.name_to_code("Spanish"))

    an = "Medico"
    print(trans.translate("en", an))

    print(text)
    #trans.speak("es-ES", text, "female")

    #testing a quiz
    cont = Content(trans)
    cont.load_quizzes()
    occ_quiz = cont.get_quiz(1)

    print(occ_quiz.ask())
    ans = input("Answer the question: ")
    right, real_ans = occ_quiz.answer(trans, ans)
    print(right)
    print(real_ans)

    print(occ_quiz.ask())
    ans = input("Answer the question: ")
    right, real_ans = occ_quiz.answer(trans, ans)
    print(right)
    print(real_ans)

    print("Res: ")
    print(occ_quiz.percent())
    occ_quiz.reset()