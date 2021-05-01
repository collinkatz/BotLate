from Translator import Translator

class Question:
    """
    Represents one question with multiple answers
    """
    def __init__(self, question):
        self.question = question
        self.ans = []

    def set_ans(self, answers):
        for ans in answers:
            self.ans.append(ans)

    def check_correct(self, translation_obj: Translator, user_ans, expected_lang):
        """user answer maybe in any language"""
        #first, convert user answer to english
        user_in_engl = translation_obj.translate("en", user_ans)
        print(user_in_engl)
        # check if the language is the same as expected
        print(translation_obj.detected_lang)
        if translation_obj.detected_lang != expected_lang:
            return False

        for ans in self.ans:
            if ans.upper() == user_in_engl.upper():
                return True
        return False

class Quiz():
    """
    A quiz is defined by a series of questions and correct answers (in English). This is
    only for text quizzes.
    """
    def __init__(self, name, id, questions, target_language):
        self.name = name
        self.id = id
        self.questions = questions #array of question objects
        self.target_language = target_language
        self.translation_obj = None #set by Content()

        self.q_counter = 0
        self.done = False
        self.score = 0 #number of correct questions answered

    def ask(self):
        """
        Asks a question, and must call answer() after
        :return: The question as a string in English
        """
        return self.questions[self.q_counter].question

    def check_right(self, ans_text):
        """
        Determines if a given answer matches the real answer by
        calling the question's check_correct method
        :param ans_text: the user-inputted answer
        :param real_ans: the real, correct answer encoded
        :return: boolean
        """
        return self.questions[self.q_counter].check_correct(self.translation_obj, ans_text, self.target_language)

    def answer(self, trans_object, ans_text):
        """
        Increments the score if correct and always increments the
        question counter.
        :param trans_object: A Translator object found in Translator.py
        :param ans_text: The text that the user returns
        :return: boolean of if it was correct and the correct answer
        """

        #Perform action to determine if answer is right
        right_answers = self.questions[self.q_counter].ans
        right = self.check_right(ans_text)

        if right:
            self.score += 1

        self.q_counter += 1
        if (self.q_counter >= len(self.questions)):
            self.done = True

        return right, right_answers

    def reset(self):
        self.q_counter = 0
        self.score = 0

    def percent(self):
        """
        :return: current percentage out of 100
        """
        return (self.score / len(self.questions)) * 100

    def num_qs(self):
        return len(self.questions)


class Content:
    def __init__(self, translation_obj: Translator, language):
        self.translation_obj = translation_obj
        self.quizzes = []
        self.scenarios = []
        self.language = language #full name eg. Spanish"
        self.load_quizzes()

    def load_quizzes(self):
        """Used to load quizzes"""
        #Quiz for Occupation
        occ_quiz = self.load_occupation_quiz(self.language)
        self.quizzes.append(occ_quiz)

    def load_occupation_quiz(self, target_lang):
        q1 = Question("This person plays roles in a movie.")
        q1.set_ans(["Actor", "Actress", "The actor"])

        q2 = Question("This person plans out buildings")
        q2.set_ans(["Architect", "The Architect"])

        q3 = Question("This person is in charge of planning out a building")

        qs = [q1, q2]

        #Get languge code

        occ_quiz = Quiz("Occupation", 1, qs, self.translation_obj.lang_dict_rev[target_lang])
        occ_quiz.translation_obj = self.translation_obj

        return occ_quiz


    def get_quiz(self, quiz_id):
        for quiz in self.quizzes:
            if quiz.id == quiz_id:
                return quiz
        return -1
