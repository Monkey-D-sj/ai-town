from abc import abstractmethod, ABC


class BaseStore(ABC):
    
    @abstractmethod
    def connect(self): ...

    @abstractmethod
    def disconnect(self): ...
