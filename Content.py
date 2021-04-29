from Translator import Translator

class Quiz():
    """
    A quiz is defined by a series of questions and correct answers (in English)
    """
    def __init__(self, name, id, questions, answers):
        self.name = name
        self.id = id
        #both questions and answers are arrays
        self.questions = questions
        self.answers = answers

        self.q_counter = 0
        self.done = False
        self.score = 0 #number of correct questions answered

    def ask(self):
        return self.questions[self.q_counter]

    def check_right(self, ans_text, real_ans):
        pass

    def answer(self, trans_object, ans_text):

        #TODO: Perform action to determine if answer is right
        right_answer = self.answers[self.q_counter]
        right = True

        if right:
            self.score += 1

        self.q_counter += 1
        if (self.q_counter >= len(self.questions)):
            self.done = True

        return right, right_answer


class Content():
    def __init__(self):
        self.quizzes = []
        self.scenarios = []
        self.load_quizzes()

    def load_quizzes(self):
        """Used to load quizzes"""
        #Quiz for Occupation
        qs = ["This person makes food at a restaurant.", "This person teaches at a univeristy."]
        ans = ["Chef", "Professor"]
        occ_quiz = Quiz("Occupation", 1, qs, ans)
        self.quizzes.append(occ_quiz)