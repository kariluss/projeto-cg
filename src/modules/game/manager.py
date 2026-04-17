import random
import math
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, MAX_SMALL_ASTEROIDS
from src.modules.entities.Asteroid import Asteroid

class GameManager:
    
    def __init__(self):
        self.score = 0
        self.lives = 7
        self.wave = 1
        self.target_large_asteroids = 0
        self.asteroids_destroyed_this_wave = 0

    def start_new_wave(self, asteroids_list):
        self.target_large_asteroids = 3 + self.wave
        self.asteroids_destroyed_this_wave = 0
        
        for _ in range(self.target_large_asteroids):
            pos = self._get_random_edge_position()
            asteroids_list.append(Asteroid(pos, Asteroid.SIZE_LARGE))

    def _get_random_edge_position(self, margin=40):
        if random.choice([True, False]):
            x = random.choice([random.uniform(-margin, -margin/2), random.uniform(SCREEN_WIDTH + margin/2, SCREEN_WIDTH + margin)])
            y = random.uniform(0, SCREEN_HEIGHT)
        else:
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.choice([random.uniform(-margin, -margin/2), random.uniform(SCREEN_HEIGHT + margin/2, SCREEN_HEIGHT + margin)])
        return [x, y]

    def handle_offscreen_asteroid(self, asteroid, asteroids_list):
        asteroid.alive = False
        
        current_small = sum(1 for a in asteroids_list if a.size == Asteroid.SIZE_SMALL)
        if current_small >= MAX_SMALL_ASTEROIDS:
            return

        current_large = sum(1 for a in asteroids_list if a.size == Asteroid.SIZE_LARGE)
        size = Asteroid.SIZE_LARGE if current_large < self.target_large_asteroids else Asteroid.SIZE_MEDIUM
        
        pos = self._get_random_edge_position()
        replacement = Asteroid(pos, size)
        
        # Velocidade baixa para respawns
        low_speed = random.uniform(0.5, 1.2)
        angle = random.uniform(0, 2 * math.pi)
        replacement.velocity = [low_speed * math.cos(angle), low_speed * math.sin(angle)]
        
        asteroids_list.append(replacement)

    def handle_asteroid_destruction(self, asteroid, asteroids_list, ship_position):
        self.score += asteroid.points
        asteroid.alive = False
        
        if asteroid.size == Asteroid.SIZE_LARGE:
            self.asteroids_destroyed_this_wave += 1
            
        if asteroid.size > Asteroid.SIZE_SMALL:
            new_size = asteroid.size - 1
            
            dx = ship_position[0] - asteroid.position[0]
            dy = ship_position[1] - asteroid.position[1]
            h_angle = math.atan2(dy, dx)
            asteroids_list.append(Asteroid(asteroid.position.copy(), new_size, [1.0 * math.cos(h_angle), 1.0 * math.sin(h_angle)]))
            
            r_angle = random.uniform(0, 2 * math.pi)
            speed = asteroid.SIZE_CONFIG[new_size]["speed_factor"] * 2.0
            asteroids_list.append(Asteroid(asteroid.position.copy(), new_size, [speed * math.cos(r_angle), speed * math.sin(r_angle)]))

    def check_wave_completion(self, asteroids_list):
        if len(asteroids_list) == 0:
            self.wave += 1
            return True
        return False
