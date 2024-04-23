from abc import ABC, abstractmethod


class BaseModule(ABC):
    name: str = "anonymous"

    def __init__(self, params: dict):
        self.params = params

    @abstractmethod
    def process(self, ssh_client, task_counter):
        pass
