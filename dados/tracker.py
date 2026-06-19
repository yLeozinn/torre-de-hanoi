"""Cronometro e contador de movimentos da partida."""

import time


class GameTracker:
    def __init__(self, total_discos):
        self.total_discos = total_discos
        self.reset()

    def reset(self):
        self.iniciado_em = time.time()
        self.finalizado_em = None
        self.movimentos = 0

    def register_move(self):
        self.movimentos += 1

    def finish(self):
        if self.finalizado_em is None:
            self.finalizado_em = time.time()

    def elapsed_seconds(self):
        fim = self.finalizado_em or time.time()
        return int(fim - self.iniciado_em)

    def optimal_moves(self):
        return (2 ** self.total_discos) - 1

    def summary(self):
        return {
            "discos": self.total_discos,
            "movimentos": self.movimentos,
            "movimentos_otimos": self.optimal_moves(),
            "tempo_segundos": self.elapsed_seconds(),
        }
