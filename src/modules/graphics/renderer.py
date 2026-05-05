import pygame
import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, YELLOW, BLACK
from src.modules.graphics.main import (
    bresenham, scanline_fill, setPixel, sutherland_hodgman_clip, scanline_texture,
    midpoint_circle, midpoint_ellipse, flood_fill, scanline_gradient_fill, cohen_sutherland_clip
)
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

        # Semente para lasers aleatórios no menu (para consistência entre frames se desejado)
        self._lasers = []
        import random
        for _ in range(20):
            self._lasers.append((
                random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            ))
        
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

    def draw_start_menu(self, font, frame_count):
        """Desenha o Menu Inicial Animado com vários elementos dinâmicos."""
        # 1. Fundo com Gradiente (Scanline Gradient) - Animado
        bg_points = [(0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)]
        
        # Cores que variam com o tempo para efeito de pulsação
        intensity = abs(math.sin(frame_count * 0.02)) * 30
        bg_colors = [
            (int(intensity), 0, 50 + int(intensity)), 
            (int(intensity), 0, 50 + int(intensity)), 
            (0, 0, int(20 + intensity)), 
            (0, 0, int(20 + intensity))
        ]
        scanline_gradient_fill(self.screen, bg_points, bg_colors)

        # 2. Planeta com rotação e pulsação de escala
        planet_xc, planet_yc = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        planet_base_r = 100
        planet_r = planet_base_r + int(10 * math.sin(frame_count * 0.03))
        
        midpoint_circle(self.screen, planet_xc, planet_yc, planet_r, (0, 200, 0))
        flood_fill(self.screen, planet_xc, planet_yc, (0, 0, 0, 255), (0, 100, 0))

        # 3. Anéis planetários com rotação
        rotation_angle = (frame_count * 2) % 360
        
        # Anéis ellipse estáticos (base)
        midpoint_ellipse(self.screen, planet_xc, planet_yc, 180, 40, (200, 200, 100))
        midpoint_ellipse(self.screen, planet_xc, planet_yc, 200, 50, (150, 150, 50))
        
        # Anéis dinâmicos que pulsam
        ring_scale = 220 + int(30 * math.sin(frame_count * 0.04))
        midpoint_ellipse(self.screen, planet_xc, planet_yc, ring_scale, 30, 
                        (int(100 + 100 * math.sin(frame_count * 0.05)), 150, 200))

        # 4. Asteroides orbitando ao redor do planeta (NOVO)
        num_asteroids = 5
        orbit_radius = 250
        for i in range(num_asteroids):
            angle = (frame_count * 1.5 + (360 / num_asteroids) * i) * (math.pi / 180)
            ast_x = planet_xc + orbit_radius * math.cos(angle)
            ast_y = planet_yc + orbit_radius * math.sin(angle)
            
            ast_size = 15 + int(5 * math.sin(frame_count * 1.5 + i))
            midpoint_circle(self.screen, int(ast_x), int(ast_y), ast_size, (200, 100, 100))
            
            # Pequeno preenchimento para o asteroide
            try:
                flood_fill(self.screen, int(ast_x), int(ast_y), (0, 0, 0, 255), (150, 50, 50))
            except:
                pass  # Evita erros se clicar fora da tela

        # 5. Lasers de Fundo com Cohen-Sutherland (ANIMADO)
        clip_margin = 150
        xmin, ymin = SCREEN_WIDTH // 2 - clip_margin, SCREEN_HEIGHT // 2 - clip_margin
        xmax, ymax = SCREEN_WIDTH // 2 + clip_margin, SCREEN_HEIGHT // 2 + clip_margin
        
        pygame.draw.rect(self.screen, WHITE, (xmin, ymin, xmax-xmin, ymax-ymin), 1)

        for idx, (x0, y0, x1, y1, color) in enumerate(self._lasers):
            # Lasers se movem suavemente
            offset = int(20 * math.sin(frame_count * 0.05 + idx * 0.3))
            x0_anim = x0 + offset
            x1_anim = x1 + offset
            
            clipped = cohen_sutherland_clip(x0_anim, y0, x1_anim, y1, xmin, ymin, xmax, ymax)
            if clipped:
                cx0, cy0, cx1, cy1 = clipped
                # Cor pulsante
                r = int(color[0] + 50 * math.sin(frame_count * 0.06 + idx * 0.2))
                g = int(color[1] + 50 * math.sin(frame_count * 0.06 + idx * 0.3))
                b = int(color[2] + 50 * math.sin(frame_count * 0.06 + idx * 0.4))
                r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
                bresenham(self.screen, int(cx0), int(cy0), int(cx1), int(cy1), (r, g, b))

        # 6. Efeito de Stars de Fundo (NOVO)
        import random
        random.seed(42)  # Seed fixo para consistência
        for _ in range(30):
            star_x = random.randint(0, SCREEN_WIDTH)
            star_y = random.randint(0, SCREEN_HEIGHT)
            star_brightness = int(200 + 55 * math.sin(frame_count * 0.02 + star_x * 0.01))
            star_brightness = max(0, min(255, star_brightness))
            setPixel(self.screen, star_x, star_y, (star_brightness, star_brightness, star_brightness))

        # 7. UI Text com animações
        title_text = font.render("ASTEROIDS CG", True, WHITE)
        title_y = 50 + int(5 * math.sin(frame_count * 0.04))  # Pulsação vertical
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, title_y))
        
        # Texto de início com piscada
        alpha_start = int(255 * (0.5 + 0.5 * math.sin(frame_count * 0.05)))
        if alpha_start > 100:  # Só desenha quando brilhante o suficiente
            start_text = font.render("Press ENTER to Start", True, YELLOW)
            self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT - 100))
        
        # Texto de sair fixo
        quit_text = font.render("Press ESC to Quit", True, RED)
        self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT - 60))

        # 8. Indicador de "ready" com animação de escala
        scale = 1.0 + 0.2 * math.sin(frame_count * 0.06)
        ready_size = int(24 * scale)
        ready_font = pygame.font.Font(None, ready_size)
        ready_text = ready_font.render("●", True, (0, 255, 0))
        self.screen.blit(ready_text, (SCREEN_WIDTH // 2 - ready_text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))