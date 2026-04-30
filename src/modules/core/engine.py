import pygame
import sys
import math
import random
from src.settings import *
from src.modules.entities.Ship import Ship
from src.modules.entities.Asteroid import Asteroid
from src.modules.entities.Bullet import Bullet
from src.modules.physics.CollisionSystem import CollisionSystem
from src.modules.physics.PhysicsSystem import PhysicsSystem
from src.modules.game.manager import GameManager
from src.modules.graphics.main import bresenham, scanline_fill, setPixel, sutherland_hodgman_clip, desenhar_poligono_bordas, scanline_texture
from src.modules.math.math import Matrix, get_translation_matrix, get_rotation_matrix, get_scale_matrix, get_window_to_viewport_matrix

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
        self.game_manager.start_new_wave(self.asteroids)

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
            rad = math.radians(self.ship.rotation)
            bullet_pos = [self.ship.position[0] + self.ship.radius * math.sin(rad),
                          self.ship.position[1] - self.ship.radius * math.cos(rad)]
            bullet = Bullet(bullet_pos, self.ship.rotation)
            bullet.velocity = [bullet.speed * math.sin(rad), -bullet.speed * math.cos(rad)]
            self.bullets.append(bullet)
            self.ship.shoot_cooldown = self.ship.shoot_delay

    def _update(self):
        if self.state == "RUNNING":
            self.ship.rotation += self.ship.rotation_input * 4
            if self.ship.thrust_input:
                rad = math.radians(self.ship.rotation)
                self.ship.velocity[0] += self.ship.acceleration * math.sin(rad)
                self.ship.velocity[1] -= self.ship.acceleration * math.cos(rad)
            
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
            
            if self.game_manager.check_wave_completion(self.asteroids):
                self.game_manager.start_new_wave(self.asteroids)

    def _get_polygon_points(self, entity):
        """Aplica a pipeline de transformação (Escala -> Rotação -> Translação) e retorna as coordenadas da tela."""
        transform_matrix = (
            get_translation_matrix(entity.position[0], entity.position[1]) @ 
            get_rotation_matrix(math.radians(entity.rotation)) @ 
            get_scale_matrix(entity.radius, entity.radius)
        )
        world_vertices = transform_matrix @ entity.vertices
        
        return [
            (int(round(world_vertices.data[0][i])), int(round(world_vertices.data[1][i]))) 
            for i in range(world_vertices.cols)
        ]

    def _render(self):
        self.screen.fill(BLACK)
        
        # 1. RENDERIZAÇÃO DA TELA PRINCIPAL (O MUNDO)
        ship_pts = self._get_polygon_points(self.ship)
        scanline_fill(self.screen, ship_pts, self.ship.color)
        
        for a in self.asteroids:
            ast_pts = self._get_polygon_points(a)
            if a.radius == 30:
                scanline_texture(self.screen, ast_pts, a.uvs, self.moon_texture_30p)
            elif a.radius == 20:
                scanline_texture(self.screen, ast_pts, a.uvs, self.moon_texture_20p)
            elif a.radius == 10:
                scanline_texture(self.screen, ast_pts, a.uvs, self.moon_texture_10p)
            # Opcional: deixar as bordas brancas pra dar um destaque, ou remover.
            #desenhar_poligono_bordas(self.screen, ast_pts, WHITE)
        
        #for a in self.asteroids:
        #    ast_pts = self._get_polygon_points(a)
        #    desenhar_poligono_bordas(self.screen, ast_pts, WHITE)
            
        for b in self.bullets:
            bx, by = int(round(b.position[0])), int(round(b.position[1]))
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if 0 <= bx+dx < SCREEN_WIDTH and 0 <= by+dy < SCREEN_HEIGHT: 
                        setPixel(self.screen, bx+dx, by+dy, b.color)
        
        # ==============================================================
        # 2. RENDERIZAÇÃO DO RADAR (MINIMAPA) USANDO VIEWPORT E CLIPPING
        # ==============================================================
        
        # Dimensões da Viewport do Radar (canto inferior direito)
        VP_WIDTH, VP_HEIGHT = 150, 150
        v_xmin = SCREEN_WIDTH - VP_WIDTH - 20
        v_ymin = SCREEN_HEIGHT - VP_HEIGHT - 20
        v_xmax = v_xmin + VP_WIDTH
        v_ymax = v_ymin + VP_HEIGHT

        # Matriz que transforma o Mundo inteiro para dentro do Radar
        matrix_radar = get_window_to_viewport_matrix(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,  # Mundo
            v_xmin, v_ymin, v_xmax, v_ymax      # Viewport do Radar
        )

        # Desenhar a borda do Radar (uma linha ao redor)
        pygame.draw.rect(self.screen, WHITE, (v_xmin, v_ymin, VP_WIDTH, VP_HEIGHT), 1)

        # Função auxiliar para renderizar entidades no Radar
        def render_on_radar(entity, is_ship=False):
            # Obtém os vértices no espaço do mundo
            world_pts = self._get_polygon_points(entity)
            
            # Transforma os vértices do Mundo para a Viewport do Radar
            radar_pts = []
            for x, y in world_pts:
                # Cria vetor [x, y, 1] e multiplica pela matriz do radar
                vec = Matrix(3, 1, [[x], [y], [1]])
                vec_transformed = matrix_radar @ vec
                radar_pts.append((vec_transformed.data[0][0], vec_transformed.data[1][0]))

            # CLIPPING: Corta o que vazar do radar para não sujar a tela
            clipped_pts = sutherland_hodgman_clip(radar_pts, v_xmin, v_ymin, v_xmax, v_ymax)
            
            if clipped_pts:
                cor_radar = RED if is_ship else YELLOW
                scanline_fill(self.screen, clipped_pts, cor_radar)

        # Desenhar Nave e Asteroides no radar
        render_on_radar(self.ship, is_ship=True)
        for a in self.asteroids:
            render_on_radar(a)
        # ==============================================================

        # UI e Textos
        font = pygame.font.Font(None, 36)
        txt = f"Score: {self.game_manager.score} | Wave: {self.game_manager.wave} | Lives: {self.game_manager.lives}"
        self.screen.blit(font.render(txt, True, WHITE), (10, 10))
        
        if self.state == "GAME_OVER": 
            self.screen.blit(font.render("GAME OVER", True, RED), (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
        elif self.state == "PAUSED": 
            self.screen.blit(font.render("PAUSED", True, YELLOW), (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            
        pygame.display.flip()

    def run(self):
        while self.running:
            self._process_events(); self._update(); self._render()
            self.clock.tick(FPS)
        pygame.quit(); sys.exit()