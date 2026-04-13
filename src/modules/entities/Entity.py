from src.modules.math.math import Matrix

class Entity:
    def __init__(self, model_vertices):
        self.vertices = model_vertices
        self.rotation = 0