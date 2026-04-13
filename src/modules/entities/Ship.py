from src.modules.math.math import Matrix
from src.modules.entities.Entity import Entity

class Ship(Entity):
    def __init__(self):
        super().__init__(Matrix(3, 3, [
            [  0, -10, 10],
            [-10,  10, 10],
            [  1,   1,  1]
        ]))
        self.scale = [1, 1]
        self.color = (255, 255, 255)
        