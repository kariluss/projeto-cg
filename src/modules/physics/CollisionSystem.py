import math

class CollisionSystem:
    """Sistema de colisão círculo-círculo usando Teorema de Pitágoras"""
    
    @staticmethod
    def check_collision(center1, radius1, center2, radius2):
        """
        Verifica se dois círculos colidem.
        
        Args:
            center1: [x, y] - centro do primeiro círculo
            radius1: float - raio do primeiro círculo
            center2: [x, y] - centro do segundo círculo
            radius2: float - raio do segundo círculo
        
        Returns:
            bool - True se há colisão, False caso contrário
        """
        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]
        
        # Distância entre os centros (Teorema de Pitágoras)
        distance = math.sqrt(dx**2 + dy**2)
        
        # Há colisão se a distância é menor que a soma dos raios
        return distance < (radius1 + radius2)
    
    @staticmethod
    def check_bullet_asteroid_collisions(bullets, asteroids):
        """
        Verifica colisões entre bullets e asteroides.
        
        Returns:
            list - tuplas (bullet_index, asteroid_index) de colisões
        """
        collisions = []
        
        for i, bullet in enumerate(bullets):
            if not bullet.alive:
                continue
            
            for j, asteroid in enumerate(asteroids):
                if not asteroid.alive:
                    continue
                
                if CollisionSystem.check_collision(
                    bullet.get_center(),
                    bullet.get_radius(),
                    asteroid.get_center(),
                    asteroid.get_radius()
                ):
                    collisions.append((i, j))
        
        return collisions
    
    @staticmethod
    def check_ship_asteroid_collisions(ship, asteroids):
        """
        Verifica colisões entre a nave e asteroides.
        
        Returns:
            bool - True se há colisão
        """
        for asteroid in asteroids:
            if not asteroid.alive:
                continue
            
            if CollisionSystem.check_collision(
                ship.get_center(),
                ship.get_radius(),
                asteroid.get_center(),
                asteroid.get_radius()
            ):
                return True
        
        return False