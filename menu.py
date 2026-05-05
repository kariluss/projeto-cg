import pygame
import math
import random
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, YELLOW, RED
from src.modules.entities.Asteroid import Asteroid
from src.modules.physics.PhysicsSystem import PhysicsSystem


class MenuScreen:
    """Menu inicial com asteroides voadores de fundo e animações"""
    
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_started = False
        
        # Fonte para o título (grande e ousada)
        self.title_font = pygame.font.Font(None, 120)
        self.subtitle_font = pygame.font.Font(None, 32)
        
        # Asteroides de fundo
        self.background_asteroids = []
        self._initialize_background_asteroids()
        
        # Animação de piscada do texto "Aperte Enter"
        self.blink_timer = 0
        self.blink_interval = 30  # frames entre piscadas (30 frames = 1 segundo a 30 FPS)
        self.show_start_text = True
        
        # Cores com tema retro-futurista
        self.title_color = (255, 255, 255)  # Ciano neon
        self.subtitle_color = (255, 255, 255)  # Magenta neon
        self.glow_color = (100, 50, 255)  # Roxo para efeito glow
        
    def _initialize_background_asteroids(self):
        """Cria asteroides que voam no fundo do menu"""
        for _ in range(6):
            pos = [random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT)]
            size = random.choice([Asteroid.SIZE_LARGE, Asteroid.SIZE_MEDIUM, Asteroid.SIZE_SMALL])
            asteroid = Asteroid(pos, size)
            asteroid.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
            self.background_asteroids.append(asteroid)
    
    def _process_events(self):
        """Processa eventos de entrada"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_started = True
                    self.running = False
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def _update(self):
        """Atualiza lógica do menu"""
        # Atualiza asteroides
        PhysicsSystem.update_all(self.background_asteroids)
        for asteroid in self.background_asteroids:
            PhysicsSystem.apply_wrap_around(asteroid)
        
        # Atualiza animação de piscada
        self.blink_timer += 1
        if self.blink_timer >= self.blink_interval * 2:
            self.blink_timer = 0
        
        self.show_start_text = self.blink_timer < self.blink_interval
    
    def _draw_glow_text(self, text, font, color, x, y):
        """Desenha texto com efeito glow sutil (apenas brilho nas bordas)"""
        # Renderiza o glow apenas nas laterais (bem sutil)
        for offset in range(2, 0, -1):
            glow_surf = font.render(text, True, color)
            glow_surf.set_alpha(15)
            self.screen.blit(glow_surf, (x - offset, y))
            self.screen.blit(glow_surf, (x + offset, y))
        
        # Renderiza o texto principal
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.screen.blit(text_surf, text_rect)
    
    def _render(self):
        """Renderiza a tela do menu"""
        # Fundo preto
        self.screen.fill(BLACK)
        
        # Desenha asteroides de fundo com baixa opacidade
        self._render_background_asteroids()
        
        # Título com glow sutil
        title_y = SCREEN_HEIGHT // 2 - 60
        self._draw_glow_text("ASTEROIDS", self.title_font, self.title_color, SCREEN_WIDTH // 2, title_y)
        
        # Texto "Aperte Enter" com animação de piscada
        if self.show_start_text:
            subtitle_y = SCREEN_HEIGHT // 2 + 60
            subtitle_text = "APERTE ENTER PARA COMEÇAR"
            self._draw_glow_text(subtitle_text, self.subtitle_font, self.subtitle_color, SCREEN_WIDTH // 2, subtitle_y)
        
        pygame.display.flip()
    
    def _render_background_asteroids(self):
        """Renderiza os asteroides de fundo com opacidade reduzida"""
        # Cria uma superfície temporária para asteroides com transparência
        temp_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        from src.modules.graphics.renderer import Renderer
        from src.modules.math.math import get_translation_matrix, get_rotation_matrix, get_scale_matrix
        
        for asteroid in self.background_asteroids:
            # Calcula transformação (igual ao renderer normal)
            transform_matrix = (
                get_translation_matrix(asteroid.position[0], asteroid.position[1]) @ 
                get_rotation_matrix(math.radians(asteroid.rotation)) @ 
                get_scale_matrix(asteroid.radius, asteroid.radius)
            )
            world_vertices = transform_matrix @ asteroid.vertices
            
            # Cria lista de pontos
            points = [
                (world_vertices.data[0][i], world_vertices.data[1][i]) 
                for i in range(world_vertices.cols)
            ]
            
            # Desenha com cor reduzida e transparência
            if len(points) >= 3:
                pygame.draw.polygon(temp_surf, (100, 100, 150, 80), points, 2)
        
        # Reduz opacidade geral dos asteroides
        temp_surf.set_alpha(50)
        self.screen.blit(temp_surf, (0, 0))
    
    def run(self):
        """Loop principal do menu"""
        while self.running:
            self._process_events()
            self._update()
            self._render()
            self.clock.tick(30)  # 30 FPS como no jogo
        
        return self.game_started