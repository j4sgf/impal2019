import spacy
import csv
import logging
import pandas
import sys
import os
from multiprocessing import Pool
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from scipy.sparse import csr_matrix

from qna.global_constant import CORPUS_DIR
from qna.corpus.constant import QUESTION_CLASSIFICATION_TRAINING_DATA, QUESTION_MODEL, QUESTION_CLASSIFICATION_RAW

logger = logging.getLogger(__name__)


def get_data_info(question_df):
    logger.debug("\n{0}".format(question_df.head()))
    logger.debug("\n{0}".format(question_df.info()))
    logger.debug("\n{0}".format(question_df.describe()))
    logger.debug("\n{0}".format(question_df.columns))


def pre_process(question_df):
    return pandas.get_dummies(question_df)


def remove_irrelevant_features(df_question):
    df_question_class = df_question.pop('Class')

    df_question.pop('Question')
    df_question.pop('WH-Bigram')

    return df_question_class


def support_vector_machine(df_question_train, df_question_class):
    lin_clf = LinearSVC()
    lin_clf.fit(df_question_train, df_question_class)
    logger.info("Linear SVC: {0}".format(lin_clf))

    return lin_clf


def save_classifier_model(df_question_train, df_question_class, model_type="linearSVC"):

    classifier_model = None
    training_model_path = os.path.join("trainer_model.pkl")

    if model_type == "linearSVC":
        classifier_model = support_vector_machine(
            df_question_train, df_question_class)
    else:
        logger.error("Undefined Classifier")

    if classifier_model is not None:
        joblib.dump(classifier_model, training_model_path)
        logger.info("Model saved at {0}".format(training_model_path))
    else:
        logger.error("Model empty")


def transform_data_matrix(df_question_train):

    # Generate Compressed Sparse Row matrix:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html
    logger.debug("Training data: {0}".format(df_question_train.shape))
    df_question_train = csr_matrix(df_question_train)

    return df_question_train


def train_qclassifier(training_data_path):
    df_question = pandas.read_csv(training_data_path, sep='|', header=0)
    get_data_info(df_question)

    df_question_class = remove_irrelevant_features(df_question)

    df_question_train = pre_process(df_question)

    df_question_train = transform_data_matrix(df_question_train)

    save_classifier_model(df_question_train, df_question_class)


def read_input_file(raw_data, training_data_path, en_nlp):

    with open(training_data_path, 'a', newline='') as csv_fp:
        csv_fp_writer = csv.writer(csv_fp, delimiter='|')
        for row in raw_data:
            list_row = row.split(" ")
            question_class_list = list_row[0].split(":")
            question = " ".join(list_row[1:len(list_row)])
            question = question.strip("\n")
            question_class = question_class_list[0]

            process_question(question, question_class, en_nlp, csv_fp_writer)

    csv_fp.close()


def clean_old_data(training_data_path):

    question_features = ['Question', 'WH', 'WH-Bigram',
                         'WH-POS', 'WH-NBOR-POS', 'Root-POS', 'Class']

    with open(training_data_path, 'w', newline='') as csv_fp:
        csv_fp_writer = csv.writer(csv_fp, delimiter='|')
        csv_fp_writer.writerow(question_features)
        csv_fp.close()


def process_question(question, qclass, en_nlp, csv_fp_writer):
    en_doc = en_nlp(u"" + question)
    print(en_doc)
    sent_list = list(en_doc.sents)
    sent = sent_list[0]
    wh_bi_gram = []
    root_token = ""
    wh_pos = ""
    wh_nbor_pos = ""
    wh_word = ""
    for token in sent:
        if token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
            wh_pos = token.tag_
            wh_word = token.text
            wh_bi_gram.append(token.text)
            wh_bi_gram.append(str(en_doc[token.i + 1]))
            wh_nbor_pos = en_doc[token.i + 1].tag_
        if token.dep_ == "ROOT":
            root_token = token.tag_

    if wh_word != "" and " ".join(wh_bi_gram) != "" and wh_pos != "" and wh_nbor_pos != "":
        csv_fp_writer.writerow([question, wh_word, " ".join(
            wh_bi_gram), wh_pos, wh_nbor_pos, root_token, qclass])
    else:
        logger.error("Extraction failed: {0}:{1}".format(
            question, qclass))


def extract_training_features(raw_data_path, training_data_path, en_nlp):
    with open(raw_data_path, 'r') as fp:
        read_input_file(fp, training_data_path, en_nlp)
        fp.close()
        logger.info("Extracted features from raw data.")
        logger.info("Excluded data where features failed to extract.")


if __name__ == "__main__":

    from time import time

    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        start_time = time()

        should_extract = sys.argv[1]

        training_path = os.path.join(
            CORPUS_DIR, QUESTION_CLASSIFICATION_TRAINING_DATA)
        raw_path = os.path.join(CORPUS_DIR, QUESTION_CLASSIFICATION_RAW)

        if should_extract:
            logger.info("Cleaning enabled.")
            clean_old_data(training_path)
            en_nlp = spacy.load("en_core_web_md")

            extract_training_features(raw_path, training_path, en_nlp)

        train_qclassifier(training_path)

        end_time = time()
        logger.info("Total training time : {0}".format(end_time - start_time))
    else:
        raise ValueError(
            'Missing option to enable to disable feature extraction')
