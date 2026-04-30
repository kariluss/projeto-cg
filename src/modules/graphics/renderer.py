import pygame
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, YELLOW, BLACK
from src.modules.graphics.main import bresenham, scanline_fill, setPixel, sutherland_hodgman_clip, scanline_texture
from src.modules.math.math import Matrix, get_translation_matrix, get_rotation_matrix, get_scale_matrix, get_window_to_viewport_matrix

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        
        # Viewport do Mundo (Viewport Principal)
        self.w_xmin, self.w_ymin = 0, 0
        self.w_xmax, self.w_ymax = SCREEN_WIDTH, SCREEN_HEIGHT

        # Viewport do Radar (Minimapa)
        self.VP_WIDTH, self.VP_HEIGHT = 150, 150
        self.v_xmin = SCREEN_WIDTH - self.VP_WIDTH - 20
        self.v_ymin = SCREEN_HEIGHT - self.VP_HEIGHT - 20
        self.v_xmax = self.v_xmin + self.VP_WIDTH
        self.v_ymax = self.v_ymin + self.VP_HEIGHT

        # Matriz Mundo -> Radar
        self.matrix_radar = get_window_to_viewport_matrix(
            self.w_xmin, self.w_ymin, self.w_xmax, self.w_ymax,
            self.v_xmin, self.v_ymin, self.v_xmax, self.v_ymax
        )
        
    def _get_polygon_points(self, entity):
        """Aplica a pipeline de transformação (Escala -> Rotação -> Translação) no objeto e retorna vértices no mundo."""
        transform_matrix = (
            get_translation_matrix(entity.position[0], entity.position[1]) @ 
            get_rotation_matrix(math.radians(entity.rotation)) @ 
            get_scale_matrix(entity.radius, entity.radius)
        )
        world_vertices = transform_matrix @ entity.vertices
        
        # Retorna float para maior precisão antes do Clipping
        return [
            (world_vertices.data[0][i], world_vertices.data[1][i]) 
            for i in range(world_vertices.cols)
        ]

    def draw_world_entities(self, ship, asteroids, bullets, textures_map):
        self.screen.fill(BLACK)
        
        # 1. Pipeline para a Nave Principal (com Clipping Ativo)
        ship_pts = self._get_polygon_points(ship)
        clipped_ship = sutherland_hodgman_clip(ship_pts, self.w_xmin, self.w_ymin, self.w_xmax, self.w_ymax)
        if clipped_ship:
            scanline_fill(self.screen, clipped_ship, ship.color)
            
        # 2. Pipeline para os Asteroides
        for a in asteroids:
            ast_pts = self._get_polygon_points(a)
            # Para textura, já validamos X e Y dentro do `scanline_texture`.
            # Não aplicamos Sutherland-Hodgman aqui pq ele alteraria o array de pontos e 
            # não temos um algoritmo para interpolar os atributos UV para os novos vértices criados na borda do clipping.
            ast_pts_int = [(int(round(x)), int(round(y))) for x, y in ast_pts]
            
            tex = None
            if a.radius == 30: tex = textures_map.get('30p')
            elif a.radius == 20: tex = textures_map.get('20p')
            elif a.radius == 10: tex = textures_map.get('10p')
            
            if tex:
                scanline_texture(self.screen, ast_pts_int, a.uvs, tex)
            else:
                # Fallback preenchido com clipping sem textura
                clipped_ast = sutherland_hodgman_clip(ast_pts, self.w_xmin, self.w_ymin, self.w_xmax, self.w_ymax)
                if clipped_ast:
                    scanline_fill(self.screen, clipped_ast, WHITE)
                
        # 3. Pipeline para os Tiros (Clipping Point bounds-check puro)
        for b in bullets:
            bx, by = int(round(b.position[0])), int(round(b.position[1]))
            # Clipping Check Point-Viewport
            if self.w_xmin <= bx < self.w_xmax and self.w_ymin <= by < self.w_ymax:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        nx, ny = bx+dx, by+dy
                        if self.w_xmin <= nx < self.w_xmax and self.w_ymin <= ny < self.w_ymax: 
                            setPixel(self.screen, nx, ny, b.color)

    def draw_radar(self, ship, asteroids):
        # Caixa do radar
        pygame.draw.rect(self.screen, WHITE, (self.v_xmin, self.v_ymin, self.VP_WIDTH, self.VP_HEIGHT), 1)

        self._render_on_radar(ship, is_ship=True)
        for a in asteroids:
            self._render_on_radar(a)
            
    def _render_on_radar(self, entity, is_ship=False):
        world_pts = self._get_polygon_points(entity)
        
        radar_pts = []
        for x, y in world_pts:
            vec = Matrix(3, 1, [[x], [y], [1]])
            vec_transformed = self.matrix_radar @ vec
            radar_pts.append((vec_transformed.data[0][0], vec_transformed.data[1][0]))

        clipped_pts = sutherland_hodgman_clip(radar_pts, self.v_xmin, self.v_ymin, self.v_xmax, self.v_ymax)
        
        if clipped_pts:
            cor_radar = RED if is_ship else YELLOW
            scanline_fill(self.screen, clipped_pts, cor_radar)
