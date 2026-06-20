import os
import click
import torre
import time
import csv
from dados import salvar_resultado_csv
from torre import Torre #Trazendo a classe Torre do arquivo torre.py

def main():
    print("--- BEM-VINDO À TORRE DE HANÓI ---")
    nome_jogador = input("Qual é o seu nome? -> ").strip()

    n = int(input("Com quantos discos deseja jogar?\n\n-> "))
    
    #  contagem de movimentos 
    movimentos = 0
    movimentos_minimos = (2**n) - 1 

    tempo_inicio = time.time()

    torreA = Torre(n)
    torreB = Torre(n)
    torreC = Torre(n)

    # O dicionário foi movido para cá, depois das torres serem criadas
    torres = {
        "A": torreA,
        "B": torreB,
        "C": torreC
    }

    # Preenchendo a Torre A
    for i in range(n, 0, -1):
        torreA.empilhar(i)

    while not torreC.jogadorVenceu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- TORRE DE HANÓI ---")
        print("Objetivo: Mover todos os discos da torre A para a torre C.")
        print("Regras: Apenas um disco pode ser movido por vez. Não coloque um disco maior sobre um menor.")
        print(f"\nMovimentos: {movimentos} / Ideal: {movimentos_minimos}\n")

        print("Torre A:")
        torreA.mostrarTorre()
        print("\nTorre B:")
        torreB.mostrarTorre()
        print("\nTorre C:")
        torreC.mostrarTorre()

        print("\nDigite seu movimento (ex: 'A B' para mover de A para B) ou 'X X' para reiniciar: ")
        letra = input().strip()

        # Tratamento seguro da entrada usando split()
        try:
            origem, destino = letra.split()
        except ValueError:
            print("\nEntrada inválida! Digite as duas torres separadas por espaço.")
            print("Pressione qualquer tecla para tentar novamente...")
            click.getchar()
            continue

        if origem.upper() == 'X' and destino.upper() == 'X':
            print("\nReiniciando o desafio...")
            print("Pressione qualquer tecla...")
            click.getchar()
            movimentos = 0
            torreA = Torre(n)
            torreB = Torre(n)
            torreC = Torre(n)
            torres = {"A": torreA, "B": torreB, "C": torreC}
            for i in range(n, 0, -1):
                torreA.empilhar(i)
            continue

        torreOrigem = torres.get(origem.upper())
        torreDestino = torres.get(destino.upper())

        if not torreOrigem or not torreDestino:
            print("\nTorre inválida! Use apenas A, B ou C.")
            print("Pressione qualquer tecla para tentar novamente...")
            click.getchar()
            continue

        if torreOrigem.torreVazia():
            print("\nMovimento inválido: torre de origem vazia!")
            print("Pressione qualquer tecla para tentar novamente...")
            click.getchar()
            continue

        # Espiamos o disco do topo ANTES de desempilhar
        disco_no_topo = torreOrigem.topoTorre()

        if not torreDestino.torreVazia() and torreDestino.topoTorre() < disco_no_topo:
            print("\nMovimento inválido: não pode colocar disco maior sobre menor.")
            print("Pressione qualquer tecla para tentar novamente...")
            click.getchar()
            continue

        # Se passou em todas as regras, executa o movimento
        discoMovido = torreOrigem.desempilhar()
        torreDestino.empilhar(discoMovido)
        movimentos += 1 # Computa a jogada válida
    
    tempo_fim = time.time()
    tempo_total = tempo_fim - tempo_inicio

    # Fim de jogo
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Torre C:")
    torreC.mostrarTorre()
    print(f"\nPARABÉNS, {nome_jogador.upper()}! VOCÊ CONCLUIU O DESAFIO EM {movimentos} MOVIMENTOS.\n")
    # Chama a função que veio do arquivo dados.py
    salvar_resultado_csv(nome_jogador, movimentos, tempo_total)
    
    click.getchar()


if __name__ == "__main__":
    main()