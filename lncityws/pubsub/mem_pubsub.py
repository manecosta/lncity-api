
from .pubsub import PubSub


class MemoryPubSub(PubSub):

    def __init__(self):
        self._subscribers_by_topic = {}

    def subscribe(self, topic, obj, method_name):
        self._subscribers_by_topic.setdefault(topic, []).append({
            'object': obj,
            'method_name': method_name
        })

    def publish(self, topic, obj):
        subscribers = self._subscribers_by_topic.get(topic, [])

        for subscriber in subscribers:
            o = subscriber.get('object')
            mn = subscriber.get('method_name')

            getattr(o, mn)(topic, obj)


mem_pubsub = MemoryPubSub()
