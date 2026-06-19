"""Exportacao simples de metricas para CSV."""

import csv


def export_csv(registros, caminho_arquivo):
    if not registros:
        return

    campos = list(registros[0].keys())
    with open(caminho_arquivo, "w", newline="", encoding="utf-8") as arquivo_csv:
        escritor = csv.DictWriter(arquivo_csv, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(registros)
