import argparse
import sys
import logging
import spacy

from qna.question_classifier.qclassifier import classify_question
from qna.feature_extractor import extract_features
from qna.query_constructor import construct_query
from qna.find_answ.hadith_search import ElasticSearchOperate
from qna.search_rank import search_rank
from qna.candidate_answ import get_candidate_answers

_logger = logging.getLogger(__name__)
ess = ElasticSearchOperate()


class initQna:

    language = "en"

    question_in = None
    question_class = ""
    question_keywords = None
    query = None

    candidate_answers = None

    def __init__(self, en_nlp1, language):
        self.language = language
        self.nlp = en_nlp1

    def get_question_in(self, question):
        self.question_in = self.nlp(u'' + question)
        return self.question_in

    def process_question(self):
        self.question_class = classify_question(self.question_in)
        _logger.info("Question Class : {}".format(self.question_class))

        self.question_keywords = extract_features(
            self.question_class, self.question_in)
        _logger.info("Question Features : {}".format(self.question_keywords))

        self.query = construct_query(self.question_keywords, self.question_in)
        _logger.info("Query: {}".format(self.query))

    def process_answer(self):
        # self.answ = ess.search_answ(self.question_keywords)
        # _logger.info("answ:{}".format(self.answ))

        verse_number = search_rank(self.query)
        _logger.info("Verses retrieved: {}".format(len(verse_number)))
        # _logger.debug("Ranked pages: {}".format(ranked_wiki_docs))

        self.candidate_answers, keywords = get_candidate_answers(
            self.query, verse_number, self.nlp)
        _logger.info("Candidate answers ({}):\n{}".format(
            len(self.candidate_answers), '\n'.join(self.candidate_answers)))

        return " ".join(self.candidate_answers)


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(dest='question', type=str,
                        default='', metavar='"QUESTION"')

    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)

    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)

    return parser.parse_args(args)


def setup_logging(loglevel):

    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger('elasticsearch').setLevel(logging.CRITICAL)
    logging.getLogger('gensim').setLevel(logging.CRITICAL)


def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    en_nlp = spacy.load("en_core_web_md")
    if args.question is None:
        args.question = input("Input Question : ")

    qna = initQna(en_nlp1=en_nlp, language='en')
    qna.get_question_in(args.question)
    qna.process_question()
    answer = qna.process_answer()


def run():

    main(sys.argv[1:])


if __name__ == "__main__":
    run()
