"""Regras de validade dos movimentos da Torre de Hanoi."""


def can_move(estado_jogo, origem, destino):
    """Verifica se um disco pode sair de source e ir para target."""
    if origem == destino:
        return False, "Escolha uma torre de destino diferente."

    if origem not in estado_jogo.torres or destino not in estado_jogo.torres:
        return False, "Torre invalida."

    disco_origem = estado_jogo.top_disk(origem)
    disco_destino = estado_jogo.top_disk(destino)

    if disco_origem is None:
        return False, "A torre de origem esta vazia."

    if disco_destino is not None and disco_origem > disco_destino:
        return False, "Nao coloque um disco maior sobre um menor."

    return True, "Movimento realizado."
