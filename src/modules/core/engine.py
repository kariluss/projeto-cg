import pygame
import sys
import math
from src.settings import *
from src.modules.graphics.main import bresenham, scanline_fill
from src.modules.math.math import Matrix, get_translation_matrix, get_rotation_matrix
from src.modules.entities.Ship import Ship

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "RUNNING"
        
        # Instanciamos a entidade pura
        self.ship = Ship()
        self.ship.position = [400, 300]

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_p:
                    self.state = "PAUSED" if self.state == "RUNNING" else "RUNNING"

    def _update(self):
        if self.state == "RUNNING":
            keys = pygame.key.get_pressed()
            
            # --- ATENÇÃO: ISSO É UMA "FÍSICA FALSA" ---
            # Estamos mudando a posição e ângulo diretamente pelo input.
            if keys[pygame.K_w]:
                self.ship.position[1] -= 5
            if keys[pygame.K_s]:
                self.ship.position[1] += 5
            if keys[pygame.K_a]:
                self.ship.position[0] -= 5
            if keys[pygame.K_d]:
                self.ship.position[0] += 5
                
            if keys[pygame.K_q]:
                self.ship.rotation -= 5
            if keys[pygame.K_e]:
                self.ship.rotation += 5

    def _render(self):
        self.screen.fill(BLACK)
        
        # 1. Cria as matrizes de transformação baseadas no estado da nave
        # Lembre-se: math.radians converte graus para radianos para o sin/cos
        m_trans = get_translation_matrix(self.ship.position[0], self.ship.position[1])
        m_rot = get_rotation_matrix(math.radians(self.ship.rotation))
        
        # 2. Cria a Matriz do Mundo (Mundo = Translação * Rotação)
        m_world = m_trans @ m_rot
        
        # 3. Aplica a Matriz do Mundo aos vértices do Modelo
        world_vertices = m_world @ self.ship.vertices
        
        # 4. Extrai os pontos para o formato do rasterizador
        pontos_render = []
        for i in range(3):
            x = int(round(world_vertices.data[0][i]))
            y = int(round(world_vertices.data[1][i]))
            pontos_render.append((x, y))

        # 5. Desenha
        scanline_fill(self.screen, pontos_render, self.ship.color)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self._process_events()
            self._update()
            self._render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()