class Torre:
    def __init__(self, qtdDiscos):
        self.topo = -1
        self.capacidade = qtdDiscos
        self.Discos = [0] * qtdDiscos
    
    def torreVazia(self):
        return self.topo == -1

    def empilhar(self, disco):
        if(self.topo < (self.capacidade - 1)):
            self.topo += 1
            self.Discos[self.topo] = disco
            return 1
        return 0
    
    def desempilhar(self):
        if (not self.torreVazia()):
            discoRemovido = self.Discos[self.topo]
            self.topo -= 1
            return discoRemovido
        return -1
    
    def topoTorre(self):
        if(not self.torreVazia()):
            return self.Discos[self.topo]
        return -1

    def mostrarTorre(self):
        print("\nEstado atual da torre:\n")
        for i in range(self.topo + 1):
            print(self.Discos[i])
        
    
