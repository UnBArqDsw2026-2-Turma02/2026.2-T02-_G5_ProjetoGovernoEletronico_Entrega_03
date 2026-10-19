from abc import abstractmethod
from typing import Protocol

from .observador import Observador


class Sujeito(Protocol):
    @abstractmethod
    def adicionar(self, observador: Observador) -> None:
        raise NotImplementedError("O sujeito concreto precisa implementar adicionar().")

    @abstractmethod
    def remover(self, observador: Observador) -> None:
        raise NotImplementedError("O sujeito concreto precisa implementar remover().")

    @abstractmethod
    def notificar(self) -> None:
        raise NotImplementedError("O sujeito concreto precisa implementar notificar().")
