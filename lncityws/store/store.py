
class Store:

    def save_object(self, key, obj):
        raise NotImplemented

    def get_object(self, key, default=None):
        raise NotImplemented
