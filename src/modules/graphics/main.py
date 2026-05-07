import pygame

def setPixel(superficie: pygame.Surface, x: int, y: int, cor: tuple):
    """Set a pixel on the surface.
    Args:
        superficie (pygame.Surface): surface to draw on
        x (int): x coordinate
        y (int): y coordinate
        cor (tuple): color of the pixel
    Returns:
        None
    """
    superficie.set_at((x, y), cor)
    
def bresenham(superficie: pygame.Surface, x0: int, y0: int, x1: int, y1: int, cor: tuple):
    """Draw a line on the surface using Bresenham's algorithm.
    Args:
        superficie (pygame.Surface): surface to draw on
        x0 (int): x coordinate of the first point
        y0 (int): y coordinate of the first point
        x1 (int): x coordinate of the second point
        y1 (int): y coordinate of the second point
        cor (tuple): color of the line
    Returns:
        None
    """
    # Flags para transformações
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    ystep = 1
    if dy < 0:
        ystep = -1
        dy = -dy

    # Bresenham clássico
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x0
    y = y0

    while x <= x1:
        if steep:
            setPixel(superficie, y, x, cor)
        else:
            setPixel(superficie, x, y, cor)

        if d <= 0:
            d += incE
        else:
            d += incNE
            y += ystep

        x += 1

def dda(superficie: pygame.Surface, x0: int, y0: int, x1: int, y1: int, cor: tuple):
    """Draw a line on the surface using DDA's algorithm.
    Args:
        superficie (pygame.Surface): surface to draw on
        x0 (int): x coordinate of the first point
        y0 (int): y coordinate of the first point
        x1 (int): x coordinate of the second point
        y1 (int): y coordinate of the second point
        cor (tuple): color of the line
    Returns:
        None
    """
    dx = x1 - x0
    dy = y1 - y0

    passos = max(abs(dx), abs(dy))

    if passos == 0:
        setPixel(superficie, x0, y0, cor)
        return

    x_inc = dx / passos
    y_inc = dy / passos

    x = x0
    y = y0

    for _ in range(passos + 1):
        setPixel(superficie, round(x), round(y), cor)
        x += x_inc
        y += y_inc
        
def scanline_fill(superficie: pygame.Surface, pontos: list, cor_preenchimento: tuple):
    """Fill a polygon on the surface using scanline algorithm.
    Args:
        superficie (pygame.Surface): surface to draw on
        pontos (list): list of points of the polygon
        cor_preenchimento (tuple): color of the fill
    Returns:
        None
    """
    # Encontra Y mínimo e máximo
    ys = [p[1] for p in pontos]
    y_min = min(ys)
    y_max = max(ys)

    n = len(pontos)

    for y in range(y_min, y_max):
        intersecoes_x = []

        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]

            # Ignora arestas horizontais
            if y0 == y1:
                continue

            # Garante y0 < y1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0

            # Regra Ymin ≤ y < Ymax
            if y < y0 or y >= y1:
                continue

            # Calcula interseção
            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersecoes_x.append(x)

        # Ordena interseções
        intersecoes_x.sort()

        # Preenche entre pares
        for i in range(0, len(intersecoes_x), 2):
            if i + 1 < len(intersecoes_x):
                x_inicio = int(round(intersecoes_x[i]))
                x_fim = int(round(intersecoes_x[i + 1]))

                for x in range(x_inicio, x_fim + 1):
                    setPixel(superficie, x, y, cor_preenchimento)

def midpoint_circle(superficie: pygame.Surface, xc: int, yc: int, r: int, cor: tuple):
    """Draw a circle on the surface using Midpoint Circle algorithm."""
    x = 0
    y = r
    d = 1 - r

    def _draw_circle_points(s, xc, yc, x, y, cor):
        setPixel(s, xc + x, yc + y, cor)
        setPixel(s, xc - x, yc + y, cor)
        setPixel(s, xc + x, yc - y, cor)
        setPixel(s, xc - x, yc - y, cor)
        setPixel(s, xc + y, yc + x, cor)
        setPixel(s, xc - y, yc + x, cor)
        setPixel(s, xc + y, yc - x, cor)
        setPixel(s, xc - y, yc - x, cor)

    _draw_circle_points(superficie, xc, yc, x, y, cor)
    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        _draw_circle_points(superficie, xc, yc, x, y, cor)

