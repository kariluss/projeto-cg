import pygame
import sys
from src.config import *
from src.modules.entities.Ship import Ship
from src.modules.entities.Asteroid import Asteroid
from src.modules.entities.Bullet import Bullet
from src.modules.physics.CollisionSystem import CollisionSystem
from src.modules.physics.PhysicsSystem import PhysicsSystem
from src.modules.game.manager import GameManager
from src.modules.graphics.renderer import Renderer

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.key.stop_text_input()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "RUNNING"
        
        # CARREGANDO A TEXTURA DA LUA
        # (Certifique-se de ter um arquivo 'moon.jpg' na mesma pasta onde roda o script)
        try:
            self.moon_texture_30p = pygame.image.load("./assets/moon-8bit-30p.png").convert()
            self.moon_texture_20p = pygame.image.load("./assets/moon-8bit-20p.png").convert()
            self.moon_texture_10p = pygame.image.load("./assets/moon-8bit-10p.png").convert()
        except:
            print("AVISO: 'moon-8bit-30p.png', 'moon-8bit-20p.png', 'moon-8bit-10p.png' não encontrada! Criando textura roxa de fallback.")
            self.moon_texture_30p = pygame.Surface((128, 128))
            self.moon_texture_30p.fill((150, 0, 150))
            self.moon_texture_20p = pygame.Surface((128, 128))
            self.moon_texture_20p.fill((150, 0, 150))
            self.moon_texture_10p = pygame.Surface((128, 128))
            self.moon_texture_10p.fill((150, 0, 150))
            
        self.ship = Ship()
        self.ship.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.bullets = []
        self.asteroids = []
        
        self.game_manager = GameManager()
        self.game_manager.initialize(self.asteroids)
        
        self.renderer = Renderer(self.screen)
        self.textures_map = {
            '30p': self.moon_texture_30p,
            '20p': self.moon_texture_20p,
            '10p': self.moon_texture_10p
        }
        self.font = pygame.font.Font(None, 36)

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.running = False
                if event.key == pygame.K_p: self.state = "PAUSED" if self.state == "RUNNING" else "RUNNING"
                if event.key in (pygame.K_LEFT, pygame.K_a): self.ship.rotation_input = -1
                elif event.key in (pygame.K_RIGHT, pygame.K_d): self.ship.rotation_input = 1
                if event.key in (pygame.K_UP, pygame.K_w): self.ship.thrust_input = True
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a) and self.ship.rotation_input == -1: self.ship.rotation_input = 0
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and self.ship.rotation_input == 1: self.ship.rotation_input = 0
                if event.key in (pygame.K_UP, pygame.K_w): self.ship.thrust_input = False

    def _handle_shooting(self):
        if self.ship.shoot_cooldown > 0: self.ship.shoot_cooldown -= 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.ship.shoot_cooldown <= 0:
            offset = PhysicsSystem.calculate_bullet_velocity(self.ship.rotation, self.ship.radius)
            bullet_pos = [self.ship.position[0] + offset[0], self.ship.position[1] + offset[1]]
            bullet = Bullet(bullet_pos, self.ship.rotation)
            bullet.velocity = PhysicsSystem.calculate_bullet_velocity(self.ship.rotation, bullet.speed)
            self.bullets.append(bullet)
            self.ship.shoot_cooldown = self.ship.shoot_delay

    def _update(self):
        if self.state == "RUNNING":
            PhysicsSystem.apply_controls(self.ship, self.ship.thrust_input, self.ship.rotation_input)
            
            PhysicsSystem.update_all([self.ship] + self.bullets + self.asteroids)
            PhysicsSystem.apply_wrap_around(self.ship)
            
            margin = 80
            for bullet in self.bullets:
                bullet.distance_traveled += bullet.speed
                if (bullet.distance_traveled >= bullet.max_distance or 
                    not ( -margin < bullet.position[0] < SCREEN_WIDTH + margin and -margin < bullet.position[1] < SCREEN_HEIGHT + margin)):
                    bullet.alive = False
            
            for asteroid in self.asteroids:
                if not ( -margin < asteroid.position[0] < SCREEN_WIDTH + margin and -margin < asteroid.position[1] < SCREEN_HEIGHT + margin):
                    self.game_manager.handle_offscreen_asteroid(asteroid, self.asteroids)

            self._handle_shooting()
            self.bullets = [b for b in self.bullets if b.alive]
            self.asteroids = [a for a in self.asteroids if a.alive]
            
            collisions = CollisionSystem.check_bullet_asteroid_collisions(self.bullets, self.asteroids)
            for b_idx, a_idx in collisions:
                bullet, asteroid = self.bullets[b_idx], self.asteroids[a_idx]
                bullet.alive = False
                self.game_manager.handle_asteroid_destruction(asteroid, self.asteroids, self.ship.position)
            
            if CollisionSystem.check_ship_asteroid_collisions(self.ship, self.asteroids):
                self.game_manager.lives -= 1
                if self.game_manager.lives <= 0: self.state = "GAME_OVER"
                else:
                    self.ship.position, self.ship.velocity = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], [0.0, 0.0]
                    self.bullets = []
            
            self.game_manager.update_difficulty(self.asteroids)

    def _render(self):
        self.renderer.draw_world_entities(self.ship, self.asteroids, self.bullets, self.textures_map)
        self.renderer.draw_radar(self.ship, self.asteroids)

        # UI e Textos
        txt = f"Score: {self.game_manager.score} | Lives: {self.game_manager.lives}"
        self.screen.blit(self.font.render(txt, True, WHITE), (10, 10))
        
        if self.state == "GAME_OVER": 
            self.screen.blit(self.font.render("GAME OVER", True, RED), (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
        elif self.state == "PAUSED": 
            self.screen.blit(self.font.render("PAUSED", True, YELLOW), (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            
        pygame.display.flip()

    def run(self):
        while self.running:
            self._process_events(); self._update(); self._render()
            self.clock.tick(FPS)
        pygame.quit(); sys.exit()