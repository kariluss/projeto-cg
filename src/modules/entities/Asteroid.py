import random
from src.modules.math.math import random_direction
from src.modules.entities.Entity import Entity
from src.modules.math.math import Matrix

class Asteroid(Entity):
    SIZE_LARGE = 2
    SIZE_MEDIUM = 1
    SIZE_SMALL = 0
    
    SIZE_CONFIG = {
        SIZE_LARGE: {"radius": 30, "points": 20, "speed_factor": 1.0},
        SIZE_MEDIUM: {"radius": 20, "points": 50, "speed_factor": 1.5},
        SIZE_SMALL: {"radius": 10, "points": 100, "speed_factor": 2.0},
    }
    
    def __init__(self, position, size=SIZE_LARGE, velocity=None):
        # Matriz base do modelo (-1 a 1)
        # Modelagem de asteroide hardcoded: polígono de 7 lados levemente imperfeito e assimétrico
        model_data = [
            [ 1.0,  0.5, -0.4, -0.9, -0.6,  0.2,  0.8],
            [ 0.1,  0.9,  0.8, -0.2, -0.8, -1.0, -0.6],
            [ 1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0]
        ]
        super().__init__(Matrix(3, 7, model_data))
        
        # Mapeamento UV Automático baseado nos vértices do modelo!
        # Como o modelo vai de -1 a 1, normalizamos para 0 a 1 para pegar a textura.
        self.uvs = []
        for col in range(7):
            x = model_data[0][col]
            y = model_data[1][col]
            u = (x + 1.0) / 2.0
            v = (y + 1.0) / 2.0
            self.uvs.append((u, v))
            
        self.position = position.copy()
        self.size = size
        self.color = (255, 255, 255)
        self.radius = self.SIZE_CONFIG[size]["radius"]
        self.points = self.SIZE_CONFIG[size]["points"]
        
        if velocity is None:
            speed = random.uniform(1, 3) * self.SIZE_CONFIG[size]["speed_factor"]
            self.velocity = random_direction(speed)
        else:
            self.velocity = velocity.copy()
        
        self.alive = True
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
    
    def get_center(self):
        return self.position
    
    def get_radius(self):
        return self.radius