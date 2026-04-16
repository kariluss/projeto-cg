import pygame
import sys
import math
from src.settings import *
from src.modules.graphics.main import bresenham, scanline_fill
from src.modules.math.math import Matrix, get_translation_matrix, get_rotation_matrix
from src.modules.entities.Ship import Ship
from src.modules.entities.Asteroid import Asteroid
from src.modules.physics.CollisionSystem import CollisionSystem

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.key.stop_text_input()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "RUNNING"
        
        # Entidades
        self.ship = Ship()
        self.ship.position = [400, 300]
        
        self.bullets = []
        self.asteroids = []
        
        # Game state
        self.lives = 7
        self.score = 0
        self.wave = 1
        self.asteroids_destroyed_this_wave = 0
        
        # Spawnar asteroides iniciais
        self._spawn_wave()

    def _spawn_wave(self):
        """Spawna asteroides para o início de uma onda"""
        # Começa com 3 asteroides grandes
        num_asteroids = 3 + self.wave
        
        for _ in range(num_asteroids):
            # Spawna em posições aleatórias nas bordas da tela
            import random
            if random.choice([True, False]):
                x = random.choice([random.uniform(-50, 0), random.uniform(SCREEN_WIDTH, SCREEN_WIDTH + 50)])
                y = random.uniform(0, SCREEN_HEIGHT)
            else:
                x = random.uniform(0, SCREEN_WIDTH)
                y = random.choice([random.uniform(-50, 0), random.uniform(SCREEN_HEIGHT, SCREEN_HEIGHT + 50)])
            
            asteroid = Asteroid([x, y], Asteroid.SIZE_LARGE)
            self.asteroids.append(asteroid)

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_p:
                    self.state = "PAUSED" if self.state == "RUNNING" else "RUNNING"
                if event.key == pygame.K_SPACE and self.state == "RUNNING":
                    # Tentar atirar
                    bullet = self.ship.shoot()
                    if bullet:
                        self.bullets.append(bullet)

                # --- Controle da nave (WASD + SETAS) ---
                # Rotação para esquerda
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.ship.rotation_input = -1
                # Rotação para direita
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.ship.rotation_input = 1
                # Aceleração (frente)
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.ship.thrust_input = True
                
            if event.type == pygame.KEYUP:
                # Parar rotação quando a tecla for solta
                if event.key in (pygame.K_LEFT, pygame.K_a) and self.ship.rotation_input == -1:
                    self.ship.rotation_input = 0
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.ship.rotation_input == 1:
                    self.ship.rotation_input = 0
                # Parar aceleração
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.ship.thrust_input = False

    def _update(self):
        # print("Estado do jogo:", self.state)
        if self.state == "RUNNING":
            keys = pygame.key.get_pressed()
            #print("UP:", keys[pygame.K_UP], "LEFT:", keys[pygame.K_LEFT])
            
            # Atualizar nave (agora com inércia)
            self.ship.update(keys)
            
            # Atualizar bullets
            for bullet in self.bullets:
                bullet.update()
            
            # Remover bullets que não estão mais vivos
            self.bullets = [b for b in self.bullets if b.alive]
            
            # Atualizar asteroides
            for asteroid in self.asteroids:
                asteroid.update()
            
            # Remover asteroides que não estão mais vivos (saíram da tela)
            self.asteroids = [a for a in self.asteroids if a.alive]
            
            # --- COLISÕES ---
            # 1. Colisão Bullet-Asteroid
            collisions = CollisionSystem.check_bullet_asteroid_collisions(self.bullets, self.asteroids)
            
            for bullet_idx, asteroid_idx in collisions:
                bullet = self.bullets[bullet_idx]
                asteroid = self.asteroids[asteroid_idx]
                
                # Destruir bullet
                bullet.alive = False
                
                # Destruir asteroide e spawnar menores
                self.score += asteroid.points
                new_asteroids = asteroid.split()
                self.asteroids.extend(new_asteroids)
                asteroid.alive = False
                
                self.asteroids_destroyed_this_wave += 1
            
            # Remover bullets/asteroides destruídos novamente
            self.bullets = [b for b in self.bullets if b.alive]
            self.asteroids = [a for a in self.asteroids if a.alive]
            
            # 2. Colisão Ship-Asteroid
            if CollisionSystem.check_ship_asteroid_collisions(self.ship, self.asteroids):
                self.lives -= 1
                if self.lives <= 0:
                    self.state = "GAME_OVER"
                else:
                    # Respawnar a nave no centro
                    self.ship.position = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
                    self.ship.velocity = [0, 0]
                    # Limpar bullets
                    self.bullets = []
            
            # 3. Próxima onda se destruiu todos os asteroides
            if len(self.asteroids) == 0 and self.asteroids_destroyed_this_wave > 0:
                self.wave += 1
                self.asteroids_destroyed_this_wave = 0
                self._spawn_wave()

    def _render(self):
        self.screen.fill(BLACK)
        
        # --- Renderizar Nave ---
        m_trans = get_translation_matrix(self.ship.position[0], self.ship.position[1])
        m_rot = get_rotation_matrix(math.radians(self.ship.rotation))
        m_world = m_trans @ m_rot
        
        world_vertices = m_world @ self.ship.vertices
        
        pontos_render = []
        for i in range(3):
            x = int(round(world_vertices.data[0][i]))
            y = int(round(world_vertices.data[1][i]))
            pontos_render.append((x, y))
        
        scanline_fill(self.screen, pontos_render, self.ship.color)
        
        # --- Renderizar Bullets ---
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # --- Renderizar Asteroides ---
        for asteroid in self.asteroids:
            m_trans = get_translation_matrix(asteroid.position[0], asteroid.position[1])
            m_rot = get_rotation_matrix(math.radians(asteroid.rotation))
            m_scale = Matrix(3, 3, [
                [asteroid.radius / 25, 0, 0],
                [0, asteroid.radius / 25, 0],
                [0, 0, 1]
            ])
            m_world = m_trans @ m_rot @ m_scale
            
            asteroid.draw(self.screen, m_world)
        
        # --- HUD (Vidas, Pontuação, Onda) ---
        font = pygame.font.Font(None, 36)
        
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
        wave_text = font.render(f"Wave: {self.wave}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(wave_text, (10, 90))
        
        if self.state == "GAME_OVER":
            game_over_text = font.render("GAME OVER", True, RED)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        
        if self.state == "PAUSED":
            paused_text = font.render("PAUSED", True, YELLOW)
            self.screen.blit(paused_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self._process_events()
            self._update()
            self._render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()