def midpoint_ellipse(superficie: pygame.Surface, xc: int, yc: int, rx: int, ry: int, cor: tuple):
    """Draw an ellipse on the surface using Midpoint Ellipse algorithm."""
    x = 0
    y = ry
    
    # Region 1
    d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y

    def _draw_ellipse_points(s, xc, yc, x, y, cor):
        setPixel(s, xc + x, yc + y, cor)
        setPixel(s, xc - x, yc + y, cor)
        setPixel(s, xc + x, yc - y, cor)
        setPixel(s, xc - x, yc - y, cor)

    while dx < dy:
        _draw_ellipse_points(superficie, xc, yc, x, y, cor)
        if d1 < 0:
            x += 1
            dx += 2 * ry * ry
            d1 += dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx += 2 * ry * ry
            dy -= 2 * rx * rx
            d1 += dx - dy + (ry * ry)

    # Region 2
    d2 = ((ry * ry) * ((x + 0.5) ** 2)) + ((rx * rx) * ((y - 1) ** 2)) - (rx * rx * ry * ry)
    while y >= 0:
        _draw_ellipse_points(superficie, xc, yc, x, y, cor)
        if d2 > 0:
            y -= 1
            dy -= 2 * rx * rx
            d2 += (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx += 2 * ry * ry
            dy -= 2 * rx * rx
            d2 += dx - dy + (rx * rx)

def flood_fill(superficie: pygame.Surface, x: int, y: int, target_color: tuple, fill_color: tuple):
    """Fill a closed area using iterative stack-based Flood Fill algorithm."""
    if target_color == fill_color:
        return
    
    width, height = superficie.get_size()
    stack = [(x, y)]
    
    # Check if starting point is actually the target color
    try:
        if superficie.get_at((x, y))[:3] != target_color[:3]:
            return
    except IndexError:
        return

    visited = set()

    while stack:
        curr_x, curr_y = stack.pop()
        
        if (curr_x, curr_y) in visited:
            continue
        
        if 0 <= curr_x < width and 0 <= curr_y < height:
            if superficie.get_at((curr_x, curr_y))[:3] == target_color[:3]:
                setPixel(superficie, curr_x, curr_y, fill_color)
                visited.add((curr_x, curr_y))
                stack.append((curr_x + 1, curr_y))
                stack.append((curr_x - 1, curr_y))
                stack.append((curr_x, curr_y + 1))
                stack.append((curr_x, curr_y - 1))

def scanline_gradient_fill(superficie: pygame.Surface, pontos: list, cores: list):
    """Fill a polygon with a smooth gradient interpolated between vertex colors."""
    if not pontos or len(pontos) < 3:
        return
        
    ys = [p[1] for p in pontos]
    y_min, y_max = int(min(ys)), int(max(ys))
    n = len(pontos)

    for y in range(y_min, y_max):
        if y < 0 or y >= superficie.get_height():
            continue

        inter = []
        for i in range(n):
            p0, p1 = pontos[i], pontos[(i + 1) % n]
            c0, c1 = cores[i], cores[(i + 1) % n]

            if p0[1] == p1[1]: continue
            if p0[1] > p1[1]:
                p0, p1 = p1, p0
                c0, c1 = c1, c0

            if y < p0[1] or y >= p1[1]: continue

            t = (y - p0[1]) / (p1[1] - p0[1])
            x = p0[0] + t * (p1[0] - p0[0])
            
            # Interpolate color at the edge
            r = c0[0] + t * (c1[0] - c0[0])
            g = c0[1] + t * (c1[1] - c0[1])
            b = c0[2] + t * (c1[2] - c0[2])
            inter.append((x, (r, g, b)))

        inter.sort(key=lambda i: i[0])

        for i in range(0, len(inter), 2):
            if i + 1 >= len(inter): continue
            
            x_start, c_start = inter[i]
            x_end, c_end = inter[i + 1]

            if x_start == x_end: continue

            for x in range(int(round(x_start)), int(round(x_end)) + 1):
                if x < 0 or x >= superficie.get_width(): continue
                
                t_x = (x - x_start) / (x_end - x_start)
                r = c_start[0] + t_x * (c_end[0] - c_start[0])
                g = c_start[1] + t_x * (c_end[1] - c_start[1])
                b = c_start[2] + t_x * (c_end[2] - c_start[2])
                setPixel(superficie, x, y, (int(r), int(g), int(b)))

def cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    """Clip a line against a rectangular window using Cohen-Sutherland algorithm."""
    INSIDE = 0  # 0000
    LEFT = 1    # 0001
    RIGHT = 2   # 0010
    BOTTOM = 4  # 0100
    TOP = 8     # 1000

    def compute_code(x, y):
        code = INSIDE
        if x < xmin: code |= LEFT
        elif x > xmax: code |= RIGHT
        if y < ymin: code |= BOTTOM
        elif y > ymax: code |= TOP
        return code

    code0 = compute_code(x0, y0)
    code1 = compute_code(x1, y1)
    accept = False

    while True:
        if code0 == 0 and code1 == 0:
            accept = True
            break
        elif (code0 & code1) != 0:
            break
        else:
            x, y = 0.0, 0.0
            code_out = code0 if code0 != 0 else code1
            
            if code_out & TOP:
                x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                y = ymax
            elif code_out & BOTTOM:
                x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                y = ymin
            elif code_out & RIGHT:
                y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
                x = xmax
            elif code_out & LEFT:
                y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
                x = xmin
            
            if code_out == code0:
                x0, y0 = x, y
                code0 = compute_code(x0, y0)
            else:
                x1, y1 = x, y
                code1 = compute_code(x1, y1)

    if accept:
        return (x0, y0, x1, y1)
    else:
        return None
                    
def sutherland_hodgman_clip(poligono, xmin, ymin, xmax, ymax):
    """
    Recorta um polígono convexo contra um retângulo (Viewport) usando Sutherland-Hodgman.
    poligono: lista de tuplas (x, y)
    Retorna a nova lista de vértices recortados.
    """
    def clip_edge(pontos, borda):
        novos_pontos = []
        if not pontos: return novos_pontos
        
        for i in range(len(pontos)):
            p_atual = pontos[i]
            p_anterior = pontos[i - 1]
            
            # Funções para checar se o ponto está dentro e calcular interseção
            if borda == 'esquerda':
                dentro_atual = p_atual[0] >= xmin
                dentro_anterior = p_anterior[0] >= xmin
                intersec = lambda p1, p2: (xmin, p1[1] + (p2[1] - p1[1]) * (xmin - p1[0]) / (p2[0] - p1[0]) if p2[0] != p1[0] else p1[1])
            elif borda == 'direita':
                dentro_atual = p_atual[0] <= xmax
                dentro_anterior = p_anterior[0] <= xmax
                intersec = lambda p1, p2: (xmax, p1[1] + (p2[1] - p1[1]) * (xmax - p1[0]) / (p2[0] - p1[0]) if p2[0] != p1[0] else p1[1])
            elif borda == 'topo':
                dentro_atual = p_atual[1] >= ymin
                dentro_anterior = p_anterior[1] >= ymin
                intersec = lambda p1, p2: (p1[0] + (p2[0] - p1[0]) * (ymin - p1[1]) / (p2[1] - p1[1]) if p2[1] != p1[1] else p1[0], ymin)
            elif borda == 'fundo':
                dentro_atual = p_atual[1] <= ymax
                dentro_anterior = p_anterior[1] <= ymax
                intersec = lambda p1, p2: (p1[0] + (p2[0] - p1[0]) * (ymax - p1[1]) / (p2[1] - p1[1]) if p2[1] != p1[1] else p1[0], ymax)

            # Lógica principal de inserção de vértices
            if dentro_atual:
                if not dentro_anterior:
                    novos_pontos.append(intersec(p_anterior, p_atual))
                novos_pontos.append(p_atual)
            elif dentro_anterior:
                novos_pontos.append(intersec(p_anterior, p_atual))
                
        return novos_pontos

    # Passar o polígono pelas 4 bordas do retângulo clippador
    p = poligono
    for borda in ['esquerda', 'direita', 'topo', 'fundo']:
        p = clip_edge(p, borda)
        
    return [(int(round(x)), int(round(y))) for x, y in p]

def desenhar_poligono_bordas(superficie, pontos, cor):
    """ Desenha apenas as bordas do polígono (Wireframe) """
    if not pontos or len(pontos) < 3: return
    n = len(pontos)
    for i in range(n):
        x0, y0 = pontos[i]
        x1, y1 = pontos[(i + 1) % n]
        bresenham(superficie, int(x0), int(y0), int(x1), int(y1), cor)

def scanline_texture(superficie: pygame.Surface, pontos: list, uvs: list, textura: pygame.Surface):
    """Preenche um polígono com uma imagem usando interpolação bilinear de UVs."""
    if not pontos or len(pontos) < 3:
        return
        
    tex_w, tex_h = textura.get_width(), textura.get_height()
    ys = [p[1] for p in pontos]
    y_min, y_max = int(min(ys)), int(max(ys))
    n = len(pontos)

    for y in range(y_min, y_max):
        # Proteção para não desenhar fora da tela verticalmente
        if y < 0 or y >= superficie.get_height():
            continue

        inter = []
        for i in range(n):
            x0, y0 = pontos[i]
            x1, y1 = pontos[(i + 1) % n]
            u0, v0 = uvs[i]
            u1, v1 = uvs[(i + 1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                u0, v0, u1, v1 = u1, v1, u0, v0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)
            x = x0 + t * (x1 - x0)
            u = u0 + t * (u1 - u0)
            v = v0 + t * (v1 - v0)
            inter.append((x, u, v))

        inter.sort(key=lambda i: i[0])

        for i in range(0, len(inter), 2):
            if i + 1 >= len(inter):
                continue

            x_start, u_start, v_start = inter[i]
            x_end, u_end, v_end = inter[i + 1]

            if x_start == x_end:
                continue

            for x in range(int(x_start), int(x_end) + 1):
                # Proteção para não desenhar fora da tela horizontalmente
                if x < 0 or x >= superficie.get_width():
                    continue

                t = (x - x_start) / (x_end - x_start)
                u = u_start + t * (u_end - u_start)
                v = v_start + t * (v_end - v_start)

                tx = int(u * (tex_w - 1))
                ty = int(v * (tex_h - 1))

                if 0 <= tx < tex_w and 0 <= ty < tex_h:
                    cor = textura.get_at((tx, ty))
                    setPixel(superficie, x, y, cor)