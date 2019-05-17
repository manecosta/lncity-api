
class PubSub:

    def subscribe(self, topic, obj, method_name):
        raise NotImplemented

    def publish(self, topic, obj):
        raise NotImplemented
