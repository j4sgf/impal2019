from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError as ESConnectionError
from urllib3.exceptions import NewConnectionError
import logging
import sys

_logger = logging.getLogger(__name__)


class ElasticSearchMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                ElasticSearchMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ElasticSearchConn(metaclass=ElasticSearchMeta):
    __hostname__ = 'localhost'
    __port__ = 9200
    __es_conn__ = None
    es_index_config = None

    def __init__(self):
        es_host = {'host': self.__hostname__, 'port': self.__port__}
        self.__es_conn__ = Elasticsearch(hosts=[es_host])
        self.set_up_index()

    @staticmethod
    def get_index_mapping():
        return {
            "settings": {
                "number_of_shards": 5,
                "number_of_replicas": 1,
                "analysis": {
                    "filter": {
                        "english_stop": {
                            "type": "stop",
                            "stopwords": "_english_"
                        },
                        "english_porter2": {
                            "type": "stemmer",
                            "language": "porter2"
                        }
                    },
                    "analyzer": {
                        "cust_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": [
                                "lowercase",
                                "english_stop",
                                "english_porter2"
                            ]
                        }
                    }
                },
            },
            "mappings": {
                "_doc": {
                    "_meta": {
                        "version": 2
                    },
                    "properties": {
                        "Book": {
                            "type": "long"

                        },
                        "Narrator": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "Number": {
                            "type": "long"

                        },
                        "Verse": {
                            "type": "text",
                            "analyzer": "cust_analyzer",
                            "fields": {
                                "keyword": {
                                    "type": "keyword",
                                    "ignore_above": 256
                                }
                            }
                        },
                        "Volume": {
                            "type": "long"

                        }
                    }
                }
            }
        }

    def create_index(self):
        # ignore 400 cause by IndexAlreadyExistsException when creating an index
        self.es_index_config = ElasticSearchConn.get_index_mapping()
        res = self.__es_conn__.indices.create(
            index='hadith', body=self.es_index_config, ignore=400)
        if 'error' in res and res['status'] == 400:
            # NOTE: Illegal argument errors are also being masked here, so test the index creation
            error_type = res['error']['root_cause'][0]['type']
            if error_type == 'resource_already_exists_exception':
                _logger.debug("Index already exists")
            else:
                _logger.error(
                    "Error Occurred in Index creation:{0}".format(res))
                print("\n -- Unable to create Index:" + error_type + "--\n")
                sys.exit(1)
        elif res['acknowledged'] and res['index'] == "hadith":
            _logger.debug("Index Created")
        else:
            _logger.error("Index creation failed:{0}".format(res))
            print("\n -- Unable to create Index--\n")
            sys.exit(1)

    def set_up_index(self):
        try:
            try:
                try:
                    index_exists = self.__es_conn__.indices.exists(
                        index='hadith')
                    if not index_exists:
                        self.create_index()
                    # else:
                    #     res = self.__es_conn__.indices.get_mapping(index='hadith', doc_type='_doc')
                    #     try:
                    #         current_version = res['hadith']['mappings']['_doc']['_meta']['version']
                    #         if current_version < __index_version__:
                    #             self.update_index(current_version)
                    #         elif current_version is None:
                    #             _logger.error("Old Index Mapping. Manually reindex the index to persist your data.")
                    #             print("\n -- Old Index Mapping. Manually reindex the index to persist your data.--\n")
                    #             sys.exit(1)
                    #     except KeyError:
                    #         logger.error("Old Index Mapping. Manually reindex the index to persist your data.")
                    #         print("\n -- Old Index Mapping. Manually reindex the index to persist your data.--\n")
                    #         sys.exit(1)

                except ESConnectionError as e:
                    _logger.error(
                        "Elasitcsearch is not installed or its service is not running. {0}".format(e))
                    print(
                        "\n -- Elasitcsearch is not installed or its service is not running.--\n", e)
                    sys.exit(1)
            except NewConnectionError:
                pass
        except ConnectionRefusedError:
            pass


if __name__ == "__main__":
    es = ElasticSearchConn()
