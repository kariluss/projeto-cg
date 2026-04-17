import random
import math
from src.modules.entities.Entity import Entity
from src.modules.math.math import Matrix

class Asteroid(Entity):
    SIZE_LARGE = 2
    SIZE_MEDIUM = 1
    SIZE_SMALL = 0
    
    SIZE_CONFIG = {
        SIZE_LARGE: {"radius": 25, "points": 20, "speed_factor": 1.0},
        SIZE_MEDIUM: {"radius": 12, "points": 50, "speed_factor": 1.5},
        SIZE_SMALL: {"radius": 6, "points": 100, "speed_factor": 2.0},
    }
    
    def __init__(self, position, size=SIZE_LARGE, velocity=None):
        super().__init__(Matrix(3, 6, [
            [1.0, 0.5, -0.5, -1.0, -0.5,  0.5],
            [0.0, 0.86, 0.86,  0.0, -0.86, -0.86],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        ]))
        
        self.position = position.copy()
        self.size = size
        self.color = (255, 255, 255)
        self.radius = self.SIZE_CONFIG[size]["radius"]
        self.points = self.SIZE_CONFIG[size]["points"]
        
        if velocity is None:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3) * self.SIZE_CONFIG[size]["speed_factor"]
            self.velocity = [speed * math.cos(angle), speed * math.sin(angle)]
        else:
            self.velocity = velocity.copy()
        
        self.alive = True
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
    
    def get_center(self):
        return self.position
    
    def get_radius(self):
        return self.radius