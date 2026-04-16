import random
import math
from src.modules.entities.Entity import Entity
from src.modules.math.math import Matrix

class Asteroid(Entity):
    # Tamanhos: GRANDE = 2, MÉDIO = 1, PEQUENO = 0
    SIZE_LARGE = 2
    SIZE_MEDIUM = 1
    SIZE_SMALL = 0
    
    # Configurações por tamanho
    SIZE_CONFIG = {
        SIZE_LARGE: {"radius": 25, "points": 20, "speed_factor": 1.0},
        SIZE_MEDIUM: {"radius": 12, "points": 50, "speed_factor": 1.5},
        SIZE_SMALL: {"radius": 6, "points": 100, "speed_factor": 2.0},
    }
    
    def __init__(self, position, size=SIZE_LARGE, velocity=None):
        # Cria um polígono simples (hexágono) como representação visual
        # Vamos usar um triângulo para simplificar
        super().__init__(Matrix(3, 3, [
            [  10,   0, -10],
            [   0,  10,  10],
            [   1,   1,   1]
        ]))
        
        self.position = position.copy()  # [x, y]
        self.size = size
        self.color = (255, 255, 255)
        self.radius = self.SIZE_CONFIG[size]["radius"]
        self.points = self.SIZE_CONFIG[size]["points"]
        
        # Velocidade aleatória ou definida
        if velocity is None:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3) * self.SIZE_CONFIG[size]["speed_factor"]
            self.velocity = [speed * math.cos(angle), speed * math.sin(angle)]
        else:
            self.velocity = velocity.copy()
        
        self.alive = True
        self.rotation = random.uniform(0, 360)  # rotação visual
        self.rotation_speed = random.uniform(-5, 5)  # velocidade de rotação
    
    def update(self):
        """Atualiza a posição e rotação do asteroide"""
        if not self.alive:
            return
        
        # Atualizar posição
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Atualizar rotação (só visual, não afeta colisão)
        self.rotation += self.rotation_speed
        
        # Se sair da tela, desaparece (diferente da nave que faz wrap-around)
        screen_width = 800
        screen_height = 600
        if (self.position[0] < -50 or self.position[0] > screen_width + 50 or
            self.position[1] < -50 or self.position[1] > screen_height + 50):
            self.alive = False
    
    def split(self):
        """
        Quando destruído, retorna dois asteroides menores.
        Asteroide Grande -> 2 Médios
        Asteroide Médio -> 2 Pequenos
        Asteroide Pequeno -> Nada (é destruído completamente)
        """
        if self.size == self.SIZE_SMALL:
            return []
        
        new_size = self.size - 1
        
        # Cria dois asteroides menores com velocidades diferentes
        angle1 = math.atan2(self.velocity[1], self.velocity[0])
        angle2 = angle1 + math.pi
        
        speed = 2 + random.uniform(0, 2)
        
        new_asteroids = [
            Asteroid(
                self.position.copy(),
                new_size,
                [speed * math.cos(angle1), speed * math.sin(angle1)]
            ),
            Asteroid(
                self.position.copy(),
                new_size,
                [speed * math.cos(angle2), speed * math.sin(angle2)]
            )
        ]
        
        return new_asteroids
    
    def draw(self, screen, m_world):
        """
        Desenha o asteroide usando a matriz de transformação do mundo.
        É bem similar ao que você faz com a nave.
        """
        # Aplicar transformação
        world_vertices = m_world @ self.vertices
        
        # Extrair pontos
        pontos_render = []
        for i in range(3):
            x = int(round(world_vertices.data[0][i]))
            y = int(round(world_vertices.data[1][i]))
            pontos_render.append((x, y))
        
        # Desenhar usando scanline_fill (você importa do seu módulo graphics)
        from src.modules.graphics.main import scanline_fill
        scanline_fill(screen, pontos_render, self.color)
    
    def get_center(self):
        """Retorna o centro do asteroide"""
        return self.position.copy()
    
    def get_radius(self):
        """Retorna o raio de colisão"""
        return self.radius