import logging
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd

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
    connect_elasticsearch()
    logger.warning('Sending hadith dataframe into elasticsearch bulk API')
    hadith_df = pd.read_csv("hadith_retreiver/hadith.csv",
                            usecols=['Volume', 'Book', 'Number', 'Narrator', 'Verse'])
    print(hadith_df)
    es = connect_elasticsearch()
    res = es.index(index='hadith')
    print(res)
    # helpers.bulk(es_client, doc_generator(hadith_df))
