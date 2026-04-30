import math
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.modules.math.math import magnitude, from_angle

class PhysicsSystem:
    @staticmethod
    def update_entity(entity):
        entity.position[0] += entity.velocity[0]
        entity.position[1] += entity.velocity[1]
        
        if hasattr(entity, 'friction'):
            entity.velocity[0] *= entity.friction
            entity.velocity[1] *= entity.friction
        
        if hasattr(entity, 'max_speed'):
            speed = magnitude(entity.velocity)
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

    @staticmethod
    def apply_controls(entity, thrust_active, rotation_input):
        entity.rotation += rotation_input * 4
        if thrust_active:
            rad = math.radians(entity.rotation)
            thrust_vec = from_angle(rad, entity.acceleration)
            entity.velocity[0] += thrust_vec[0]
            entity.velocity[1] += thrust_vec[1]
            
    @staticmethod
    def calculate_bullet_velocity(rotation, speed):
        rad = math.radians(rotation)
        return from_angle(rad, speed)
