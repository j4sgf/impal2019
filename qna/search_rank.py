import logging
from qna.find_answ.hadith_search import ElasticSearchOperate

"""
Created by felix on 25/3/18 at 5:19 PM
"""

logger = logging.getLogger(__name__)


def search_rank(query):
    es = ElasticSearchOperate()
    result_all = es.search_answ(query)
    logging.debug("Ranked Verses Number: {0}".format(
        [result.get_number() for result in result_all]))
    return result_all


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    # mquery = list([[['Cushman', 'known', 'Wakefield', 'are'], [['Cushman', 'Wakefield'], 'or'], [], []]])
    mquery = list([[['Albert', 'Einstein', 'birth'], [], [], []]])

    les = ElasticSearchOperate()
    res_all = les.search_answ(mquery)
    for res in res_all:
        print(res.get_number())
