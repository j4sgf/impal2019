import logging
import pandas as pd
import os

from elasticsearch import Elasticsearch
from elasticsearch import helpers

from qna.global_constant import CORPUS_DIR
from qna.corpus.constant import HADITH_CLEAN
from qna.es_conn import ElasticSearchConn

es_client = Elasticsearch(http_compress=True)


def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def filterKeys(document):
    return {key: document[key] for key in columns}


def doc_generator(df):
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield {
            "_index": 'hadith',
            "_type": "_doc",
            "_source": filterKeys(document),
        }
    raise StopIteration


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.ERROR)
    columns = ["Volume", "Book", "Number",
               "Narrator", "Verse"]
    # connect_elasticsearch()
    logger.warning('Sending hadith dataframe into elasticsearch bulk API')
    hadith_clean = os.path.join(CORPUS_DIR, HADITH_CLEAN)
    hadith_df = pd.read_csv(hadith_clean,
                            usecols=['Volume', 'Book', 'Number', 'Narrator', 'Verse'])
    # print(hadith_df)
    es = ElasticSearchConn()
    connect_elasticsearch()
    helpers.bulk(es_client, doc_generator(hadith_df))
