from src.modules.math.math import Matrix
from src.modules.entities.Entity import Entity

class Ship(Entity):
    def __init__(self):
        super().__init__(Matrix(3, 14, [
            [ 0.0,  0.1,  0.4,  0.9,  0.6,  0.3,  0.1,  0.0, -0.1, -0.3, -0.6, -0.9, -0.4, -0.1],
            [-1.0, -0.7, -0.2,  0.5,  0.5,  0.3,  0.8,  0.6,  0.8,  0.3,  0.5,  0.5, -0.2, -0.7],
            [ 1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0]
        ]))
        
        self.color = (255, 255, 255)
        self.radius = 13
        
        self.velocity = [0.0, 0.0]
        self.acceleration = 0.2
        self.friction = 0.98
        self.max_speed = 5.0
        
        self.rotation_input = 0
        self.thrust_input = False
        self.shoot_cooldown = 0
        self.shoot_delay = 8
        
    def get_center(self):
        return self.position
    
    def get_radius(self):
        return self.radius