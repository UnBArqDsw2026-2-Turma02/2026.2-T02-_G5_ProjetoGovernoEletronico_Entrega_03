from .observador import Observador


class Sujeito:
    def __init__(self) -> None:
        self._observadores: list[Observador] = []

    def adicionar(self, observador: Observador) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)

    def remover(self, observador: Observador) -> None:
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar(self) -> None:
        for observador in tuple(self._observadores):
            observador.atualizar()