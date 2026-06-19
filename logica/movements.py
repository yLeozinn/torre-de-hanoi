"""Aplicacao de movimentos recebidos pela interface."""

from logica.rules import can_move


def move_disk(estado_jogo, origem, destino):
    """Move o disco do topo quando a regra permitir."""
    valido, mensagem = can_move(estado_jogo, origem, destino)
    if not valido:
        return False, mensagem

    disco = estado_jogo.torres[origem].pop()
    estado_jogo.torres[destino].append(disco)
    return True, mensagem
