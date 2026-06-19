"""Estado atual das torres e dos discos."""


class GameState:
    """Guarda a posicao dos discos nas tres hastes."""

    def __init__(self, total_discos=3):
        self.total_discos = total_discos
        self.reset()

    def reset(self):
        self.torres = {
            "A": list(range(self.total_discos, 0, -1)),
            "B": [],
            "C": [],
        }

    def top_disk(self, torre):
        discos = self.torres[torre]
        return discos[-1] if discos else None

    def is_complete(self):
        return len(self.torres["C"]) == self.total_discos

    def snapshot(self):
        return {nome: discos.copy() for nome, discos in self.torres.items()}
