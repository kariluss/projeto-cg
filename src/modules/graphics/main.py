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