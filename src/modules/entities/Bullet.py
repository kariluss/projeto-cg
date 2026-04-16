import math
from src.modules.entities.Entity import Entity
from src.modules.math.math import Matrix

class Bullet(Entity):
    def __init__(self, position, rotation, speed=7):
        # Um bullet é apenas um ponto (representado por uma matriz 3x1)
        super().__init__(Matrix(3, 1, [[0], [0], [1]]))
        
        self.position = position.copy()  # [x, y]
        self.rotation = rotation  # ângulo da nave no momento do tiro
        self.speed = speed
        self.max_distance = 400  # distância máxima antes de desaparecer
        self.distance_traveled = 0  # quanto já viajou
        self.color = (255, 255, 255)
        self.alive = True
    
    def update(self):
        """Move o bullet em linha reta na direção da rotação da nave"""
        if not self.alive:
            return
        
        # Converte rotação em radianos
        rad = math.radians(self.rotation)
        
        # Calcula a velocidade em x e y
        # A nave aponta para cima (eixo Y negativo), então:
        # x aumenta quando rotation é 90°, y diminui quando rotation é 0°
        vx = self.speed * math.sin(rad)
        vy = -self.speed * math.cos(rad)
        
        # Atualiza a posição
        self.position[0] += vx
        self.position[1] += vy
        
        # Atualiza a distância viajada
        self.distance_traveled += self.speed
        
        # Se viajou muito, desaparece
        if self.distance_traveled >= self.max_distance:
            self.alive = False
    
    def draw(self, screen):
        """Desenha o bullet como um pequeno ponto"""
        x = int(round(self.position[0]))
        y = int(round(self.position[1]))
        
        # Verifica se está dentro dos limites da tela
        if 0 <= x < screen.get_width() and 0 <= y < screen.get_height():
            # Desenha um pequeno círculo (3x3 pixels)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    screen.set_at((x + dx, y + dy), self.color)
    
    def get_center(self):
        """Retorna o centro (posição) do bullet"""
        return self.position
    
    def get_radius(self):
        """Retorna o raio de colisão do bullet (aproximadamente 2 pixels)"""
        return 2