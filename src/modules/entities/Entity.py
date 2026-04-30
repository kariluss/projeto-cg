from src.modules.math.math import Matrix

class Entity:
    def __init__(self, model_vertices):
        self.vertices = model_vertices
        self.position = [0.0, 0.0]
        self.velocity = [0.0, 0.0]
        self.rotation = 0.0
        self.alive = True