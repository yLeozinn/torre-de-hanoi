"""Painel textual simples para acompanhar resultados."""


def build_summary(registros):
    if not registros:
        return "Nenhuma partida registrada."

    linhas = ["Resultados da turma:"]
    for indice, registro in enumerate(registros, start=1):
        movimentos = registro.get("movimentos", 0)
        ideal = registro.get("movimentos_otimos", 0)
        tempo = registro.get("tempo_segundos", 0)
        linhas.append(
            f"Partida {indice}: {movimentos} movimentos, otimo {ideal}, {tempo}s"
        )
    return "\n".join(linhas)
