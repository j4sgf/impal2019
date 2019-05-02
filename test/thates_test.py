from unittest import TestCase
import os
import pandas
import sys


from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
# from scipy.sparse import csr_matrix

from qna.question_classifier.qclassifier import classify_question


class TestClassifyQuestion(TestCase):

    classification_score = 0.60

    def test_classify_question(self):
        training_data_path = 'test/qclasstraing.txt'
        df_question = pandas.read_csv(training_data_path, sep='|', header=0)
        df_question_train, df_question_test = train_test_split(
            df_question, test_size=0.2, random_state=42)

        predicted_class, clf, df_question_train_label, df_question_train = \
            classify_question(df_question_train=df_question_train,
                              df_question_test=df_question_test)

        scores = cross_val_score(
            clf, df_question_train, df_question_train_label)

        print("Accuracy: %0.2f (+/- %0.2f)" %
              (scores.mean(), scores.std() * 2))
        print("SD:", scores.std())

        assert scores.mean() > self.classification_score
