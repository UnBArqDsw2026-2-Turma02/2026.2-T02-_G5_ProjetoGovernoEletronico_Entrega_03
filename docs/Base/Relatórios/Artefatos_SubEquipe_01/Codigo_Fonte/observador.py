from typing import Protocol


class Observador(Protocol):
    def atualizar(self) -> None:
        raise NotImplementedError(
            "O observador deve implementar atualizar()."
        )