from flask import url_for, jsonify
from functools import lru_cache
from app import db


class Pagination(object):
    def __init__(self, endpoint, *args, **kwargs):
        items = self._get_pages(endpoint)
        self.page = int(kwargs.get("page", 0))
        self.page_size = int(kwargs.get("page_size", 10))
        self.total_items = len(items)
        self.total_pages = (len(items) - 1) // self.page_size + 1
        self.start = kwargs.get("start", None)
        if not self.start:
            offset = self.page * self.page_size
            self.start = items[offset]
    def __call__(self):
        return self

    @lru_cache()
    def _get_pages(self, endpoint):
        # Firebase returns unordered resultset
        return sorted(list(db.child(endpoint).shallow().get().val()))


class ResultSet(object):
    def __init__(self, resources, pagination, lastKey=None, *args, **kwargs):
        self.resources = resources
        self.pagination = pagination
        self.lastKey = lastKey

    def response(self):
        pagination = self.pagination
        data = {
            "items": self.resources,
            "_meta": {
                "page": pagination.page,
                "page_size": pagination.page_size,
                "total_items": pagination.total_items,
                "total_pages": pagination.total_pages,
            },
            "_next": self.lastKey,
        }
        return jsonify(data)


