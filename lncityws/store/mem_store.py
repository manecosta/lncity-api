
from .store import Store


class MemoryStore(Store):

    def __init__(self):
        self._store = {}

    def saveObject(self, key, obj):
        self._store[key] = obj

    def getObject(self, key, default=None):
        return self._store.get(key, default=default)


mem_store = MemoryStore()
