from Translator import Translator
from Content import Content
from google.cloud import dialogflow

if __name__ == '__main__':
    trans = Translator()
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path("botlate", 123456)
    print(session)

    text_input = dialogflow.TextInput(text="Book a table for 5", language_code="en-US")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("Detected intent: ")
    print(response.query_result.intent.display_name)
    print(response.query_result.fulfillment_text)

    """

    text = trans.translate("es", "Doctor")
    print(trans.detected_lang)
    print(trans.name_to_code("Spanish"))

    an = "Medico"
    print(trans.translate("en", an))

    print(text)
    #trans.speak("es-ES", text, "female")

    #testing a quiz
    cont = Content(trans, "Spanish")
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
    """
