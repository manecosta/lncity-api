
from typing import Union


class WSMessage:

    def __init__(self, identifier, action, body, parameters=None):
        self.identifier: str = identifier
        self.action: str = action
        self.body: Union[dict, list] = body
        self.parameters: dict = parameters

    def is_valid(self):
        return (
            self.identifier is not None and isinstance(self.identifier, str) and
            self.action is not None and isinstance(self.action, str) and
            self.body is not None and (isinstance(self.body, dict) or isinstance(self.body, list)) and
            (self.parameters is None or isinstance(self.parameters, dict))
        )

    def serializable(self):
        return {
            'identifier': self.identifier,
            'action': self.action,
            'body': self.body,
            'parameters': self.parameters
        }
