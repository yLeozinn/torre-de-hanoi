import Torre as t
import os
import click

torres = {
    "A": torreA,
    "B": torreB,
    "C": torreC
}

def main():
    n = int(input("Com quantos pinos deseja jogar?\n\n-> "))

    torreA = t.Torre(n)
    torreB = t.Torre(n)
    torreC = t.Torre(n)

    for i in range(n,0,-1):
        torreA.empilhar(i)

    while not torreC.jogadorVenceu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nObjetivo:\nMover todos os discos da torre A para a torre C.\n\n")
        print("Regras:\nApenas um disco pode ser movido por vez.\nNão é permitido colocar um disco maior sobre um menor.\n\n")

        torreA.mostrarTorre()
        torreB.mostrarTorre()
        torreC.mostrarTorre()

        print("\n\nDigite seu movimento (origem destino ou 'X X' para reiniciar): ")
        letra = input()
        origem, destino = letra[0], letra[1]

        if origem.lower() == 'x' and destino.lower() == 'x':
            print("Reiniciando o desafio...\n")
            print("Pressione qualquer coisa...\n")
            char = click.getchar()
            torreA = t.Torre(n)
            torreB = t.Torre(n)
            torreC = t.Torre(n)
            for i in range(n,0,-1):
                torreA.empilhar(i)
            continue

        torreOrigem = torres.get(origem.upper())
        torreDestino = torres.get(destino.upper())

        if not torreOrigem or not torreDestino:
            print("\nTorre inválida! Use apenas A, B ou C.\n")
            print("Pressione qualquer coisa para tentar novamente...\n")
            char = click.getchar()
            continue

        discoMovido = torreOrigem.desempilhar()
        if discoMovido == -1:
            print("Movimento inválido: torre de origem vazia!\n")
            digitando("Pressione qualquer coisa para tentar novamente...\n")
            char = click.getchar()
            continue

        if not torreDestino.torreVazia() and torreDestino.topoTorre() < discoMovido:
            print("Movimento inválido: não pode colocar disco maior sobre menor.\n")
            torreOrigem.empilhar(discoMovido)
            digitando("Pressione qualquer coisa para tentar novamente...\n", 10)
            char = click.getchar()
            continue

        torreDestino.empilhar(discoMovido)
    
    
    os.system('cls' if os.name == 'nt' else 'clear')
    torreA.mostrarTorre()
    torreB.mostrarTorre()
    torreC.mostrarTorre()
    print("\nVOCÊ CONCLUIU O DESAFIO.\n")
    char = click.getchar()
