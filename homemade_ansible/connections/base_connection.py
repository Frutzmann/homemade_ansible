from abc import ABC, abstractmethod


# Classe de base pour les connexions SSH
class BaseConnection(ABC):
    def __init__(self, params: dict):
        self.params = params

    @abstractmethod
    def connect(self, ip, port):
        pass
