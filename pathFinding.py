import math
from queue import PriorityQueue

import pygame

# Como vai ser a janela
LARGURA = 800
JANELA = pygame.display.set_mode((LARGURA, LARGURA))
pygame.display.set_caption("A* Path Finding")

# Quais serão as cores
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 255, 0)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
ROXO = (128, 0, 128)
LARANJA = (255, 165 ,0)
CINZA = (128, 128, 128)
TURQUESA = (64, 224, 208)

class Ponto:
    def __init__(self, linha, coluna, largura, total_linhas):
        self.linha = linha
        self.coluna = coluna
        self.x = linha * largura
        self.y = coluna * largura
        self.cor = BRANCO
        self.vizinho = []
        self.largura = largura
        self.total_linhas = total_linhas

    def get_pos(self):
        return self.linha, self.coluna
    # checa se esta fechado, aberto ou bloqueado
    def ta_fechado(self):
        return self.cor == VERMELHO
    def ta__aberto(self):
        return self.cor == VERDE
    def ta_bloqueado(self):
        return self.cor == PRETO
    
    # define começo e fim
    def e_Comeco(self):
        return self.cor == LARANJA
    def e_Final(self):
        return self.cor == TURQUESA

    def reset(self):
        self.cor = BRANCO
    
    # define oq vai ser cada coisa
    def faz_inicio(self):
        self.cor = LARANJA
    def faz_fechado(self):
        self.cor = VERMELHO
    def faz_aberto(self):
        self.cor = VERDE
    def faz_barreira(self):
        self.cor = PRETO
    def faz_final(self):
        self.cor = TURQUESA
    def faz_caminho(self):
        self.cor = ROXO
    
    # Desenha os quadrados na tela
    def draw(self, win):
        pygame.draw.rect(win, self.cor, (self.x, self.y, self.largura, self.largura))
    
    def update_vizinhos(self, grid):
        self.vizinhos = []
        # Para BAIXO
        if self.linha < self.total_linhas - 1 and not grid[self.linha +1 ][self.coluna].ta_bloqueado():
            self.vizinhos.append(grid[self.linha + 1][self.coluna])
        # Para CIMA
        if self.linha > 0 and not grid[self.linha - 1][self.coluna].ta_bloqueado():
            self.vizinhos.append(grid[self.linha - 1][self.coluna])
        #Para DIREITA
        if self.coluna < self.total_linhas - 1 and not grid[self.linha][self.coluna + 1].ta_bloqueado(): 
            self.vizinhos.append(grid[self.linha][self.coluna + 1])
        #Para ESQUERDA
        if self.coluna > 0 and not grid[self.linha][self.coluna - 1].ta_bloqueado(): 
            self.vizinhos.append(grid[self.linha][self.coluna - 1])

    def __lt__(self, other):
        return False
# Define os "pontos de distancia" de um ponto a outro ponto
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2)+ abs(y1 - y2)

# reconstroi o caminho
def reconstroi_caminho(vem_de, atual, draw):
    while atual in vem_de:
        atual = vem_de[atual]
        atual.faz_caminho()
        draw()



# algoritimo para qual sera o caminho escolhido
def algoritimo(draw, grid, inicio, fim):
    contador = 0
    open_set = PriorityQueue()
    open_set.put((0, contador, inicio))
    vem_de = {}
    # Ve a pontuação do caminho des do inicio até o fim
    pontos_g = {ponto: float("inf") for linha in grid for ponto in linha}
    pontos_g[inicio] = 0
    # estimativa de quantos pontos sera para chegar ao fim
    pontos_f = {ponto: float("inf") for linha in grid for ponto in linha}
    pontos_f[inicio] = h(inicio.get_pos(), fim.get_pos())

    # Para ver se valos estão no open_set
    open_set_hash = {inicio}

    while not open_set.empty():
        #para poder sair caso aja um problema
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
        #pega o ponto associado com o ponto atual e remove do hash
        atual = open_set.get()[2]
        open_set_hash.remove(atual)
        #checa se chegou ao final e finaliza o algoritimo
        if atual == fim:
            reconstroi_caminho(vem_de, fim, draw)
            fim.faz_final()
            return True
        # considera todos os vizinhos do ponto atual
        for vizinho in atual.vizinhos:
            # calcula os pontos_g temporarios 
            temp_pontos_g = pontos_g[atual] + 1
            # se for menos que os pontos_g atualize, pois a um caminho melhor
            if temp_pontos_g < pontos_g[vizinho]:
                vem_de[vizinho]= atual
                pontos_g[vizinho] = temp_pontos_g
                pontos_f[vizinho] = temp_pontos_g + h(vizinho.get_pos(), fim.get_pos())
                # adicione ao hash se n estiverem ainda
                if vizinho not in open_set_hash:
                    contador +=1
                    open_set.put((pontos_f[vizinho], contador, vizinho))
                    open_set_hash.add(vizinho)
                    vizinho.faz_aberto()

        draw()

        if atual != inicio:
            atual.faz_fechado()
    return False
# Faz a grid de pontos(quadrados)
def faz_grid(linhas, largura):
    grid = []
    espaco = largura // linhas
    for i in range(linhas):
        grid.append([])
        for j in range(linhas):
            ponto = Ponto(i, j, espaco, linhas)
            grid[i].append(ponto)
    return grid
# Desenha a grid
def draw_grid(win, linhas, largura):
    espaco = largura // linhas
    for i in range(linhas):
        pygame.draw.line(win, CINZA, (0, i * espaco), (largura, i * espaco))
        for j in range(linhas):
            pygame.draw.line(win, CINZA, (j * espaco, 0), (j * espaco, largura))

def draw(win, grid, linhas, largura):
    win.fill(BRANCO)

    for linha in grid:
        for ponto in linha:
            ponto.draw(win)
    draw_grid(win, linhas, largura)
    pygame.display.update()

# define a posição do clique na grid
def get_clique_pos(pos, linhas, largura):
    espaco = largura // linhas
    y, x = pos

    linha = y // espaco
    coluna = x // espaco

    return linha, coluna

def main(win, largura):
    tamanho = int(input("Qual o tamanho do quadrado (lado x lado): "))
    LINHAS = tamanho
    grid = faz_grid(LINHAS, largura)

    inicio = None
    fim = None

    run = True
    while run:
        draw(win, grid, LINHAS, largura)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:# esquerda 
                pos = pygame.mouse.get_pos()
                linha, coluna = get_clique_pos(pos, LINHAS, largura)
                ponto = grid[linha][coluna]
                if not inicio and ponto != fim:
                    inicio = ponto
                    inicio.faz_inicio()
                elif not fim and ponto != inicio:
                    fim = ponto
                    fim.faz_final()
                elif ponto != fim and ponto != inicio:
                    ponto.faz_barreira()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                linha, coluna = get_clique_pos(pos, LINHAS, largura)
                ponto = grid[linha][coluna]
                ponto.reset()
                if ponto == inicio:
                    inicio = None
                if ponto == fim:
                    fim = None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and inicio and fim:
                    for linha in grid:
                        for ponto in linha:
                            ponto.update_vizinhos(grid)

                    algoritimo(lambda: draw(win, grid, LINHAS, largura), grid, inicio, fim)
                if evento.key == pygame.K_c:
                    inicio = None
                    fim = None
                    grid = faz_grid(LINHAS, largura)

    pygame.quit()

main(JANELA, LARGURA)
