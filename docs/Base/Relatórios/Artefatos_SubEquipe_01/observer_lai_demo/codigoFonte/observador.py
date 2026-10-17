from abc import abstractmethod
from typing import Protocol


class Observador(Protocol):
    @abstractmethod
    def atualizar(self) -> None:
        raise NotImplementedError("O observador concreto precisa implementar atualizar().")
