import spacy
import csv
import logging

logger = logging.getLogger(__name__)
qtrain = open('qtrain.txt', "r")
trainres = 'qclasstraing.txt'
en_nlp = spacy.load("en_core_web_md")


def read_input_file(raw_data, training_data, en_nlp):

    with open(training_data, 'a', newline='') as csv_fp:
        csv_fp_writer = csv.writer(csv_fp, delimiter='|')
        for row in raw_data:
            list_row = row.split(" ")
            question_class_list = list_row[0].split(":")
            question = " ".join(list_row[1:len(list_row)])
            question = question.strip("\n")
            question_class = question_class_list[0]

            process_question(question, question_class, en_nlp, csv_fp_writer)

    csv_fp.close()


# clean_old_data()


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


read_input_file(qtrain, trainres, en_nlp)
