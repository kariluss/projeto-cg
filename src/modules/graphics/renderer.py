import pygame
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, YELLOW, BLACK
from src.modules.graphics.main import bresenham, scanline_fill, setPixel, sutherland_hodgman_clip, scanline_texture
from src.modules.math.math import get_translation_matrix, get_rotation_matrix, get_scale_matrix, get_window_to_viewport_matrix

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
        
        # Pré-extrai os coeficientes escalares da matrix_radar (constante após __init__).
        # Como é uma transformação pura de escala+translação (sem rotação), a matriz tem a forma:
        # [[sx, 0, tx], [0, sy, ty], [0, 0, 1]]
        # Isso permite aplicar a transformação por ponto com sx*x+tx sem criar objetos Matrix.
        rd = self.matrix_radar.data
        self._radar_sx = rd[0][0]
        self._radar_sy = rd[1][1]
        self._radar_tx = rd[0][2]
        self._radar_ty = rd[1][2]
        
        # Cache de world points calculados em draw_world_entities, reutilizados em draw_radar.
        # Evita recalcular a pipeline T@R@S@vertices duas vezes por entidade por frame.
        self._world_pts_cache = {}
        
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
        
        # Limpa o cache e reconstrói os world points para este frame.
        # Cada entidade é transformada UMA vez aqui; o radar lê deste cache.
        self._world_pts_cache = {}
        
        # 1. Pipeline para a Nave Principal (com Clipping Ativo)
        ship_pts = self._get_polygon_points(ship)
        self._world_pts_cache['ship'] = ship_pts
        clipped_ship = sutherland_hodgman_clip(ship_pts, self.w_xmin, self.w_ymin, self.w_xmax, self.w_ymax)
        if clipped_ship:
            scanline_fill(self.screen, clipped_ship, ship.color)
            
        # 2. Pipeline para os Asteroides
        for i, a in enumerate(asteroids):
            ast_pts = self._get_polygon_points(a)
            self._world_pts_cache[i] = ast_pts
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

        # Reutiliza os world points já calculados em draw_world_entities.
        # O radar é um espelho: pega o estado do mundo e projeta no viewport do minimapa.
        ship_pts = self._world_pts_cache.get('ship')
        if ship_pts is None:
            ship_pts = self._get_polygon_points(ship)
        self._render_on_radar(ship_pts, is_ship=True)
        
        for i, a in enumerate(asteroids):
            ast_pts = self._world_pts_cache.get(i)
            if ast_pts is None:
                ast_pts = self._get_polygon_points(a)
            self._render_on_radar(ast_pts)
            
    def _render_on_radar(self, world_pts, is_ship=False):
        # Aplica a transformação Mundo -> Radar inline, sem criar objetos Matrix por vértice.
        # matrix_radar é escala+translação pura: [[sx,0,tx],[0,sy,ty],[0,0,1]]
        # Logo: x' = sx*x + tx  |  y' = sy*y + ty
        sx = self._radar_sx
        sy = self._radar_sy
        tx = self._radar_tx
        ty = self._radar_ty
        radar_pts = [(sx * x + tx, sy * y + ty) for x, y in world_pts]

        clipped_pts = sutherland_hodgman_clip(radar_pts, self.v_xmin, self.v_ymin, self.v_xmax, self.v_ymax)
        
        if clipped_pts:
            cor_radar = RED if is_ship else YELLOW
            scanline_fill(self.screen, clipped_pts, cor_radar)
