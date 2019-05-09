
"""
Created by felix on 24/3/18 at 10:26 PM
"""


class ElasticSearchDocument:

    _source = None

    def __init__(self, id, source, score=0):
        self._source = dict()
        self._source['id'] = id
        self._source['score'] = score
        self._source["Book"] = source["Book"]
        self._source["Narrator"] = source["Narrator"]
        self._source["Number"] = source["Number"]
        self._source["Verse"] = source["Verse"]
        self._source["Volume"] = source["Volume"]

    def get_book(self):
        return self._source["Book"]

    def get_verse_number(self):
        return self._source['verse_number']

    def get_narrator(self):
        return self._source["Narrator"]

    def get_number(self):
        return self._source["Number"]

    def get_verse(self):
        return self._source["Verse"]

    def get_volume(self):
        return self._source["Volume"]
