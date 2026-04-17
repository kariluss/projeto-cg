from src.modules.entities.Entity import Entity
from src.modules.math.math import Matrix

class Bullet(Entity):
    def __init__(self, position, rotation, speed=7):
        super().__init__(Matrix(3, 1, [[0.0], [0.0], [1.0]]))
        
        self.position = position.copy()
        self.rotation = rotation
        self.velocity = [0.0, 0.0]
        self.speed = speed
        self.max_distance = 400
        self.distance_traveled = 0
        self.alive = True
        self.color = (255, 255, 255)
        self.radius = 2

    def get_center(self):
        return self.position
    
    def get_radius(self):
        return self.radius