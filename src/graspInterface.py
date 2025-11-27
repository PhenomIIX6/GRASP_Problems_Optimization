from abc import ABC, abstractmethod

class IMakeRCL():
    @abstractmethod
    def construction(self):
        pass

class ILocalSearch():
    @abstractmethod
    def local_search(self):
        pass

class ISolution():
    @abstractmethod
    def btt(self):
        pass

class ILog():
    @abstractmethod
    def log(self, iter, candidate, solution):
        pass