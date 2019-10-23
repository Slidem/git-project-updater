from abc import ABC, abstractmethod

class ProjectProcessorLink(ABC):

    def __init__(self):
        self.next = None

    @abstractmethod
    def process(self, projects):
        pass

    def add_next(self, link):
        self.next = link
        return self.next
