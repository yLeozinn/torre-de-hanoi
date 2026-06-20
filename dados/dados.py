import csv
import os

def salvar_resultado_csv(nome, passos, tempo_gasto, arquivo="resultados.csv"):
    # Verifica se o arquivo já existe para saber se precisamos criar o cabeçalho
    arquivo_existe = os.path.isfile(arquivo)
    
    # Abre o arquivo em modo 'a' (append) para adicionar dados
    with open(arquivo, mode='a', newline='', encoding='utf-8') as file:
        escritor = csv.writer(file)
        
        # Se for a primeira vez criando o arquivo, escreve o cabeçalho
        if not arquivo_existe:
            escritor.writerow(["Nome do Jogador", "Movimentos", "Tempo (segundos)"])
            
        # Grava os dados da partida atual
        escritor.writerow([nome, passos, f"{tempo_gasto:.2f}"])
        
    print(f"\nResultado de {nome} salvo com sucesso no arquivo {arquivo}!")