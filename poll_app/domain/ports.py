from typing import Protocol


class Receiver(Protocol):
    def receive(self): ...


class CacheSetter(Protocol):
    def set(self, data): ...


class FacilityRepo(Protocol):
    def add(self, data): ...
