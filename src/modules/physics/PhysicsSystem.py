import math
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class PhysicsSystem:
    @staticmethod
    def update_entity(entity):
        entity.position[0] += entity.velocity[0]
        entity.position[1] += entity.velocity[1]
        
        if hasattr(entity, 'friction'):
            entity.velocity[0] *= entity.friction
            entity.velocity[1] *= entity.friction
        
        if hasattr(entity, 'max_speed'):
            speed = math.sqrt(entity.velocity[0]**2 + entity.velocity[1]**2)
            if speed > entity.max_speed:
                entity.velocity[0] = (entity.velocity[0] / speed) * entity.max_speed
                entity.velocity[1] = (entity.velocity[1] / speed) * entity.max_speed
        
    @staticmethod
    def apply_wrap_around(entity):
        margin = 20
        if hasattr(entity, 'radius'):
            margin = entity.radius + 5
            
        if entity.position[0] < -margin:
            entity.position[0] = SCREEN_WIDTH + margin
        elif entity.position[0] > SCREEN_WIDTH + margin:
            entity.position[0] = -margin
            
        if entity.position[1] < -margin:
            entity.position[1] = SCREEN_HEIGHT + margin
        elif entity.position[1] > SCREEN_HEIGHT + margin:
            entity.position[1] = -margin

    @staticmethod
    def update_all(entities):
        for entity in entities:
            PhysicsSystem.update_entity(entity)
