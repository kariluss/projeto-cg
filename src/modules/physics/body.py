class PhysicsBody:
    def __init__(self, x, y, friction=0.98, angular_friction=0.90):
        self.position = [int(x), int(y)]
        self.velocity = [0.0, 0.0]
        self.rotation = 0.0  # Em graus
        self.angular_velocity = 0.0
        self.friction = friction
        self.angular_friction = angular_friction

    def update(self):
        # 1. Aplica atrito
        self.velocity[0] *= self.friction
        self.velocity[1] *= self.friction
        self.angular_velocity *= self.angular_friction

        # 2. Atualiza posição e rotação
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.rotation += self.angular_velocity