import pygame
import sys
from src.settings import *
from src.modules.graphics.main import bresenham, scanline_fill
from src.modules.math.math import Matrix, get_translation_matrix


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "RUNNING"  # RUNNING, PAUSED, GAME_OVER
        
        # Teste da nave usando matrizes (espaço do mundo inicialmente)
        # Formato: [x1, x2, x3], [y1, y2, y3], [1, 1, 1]
        # Triângulo apontando para cima
        self.ship_vertices = Matrix(3, 3, [
            [400, 380, 420],
            [250, 300, 300],
            [1, 1, 1]
        ])


    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Exemplo de controle de estado
                if event.key == pygame.K_p:
                    if self.state == "RUNNING":
                        self.state = "PAUSED"
                    elif self.state == "PAUSED":
                        self.state = "RUNNING"

    def _update(self):
        if self.state == "RUNNING":
            # Aqui entrará a lógica do jogo (física, entidades, etc)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                # Move para frente (neste teste, para cima: ty = -5)
                # O módulo math aplica M @ V, onde V são os vértices em colunas
                trans = get_translation_matrix(0, -5)
                self.ship_vertices = trans @ self.ship_vertices


    def _render(self):
        self.screen.fill(BLACK)
        
        # Converte a matriz de vértices de volta para lista de pontos (x, y)
        pontos_render = []
        for i in range(3):
            # Arredondamos para pixels (int)
            x = int(round(self.ship_vertices.data[0][i]))
            y = int(round(self.ship_vertices.data[1][i]))
            pontos_render.append((x, y))

        # Preenchimento do triângulo usando scanline
        scanline_fill(self.screen, pontos_render, WHITE)

        # Desenho das arestas usando Bresenham para maior precisão visual nas bordas
        for i in range(len(pontos_render)):
            p1 = pontos_render[i]
            p2 = pontos_render[(i + 1) % len(pontos_render)]
            bresenham(self.screen, p1[0], p1[1], p2[0], p2[1], WHITE)


        
        pygame.display.flip()

    def run(self):
        while self.running:
            self._process_events()
            self._update()
            self._render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
