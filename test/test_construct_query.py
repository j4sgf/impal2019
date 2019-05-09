import spacy
import json
from unittest import TestCase


from qna.query_constructor import construct_query


class TestConstructQuery(TestCase):

    def test_construct_query(self):
        # sql_man = SqLiteManager()
        en_nlp_l = spacy.load("en_core_web_md")

        # result = sql_man.get_random_questions(3)
        # result = sql_man.get_questions_between(5, 7)

        qid = 5
        question = ("how a water pump works")
        question_type = " "
        question_feat = ["water pump", "work"]

        if question_feat is not None:

            en_doc = en_nlp_l(u'' + question)

            query = construct_query(question_feat, en_doc)
            print("{0}){1} :\nQuery: {2}".format(
                qid, question, repr(query)))
            js_query = json.dumps(repr(query))
            # sql_man.update_search_query(qid, js_query)
            assert query is not None
        # sql_man.close_db()
