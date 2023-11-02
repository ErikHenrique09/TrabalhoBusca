class Agente:
    def __init__(self, labirinto, posicao):
        self.labirinto = labirinto
        self.posicao = posicao  # Posição inicial do agente

    def mover(self, direcao):

        if direcao == 'left' and self.posicao[1] > 0:
            # esquerda
            self.posicao[1]-=1
        elif direcao == 'right' and self.posicao[1] < len(self.labirinto[0])-1:
            # direita
            self.posicao[1]+=1
        elif direcao == 'top' and self.posicao[0] > 0:
            # cima
            self.posicao[0]-=1
        elif direcao == 'down' and self.posicao[0] < len(self.labirinto)-1:
            # baixo
            self.posicao[0]+=1
        else:
            print("Movimento invalido!!!")
            pass
