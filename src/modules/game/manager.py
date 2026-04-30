import random
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, MAX_SMALL_ASTEROIDS
from src.modules.entities.Asteroid import Asteroid
from src.modules.math.math import vector_from_points, random_direction

class GameManager:
    
    # Quantos pontos equivalem a +1 no alvo de asteroides grandes
    SCORE_PER_DIFFICULTY_STEP = 500
    BASE_LARGE_ASTEROIDS = 4
    MAX_LARGE_ASTEROIDS = 12

    def __init__(self):
        self.score = 0
        self.lives = 7

    def _target_large_count(self):
        """Calcula quantos asteroides grandes devem existir simultaneamente com base no score atual."""
        steps = self.score // self.SCORE_PER_DIFFICULTY_STEP
        return min(self.BASE_LARGE_ASTEROIDS + steps, self.MAX_LARGE_ASTEROIDS)

    def initialize(self, asteroids_list):
        """Popula a tela com o número inicial de asteroides grandes para iniciar o jogo."""
        for _ in range(self.BASE_LARGE_ASTEROIDS):
            pos = self._get_random_edge_position()
            asteroids_list.append(Asteroid(pos, Asteroid.SIZE_LARGE))

    def update_difficulty(self, asteroids_list):
        """Garante que o número de asteroides grandes na tela reflita a dificuldade atual do score."""
        current_large = sum(1 for a in asteroids_list if a.size == Asteroid.SIZE_LARGE)
        target = self._target_large_count()
        if current_large < target:
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
        """Respawna o asteroide na borda oposta com o MESMO tamanho, preservando o progresso do jogador."""
        asteroid.alive = False

        # Pequenos fora da tela não são repostos: o jogador limpou, ele some.
        if asteroid.size == Asteroid.SIZE_SMALL:
            return

        # Grandes e Médios voltam com seu próprio tamanho em posição e direção aleatória,
        # simulando um universo maior do que a janela.
        pos = self._get_random_edge_position()
        replacement = Asteroid(pos, asteroid.size)
        low_speed = random.uniform(0.5, 1.2)
        replacement.velocity = random_direction(low_speed)
        asteroids_list.append(replacement)

    def handle_asteroid_destruction(self, asteroid, asteroids_list, ship_position):
        self.score += asteroid.points
        asteroid.alive = False
            
        if asteroid.size > Asteroid.SIZE_SMALL:
            new_size = asteroid.size - 1
            
            # Checar limite de performance: Small Asteroids
            if new_size == Asteroid.SIZE_SMALL:
                current_small = sum(1 for a in asteroids_list if a.size == Asteroid.SIZE_SMALL)
                # Mais 2 serão criados, garante que não explodirá o threshold bruscamente
                if current_small + 2 > MAX_SMALL_ASTEROIDS:
                    return

            # Asteroid 1: Direção guiada para a nave (homing)
            homing_velocity = vector_from_points(asteroid.position, ship_position, speed=1.0)
            asteroids_list.append(Asteroid(asteroid.position.copy(), new_size, homing_velocity))
            
            # Asteroid 2: Direção aleatória
            speed = asteroid.SIZE_CONFIG[new_size]["speed_factor"] * 2.0
            asteroids_list.append(Asteroid(asteroid.position.copy(), new_size, random_direction(speed)))


