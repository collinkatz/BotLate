import json
from Translator import Translator, supported_speech_langs
from google.cloud import dialogflow

#Config for the bot that was made in DialogFlow
project_id = "botlate"
session_id = 123456
language_code = "en-US"

class ConvoElement:
    """
    every conversastion is made up of a prompt, and then
    and expected response that is defined on DialogFlow

    There also should be a hint and a response, with optionally
    pos/neg split in order to have different repsonses for pos/neg
    sentiment
    """
    def __init__(self, prompt, hint, response=None, pos_res=None, neg_res=None):
        self.prompt = prompt
        self.hint = hint
        self.response = response

        self.pos_res = pos_res
        self.neg_res = neg_res
        self.sentiment = False
        if pos_res and neg_res:
            self.sentiment = True

        self.intent = None #intent from the DialogFlow website

    def process_answer(self, bot_txt):
        """returns a text response once english
        text is passed in. It is guranteed to be the correct response"""
        if self.sentiment:
            pass
            #TODO: get reponse from sentiment
        return bot_txt

    def get_hint(self):
        return self.hint



class Conversation:
    """
    This is a class representing an example conversastion.
    It has an end goal (ex. order food) and is able to guide
    the user through the conversation with hints.

    It takes in a language name (ex. Spanish)

    This works by using the Google DialogFlow website to
    create the bot to flexibly respond to a variety of inputs
    """
    def __init__(self, trans_obj: Translator, lang):
        self.lang = lang
        self.lang_to_code = supported_speech_langs()
        self.situation = "You are walking down the street during the last day of summer break before school \
                         starts again in the summer. You decide to go to a small food place around the corner.\
                         Your goal is to get through this meal and the conversation. \n"

        self.session_client = dialogflow.SessionsClient() #for the convo bot
        self.session = self.session_client.session_path("botlate", 123456)

        #TODO: sentiment client
        self.trans_obj = trans_obj
        self.elem_counter = 0
        self.convo_elems = self.load_convo_elems()



    def send_to_bot(self, txt):
        #sends to bot and returns intent, response
        text_input = dialogflow.TextInput(text=txt, language_code=self.lang_to_code[self.lang])
        query_input = dialogflow.QueryInput(text=text_input)

        response = self.session_client.detect_intent(
            request={"session": self.session, "query_input": query_input}
        )

        return response.query_result.intent.display_name, response.query_result.fulfillment_text


    def load_convo_elems(self):
        #Load the convo elems in order for a resturant

        ask_for_table = ConvoElement("Hello, Welcome to our food establishment. Would you like a table and how many guests do you have?\n"\
                                     , "Tell the waiter the number of guests\n")
        ask_for_table.intent = "bot.askfortable"

        fav_season = ConvoElement("Friend: Woah! This summer weather is perfect. Summer is my favorite season. What is yours?\n", "Tell your friend your favorite season\n")
        fav_season.intent = "bot.fav_season"

        classes = ConvoElement("Friend: School is starting soon (sighs). How many classes are you taking?\n", "Tell your friend the number of classes you're taking\n")
        classes.intent = "bot.classes"

        major = ConvoElement("Friend: Also, I still need to decide my major. What major are you?\n", "Tell your friend what major you are in\n")
        major.intent = "bot.major"

        bill = ConvoElement("You have finished your meal and are getting ready to leave. The waiter is nearby and so now you should ask for a bill\n", "Ask if you can see the bill\n")
        bill.intent = "bot.ask_for_bill"

        ret = [ask_for_table, fav_season, classes, major, bill]

        return ret

    def ask(self):
        #return prompt, hint
        prompt = self.convo_elems[self.elem_counter].prompt
        hint = self.convo_elems[self.elem_counter].get_hint()

        new_prompt = self.trans_obj.translate(self.trans_obj.lang_dict_rev[self.lang], prompt)
        new_hint = self.trans_obj.translate(self.trans_obj.lang_dict_rev[self.lang], hint)

        return new_prompt, new_hint

    def answer(self, user_in):
        #increment counter and return a text
        #check if the expected bot intent is correct
        intent, bot_res = self.send_to_bot(user_in)

        if intent == self.convo_elems[self.elem_counter].intent:
            ret = self.convo_elems[self.elem_counter].process_answer(bot_res)
            self.elem_counter += 1
            return self.trans_obj.translate(self.trans_obj.lang_dict_rev[self.lang], ret)
        else:
            ret = "Not quite what we were looking for"
            self.elem_counter += 1
            return self.trans_obj.translate(self.trans_obj.lang_dict_rev[self.lang], ret)

    def is_done(self):
        return self.elem_counter > len(self.convo_elems) - 1





