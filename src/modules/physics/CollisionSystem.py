class CollisionSystem:
    """Sistema de colisão círculo-círculo usando Matemática do sistema"""
    
    @staticmethod
    def check_collision(center1, radius1, center2, radius2):
        """
        Verifica se dois círculos colidem.
        Usa distância ao quadrado para evitar o custo de sqrt.
        
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
        r_sum = radius1 + radius2
        return (dx * dx + dy * dy) < (r_sum * r_sum)
    
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