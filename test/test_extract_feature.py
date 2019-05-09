import spacy
import json
from unittest import TestCase


from qna.feature_extractor import extract_features


class TestExtractFeatures(TestCase):

    def test_extract_features(self):
        # sql_man = SqLiteManager()
        en_nlp_l = spacy.load("en_core_web_md")

        # result = sql_man.get_random_questions(3)
        # result = sql_man.get_questions_between(5, 7)
        qid = 5
        question = ("how a water pump works")
        question_type = " "

        en_doc = en_nlp_l(u'' + question)

        features = extract_features(question_type, en_doc, True)
        print("{0}){1} :\nExtracted: {2}".format(
            qid, question, features))
        # js_feat = json.dumps(features)
        # sql_man.update_feature(qid, js_feat)
        assert features is not None
        # sql_man.close_db()
