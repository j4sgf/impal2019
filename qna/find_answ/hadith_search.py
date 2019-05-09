import logging
from elasticsearch import Elasticsearch


from qna.es_conn import ElasticSearchConn
from qna.container.query_container import QueryContainer
from qna.container.es_doc import ElasticSearchDocument

_logger = logging.getLogger(__name__)


def resolve_operator(conj_op):
    if conj_op == "and":
        return "and"
    elif conj_op == "or":
        return "or"


class ElasticSearchOperate:
    es_conn = None

    def __init__(self):
        self.es = ElasticSearchConn
        self._es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def search_answ(self, search_query):
        search_res = []

        for query in search_query:
            if not isinstance(query, QueryContainer):
                query_cont = QueryContainer(query)
            else:
                query_cont = query
            if isinstance(query_cont, QueryContainer):
                features = query_cont.get_features()
                conjunctions = query_cont.get_conjunctions()
                negations = query_cont.get_negations()
                markers = query_cont.get_markers()

                must_match = []
                should_match = []
                must_not_match = []

                if conjunctions is not None and len(conjunctions) > 0:
                    for index, conj in enumerate(conjunctions):
                        if isinstance(conj, list):
                            features = [
                                feat for feat in features if feat not in conj]
                            if index < len(conjunctions) - 1:
                                conj_op = conjunctions[index + 1]
                                es_operator = resolve_operator(conj_op)
                                must_match_query = {
                                    "multi_match": {"query": " ".join(conj), "operator": es_operator, "fields": "Verse"}}
                                must_match.append(must_match_query)

                if negations is not None and len(negations) > 0:
                    for index, negate in enumerate(negations):
                        if isinstance(negate, list):
                            features = [
                                feat for feat in features if feat not in negate]
                            if index < len(negations) - 1:
                                conj_op = negations[index + 1]
                                es_operator = resolve_operator(conj_op)
                                must_not_match_term = {
                                    "multi_match": {
                                        "query": " ".join(negations[index]),
                                        "operator": es_operator,

                                        "fields": "Verse"
                                    }
                                }
                                must_not_match.append(must_not_match_term)

                if features is not None and len(features) > 0:
                    # must_match_query = {"terms": {__wiki_content__: features}}
                    # must_match.append(must_match_query)
                    # for feat in features:
                    #     must_match_term = {"term": {__wiki_content__: feat}}
                    #     must_match.append(must_match_term)
                    must_match_query = {
                        "multi_match": {
                            "query": " ".join(features),

                            "fields": "Verse"
                        }
                    }
                    must_match.append(must_match_query)

                search_body = {
                    "query": {
                        "bool": {
                            "must": must_match,
                            "should": should_match,
                            "must_not": must_not_match,
                        }
                    }
                }

                # _logger.debug(search_body)

                es_result = self._es.search(
                    index="hadith", doc_type="_doc", body=search_body)
                if es_result['hits']['hits'] is not None:
                    es_result_hits = es_result['hits']['hits']
                    for result in es_result_hits:
                        article_id = result['_id']
                        article_score = result['_score']
                        article_source = result['_source']
                        es_document = ElasticSearchDocument(
                            article_id, article_source, article_score)
                        search_res.append(es_document)

            else:
                raise ValueError("Incorrect Query Type")

        return search_res


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    # mquery = list([[['Cushman', 'known', 'Wakefield', 'are'], [['Cushman', 'Wakefield'], 'or'], [], []]])
    mquery = list([[['Emigrated', 'deeds', 'marry'], [], [], []]])

    es = ElasticSearchOperate()
    res_all = es.search_answ(mquery)
    # for lres in res_all:
    # print(lres.get_wiki_title())
