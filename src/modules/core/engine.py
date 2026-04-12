import pygame
import sys
from src.settings import *

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "RUNNING"  # RUNNING, PAUSED, GAME_OVER

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
            pass

    def _render(self):
        self.screen.fill(BLACK)
        
        # Aqui entrará a renderização (gráficos, math para transformações)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self._process_events()
            self._update()
            self._render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
