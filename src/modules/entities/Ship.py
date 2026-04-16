import pygame
import math
from src.modules.math.math import Matrix
from src.modules.entities.Entity import Entity
from src.modules.entities.Bullet import Bullet

class Ship(Entity):
    def __init__(self):
        super().__init__(Matrix(3, 3, [
            [  0, -10, 10],
            [-10,  10, 10],
            [  1,   1,  1]
        ]))
        self.scale = [1, 1]
        self.color = (255, 255, 255)
        
        # Física
        self.velocity = [0, 0]  # [vx, vy]
        self.acceleration = 0.5
        self.friction = 0.98  # desaceleração gradual (inércia)
        self.max_speed = 8
        
        # Tiro
        self.shoot_cooldown = 0  # frames até poder atirar novamente
        self.shoot_delay = 8  # delay mínimo entre disparos (frames)

        self.rotation_input = 0   # -1 = esquerda, 0 = neutro, 1 = direita
        self.thrust_input = False
    
    def update(self, keys):
        """Atualiza a física e estado da nave"""
        # Rotação
        self.rotation += self.rotation_input * 5
        
        # Aceleração
        if self.thrust_input:
            rad = math.radians(self.rotation)
            self.velocity[0] += self.acceleration * math.sin(rad)
            self.velocity[1] -= self.acceleration * math.cos(rad)
        
        # Aplicar friction (desaceleração gradual)
        self.velocity[0] *= self.friction
        self.velocity[1] *= self.friction
        
        # Limitar velocidade máxima
        speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if speed > self.max_speed:
            self.velocity[0] = (self.velocity[0] / speed) * self.max_speed
            self.velocity[1] = (self.velocity[1] / speed) * self.max_speed
        
        # Atualizar posição
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # Wrap-around (Pac-Man): se sair de um lado, volta do outro
        screen_width = 800  # você pode pegar de settings.py
        screen_height = 600
        
        if self.position[0] < -20:
            self.position[0] = screen_width + 20
        if self.position[0] > screen_width + 20:
            self.position[0] = -20
        if self.position[1] < -20:
            self.position[1] = screen_height + 20
        if self.position[1] > screen_height + 20:
            self.position[1] = -20
        
        # Atualizar cooldown de tiro
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def shoot(self):
        """Retorna um novo Bullet se o cooldown permitir, senão retorna None"""
        if self.shoot_cooldown <= 0:
            # A bala sai da ponta da nave
            # A nave tem 10 pixels de altura, então a ponta fica a 10 pixels na direção da rotação
            rad = math.radians(self.rotation)
            bullet_offset_x = 10 * math.sin(rad)
            bullet_offset_y = -10 * math.cos(rad)
            
            bullet_pos = [
                self.position[0] + bullet_offset_x,
                self.position[1] + bullet_offset_y
            ]
            
            self.shoot_cooldown = self.shoot_delay
            return Bullet(bullet_pos, self.rotation)
        
        return None
    
    def get_center(self):
        """Retorna o centro da nave"""
        return self.position.copy()
    
    def get_radius(self):
        """Retorna o raio de colisão da nave (aproximadamente 10 pixels)"""
        return 10