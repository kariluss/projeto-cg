# 🏗️ Arquitetura Visual — Asteroids CG

## Estrutura de Diretórios vs Responsabilidades

```
projeto-cg/
│
├── src/
│   ├── main.py ........................ Ponto de entrada (importa GameEngine)
│   │
│   ├── config.py ...................... Constantes globais (FPS, resolução, limites)
│   │
│   ├── modules/
│   │   │
│   │   ├── core/
│   │   │   └── engine.py .............. 🎮 GAME ENGINE
│   │   │                              Orquestra todo o sistema
│   │   │                              - Game Loop
│   │   │                              - State Management
│   │   │                              - Event Processing
│   │   │                              - System Coordination
│   │   │
│   │   ├── math/
│   │   │   └── math.py ............... 🧮 MATH MODULE (Base de tudo)
│   │   │                              - Matrix class
│   │   │                              - TRS Transformations
│   │   │                              - Vector operations
│   │   │                              Nenhuma outra camada faz cálculos próprios!
│   │   │
│   │   ├── entities/
│   │   │   ├── Entity.py ............. 📦 Base class (dados puros)
│   │   │   ├── Ship.py ............... 👽 Nave do jogador
│   │   │   ├── Asteroid.py ........... 🪨 Asteroides (3 tamanhos)
│   │   │   └── Bullet.py ............. 💥 Projéteis
│   │   │                              Sem lógica própria, sem Pygame!
│   │   │
│   │   ├── physics/
│   │   │   ├── PhysicsSystem.py ...... 🌌 PHYSICS SYSTEM
│   │   │   │                           - Movimento (integração Euler)
│   │   │   │                           - Inércia e atrito
│   │   │   │                           - Wrap-around
│   │   │   │                           - Controles de entrada
│   │   │   │
│   │   │   └── CollisionSystem.py .... 💫 COLLISION SYSTEM
│   │   │                               - Detecção círculo-círculo
│   │   │                               - Bullet-Asteroid
│   │   │                               - Ship-Asteroid
│   │   │
│   │   ├── graphics/
│   │   │   ├── main.py ............... 🎨 RASTERIZATION ALGORITHMS
│   │   │   │                           - Bresenham (linhas)
│   │   │   │                           - Scan-line (polígonos)
│   │   │   │                           - Sutherland-Hodgman (clipping)
│   │   │   │                           - Texture mapping
│   │   │   │
│   │   │   └── renderer.py ........... 🖼️ RENDERER
│   │   │                               - TRS Pipeline
│   │   │                               - Viewport management
│   │   │                               - Radar (minimapa)
│   │   │                               - Entity drawing
│   │   │
│   │   └── game/
│   │       └── manager.py ............ 🎯 GAME MANAGER
│   │                                   - Score e pontuação
│   │                                   - Vidas e game states
│   │                                   - Progressão de dificuldade
│   │                                   - Spawning de asteroides
│   │
│   └── [outros arquivos de suporte]
│
├── doc/
│   ├── system-spec.md ................ 📄 Especificação técnica
│   ├── prod-spec.md .................. 📄 Especificação de produto
│   └── COMPLETE_DOCUMENTATION.md ..... 📄 DOCUMENTAÇÃO COMPLETA ⭐
│
├── assets/
│   ├── moon-8bit-30p.png ............ 🌙 Textura asteroide grande
│   ├── moon-8bit-20p.png ............ 🌙 Textura asteroide médio
│   └── moon-8bit-10p.png ............ 🌙 Textura asteroide pequeno
│
├── README.md ......................... 📖 Guia básico
├── dockerfile ........................ 🐳 Docker
└── main.py ........................... ▶️ Script para executar
```

---

## Fluxo de Dados — Quem Chama Quem?

```
┌────────────────────────────────────────────────────────────────┐
│                      main.py                                   │
│              (Ponto de entrada)                                │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│                    GameEngine                                  │
│               (engine.py - Core)                              │
│                                                                │
│  Responsável por:                                              │
│  ✓ Game Loop                                                   │
│  ✓ State Management (RUNNING, PAUSED, GAME_OVER)             │
│  ✓ Orquestrar Sistemas                                        │
│  ✓ Inicializar tudo                                          │
└──────────────┬────────────────────────────────────────────────┘
               │
        ┌──────┼──────────┬──────────────────┬──────────────┐
        │      │          │                  │              │
        ▼      ▼          ▼                  ▼              ▼
      INPUT PHYSICS    COLLISION        RENDERING      GAME_MGR
        │    System     System          (Renderer)      (Manager)
        │      │          │               │              │
        │      │          │               │              │
        │      │   ┌──────▼──────┐        │              │
        │      └──►│ Entity       │        │              │
        │          │ Updates:    │        │              │
        │          │ • position  │        │              │
        │          │ • velocity  │        │              │
        │          │ • rotation  │        │              │
        │          └──────┬──────┘        │              │
        │                 │               │              │
        │                 │      ┌────────▼─────────┐    │
        │                 │      │  Collision       │    │
        │                 │      │  Detection       │    │
        │                 │      │  • Bullet-Ast   │    │
        │                 │      │  • Ship-Ast     │    │
        │                 │      └────────┬────────┘    │
        │                 │               │             │
        │                 │       ┌───────▼─────────┐   │
        │                 │       │  Rendering      │   │
        │                 │       │  • Transform    │   │
        │                 │       │  • Rasterize   │   │
        │                 │       │  • Draw        │   │
        │                 │       └────────┬────────┘   │
        │                 │               │             │
        │                 │      ┌────────▼─────────┐   │
        │                 └─────►│  Game Manager   │   │
        │                        │  • Score        │   │
        │                        │  • Lives        │   │
        │                        │  • Difficulty   │   │
        │                        └────────┬────────┘   │
        │                                 │             │
        │                           ┌─────▼─────────┐   │
        │                           │  Entities:    │   │
        │                           │  • Ship       │   │
        │                           │  • Asteroids  │   │
        │                           │  • Bullets    │   │
        │                           └───────────────┘   │
        │                                              │
        └──────────────────────────────────────────────┘
                            │
                            ▼
                    All data flows through MATH
                    (Transformations, Collisions)
```

---

## Dependências Entre Módulos

```
Níveis de dependência (bottom-up, base → topo):

[NÍVEL 0 — Base]
├─ Math (math.py) — Ninguém depende dele para implementar math
│
[NÍVEL 1 — Dados]
├─ Entities (Entity.py, Ship.py, Asteroid.py, Bullet.py)
│  └─ Dependem de: Math (para tipos básicos)
│
[NÍVEL 2 — Sistemas]
├─ PhysicsSystem
│  └─ Dependem de: Math, Entities, config
│
├─ CollisionSystem
│  └─ Dependem de: Math, Entities
│
├─ Renderer
│  └─ Dependem de: Math, Entities, Graphics algorithms
│
├─ GameManager
│  └─ Dependem de: Math, Entities, config
│
[NÍVEL 3 — Orquestração]
└─ GameEngine (core/engine.py)
   └─ Dependem de: PhysicsSystem, CollisionSystem, Renderer, GameManager, Entities
```

**Regra de Ouro:** Cada módulo só conhece os módulos abaixo dele na hierarquia.

---

## Fluxo de um Frame (30 FPS)

```
FRAME START (33.3 ms budget)
│
├─ [1] EVENT PROCESSING ........................ ~1 ms
│  └─ Input: teclado → ship.rotation_input, ship.thrust_input
│
├─ [2] PHYSICS UPDATE .......................... ~3 ms
│  ├─ PhysicsSystem.apply_controls(ship)
│  │  └─ Atualiza rotation, adiciona impulso à velocidade
│  ├─ PhysicsSystem.update_all(entities)
│  │  └─ position += velocity; velocity *= friction
│  └─ PhysicsSystem.apply_wrap_around(entities)
│     └─ Teleporta se sair da tela
│
├─ [3] ENTITY-SPECIFIC UPDATES ................. ~2 ms
│  ├─ Bullets: distance_traveled += speed
│  ├─ Asteroids offscreen: respawn ou remove
│  └─ Ship: update cooldown, invincibility timer
│
├─ [4] SHOOTING ................................ ~0.5 ms
│  └─ Se espaço pressionado: cria Bullet
│
├─ [5] CLEANUP .................................. ~0.5 ms
│  ├─ bullets = [b for b in bullets if b.alive]
│  └─ asteroids = [a for a in asteroids if a.alive]
│
├─ [6] COLLISION DETECTION ..................... ~5 ms
│  ├─ CollisionSystem.check_bullet_asteroid_collisions()
│  │  └─ Para cada colisão:
│  │     GameManager.handle_asteroid_destruction()
│  │     ├─ score += asteroid.points
│  │     ├─ Se médio/grande: cria 2 menores (1 homing, 1 random)
│  │     └─ Respeita limite MAX_SMALL_ASTEROIDS
│  │
│  └─ CollisionSystem.check_ship_asteroid_collisions()
│     └─ Se colisão:
│        ├─ lives -= 1
│        ├─ Se lives > 0: respawn ship, clear bullets
│        └─ Se lives == 0: state = "GAME_OVER"
│
├─ [7] DIFFICULTY UPDATE ........................ ~0.5 ms
│  └─ GameManager.update_difficulty()
│     ├─ Calcula target = 4 + (score / 500)
│     └─ Se precisa mais asteroides, spawn novo
│
├─ [8] RENDERING ................................ ~15-20 ms (maior custo)
│  ├─ screen.fill(BLACK)
│  ├─ Renderer.draw_world_entities()
│  │  ├─ Para cada entidade:
│  │  │  ├─ Calcula T @ R @ S @ vertices (transformation pipeline)
│  │  │  ├─ Aplica clipping (Sutherland-Hodgman)
│  │  │  ├─ Rasteriza com Scan-line
│  │  │  │  ├─ Naves: preenchimento sólido
│  │  │  │  ├─ Asteroides: textura com UV mapping
│  │  │  │  └─ Bullets: ponto 3×3
│  │  │  └─ Cachea world points para radar
│  │  │
│  │  └─ Renderer.draw_radar()
│  │     ├─ Transforma mundo → viewport radar
│  │     ├─ Reutiliza world points cached
│  │     └─ Desenha nave (red) e asteroides (yellow)
│  │
│  └─ Draw UI
│     ├─ Score e Lives
│     └─ Pause / Game Over text
│
├─ [9] DISPLAY ................................. ~0.5 ms
│  └─ pygame.display.flip()
│
└─ TOTAL: ~25-30 ms ✓ (Mantém 30 FPS estável)
```

---

## Ciclo de Vida de Entidades

### Ship (Nave)

```
[SPAWN at center]
   │
   ├─ physics: apply_controls() → rotation, impulso
   ├─ physics: update_entity() → movement
   ├─ physics: apply_wrap_around()
   ├─ rendering: transform TRS
   ├─ collision: check_ship_asteroid()
   │
   ├─ [COLLISION]
   │  └─ lives -= 1
   │     ├─ Se lives > 0: respawn + invincibility (1.5s)
   │     └─ Se lives == 0: game_over
   │
   └─ [GAME END] → despawned
```

### Asteroid (Asteroide Grande → Médio → Pequeno)

```
[SPAWN at random edge]
   │
   ├─ physics: update_entity() → movement, rotation
   ├─ physics: apply_wrap_around()
   │  └─ Fora da tela? → respawn no oposto
   ├─ rendering: transform + texture
   ├─ collision: check_bullet_asteroid()
   │
   ├─ [HIT BY BULLET]
   │  ├─ score += points
   │  ├─ Se SIZE_LARGE ou SIZE_MEDIUM:
   │  │  ├─ Create 2 × SIZE_MEDIUM (ou SIZE_SMALL)
   │  │  ├─ Um em direção à nave (homing)
   │  │  └─ Um em direção aleatória
   │  └─ Se SIZE_SMALL: destruído completamente
   │
   └─ [DEAD] → removed from list
```

### Bullet (Projétil)

```
[SPAWN from ship nose]
   │
   ├─ physics: calculate_bullet_velocity()
   ├─ physics: update_entity() → straight line
   ├─ rendering: transform (ponto)
   │
   ├─ distance_traveled += speed
   │  ├─ Se > max_distance (400): mark dead
   │  └─ Se fora da tela (com margem): mark dead
   │
   ├─ collision: check_bullet_asteroid()
   │  ├─ [HIT] → trigger asteroid destruction
   │  └─ [MISS] → continua voando
   │
   └─ [DEAD] → removed from list
```

---

## Transformação de Vértices — Passo a Passo

### Exemplo: Renderizar um Asteroide

```
1. ENTITY STATE
   asteroid.vertices = Matrix(3, 7, [...])  // Modelo [-1, 1]
   asteroid.position = [400, 300]
   asteroid.rotation = 45.0  // graus
   asteroid.radius = 20

2. CONVERTER PARA RADIANOS
   angle_rad = radians(45) ≈ 0.785 rad

3. CRIAR MATRIZES DE TRANSFORMAÇÃO
   T = get_translation_matrix(400, 300)
   R = get_rotation_matrix(0.785)
   S = get_scale_matrix(20, 20)

4. COMPOR TRANSFORMAÇÃO (TRS)
   transform = T @ R @ S
   // Ordem importa! Escala primeiro, depois rotação, depois translação

5. APLICAR AOS VÉRTICES
   world_vertices = transform @ asteroid.vertices
   // Resultado: 3×7 matrix com pontos no espaço do mundo

6. EXTRAIR PONTOS COMO LISTA DE TUPLAS
   points = [
       (world_vertices.data[0][0], world_vertices.data[1][0]),
       (world_vertices.data[0][1], world_vertices.data[1][1]),
       ...,
       (world_vertices.data[0][6], world_vertices.data[1][6])
   ]

7. CLIPPING (Sutherland-Hodgman contra viewport)
   clipped_points = sutherland_hodgman_clip(points, 0, 0, 800, 600)
   // Remova vértices fora da tela, calcule intersecções nas bordas

8. RASTERIZAÇÃO (Scan-line com textura)
   scanline_texture(screen, clipped_points, asteroid.uvs, texture)
   // Preencha o polígono linha por linha, mapeando textura

9. RESULTADO
   Asteroide desenhado na tela! ✓
```

---

## Esquema de Pontuação e Progressão

```
SCORE MECHANICS
└─ Destruir Asteroide Grande    = +20 pontos
├─ Destruir Asteroide Médio     = +50 pontos
└─ Destruir Asteroide Pequeno   = +100 pontos

DIFFICULTY SCALING
└─ target_large_count = min(4 + ⌊score / 500⌋, 12)

Exemplos:
├─ Score 0     → 4 large asteroids
├─ Score 500   → 5 large asteroids
├─ Score 1000  → 6 large asteroids
├─ Score 5000  → 14, mas capped at 12
└─ (Máximo sempre 12)

SPAWNING RULES
└─ Asteroides grandes aparecem em posições aleatórias
   nas bordas da tela a cada frame se count < target

SMALL ASTEROID LIMIT
└─ Máximo 20 pequenos simultâneos (performance)
   └─ Se destruir asteroide que criaria >20 pequenos,
      os novos não são criados
```

---

## Matriz de Responsabilidades

```
┌─────────────────────┬──────────────┬──────────────┬──────────────┐
│ Operação            │ Implementado │ Camada       │ Arquivo      │
├─────────────────────┼──────────────┼──────────────┼──────────────┤
│ Multiplicar matrizes│ Matrix.__@__ │ Math         │ math.py      │
│ Rotação             │ get_rotation │ Math         │ math.py      │
│ Translação          │ get_translat │ Math         │ math.py      │
│ Escala              │ get_scale    │ Math         │ math.py      │
│ Magnitude vetor     │ magnitude()  │ Math         │ math.py      │
│ Normalizar          │ normalize()  │ Math         │ math.py      │
│ Direção aleatória   │ random_dir   │ Math         │ math.py      │
│                     │              │              │              │
│ Posição entidade    │ position[x,y]│ Entities     │ Entity.py    │
│ Velocidade          │ velocity     │ Entities     │ Entity.py    │
│ Vértices modelo     │ vertices     │ Entities     │ Entity.py    │
│ Rotação de nave     │ rotation     │ Entities     │ Ship.py      │
│ Tamanho asteroide   │ size         │ Entities     │ Asteroid.py  │
│                     │              │              │              │
│ Aplicar controls    │ apply_contr  │ Physics      │ PhysicsSystem│
│ Atualizar posição   │ update_entit │ Physics      │ PhysicsSystem│
│ Aplicar wrap-around │ apply_wrap   │ Physics      │ PhysicsSystem│
│ Calcular velocidade │ calculate_bu │ Physics      │ PhysicsSystem│
│                     │              │              │              │
│ Detectar colisão    │ check_collid │ Collision    │ Collision    │
│ Círculo-círculo     │ check_collid │ Collision    │ System.py    │
│                     │              │              │              │
│ Transformação TRS   │ transform @  │ Graphics     │ renderer.py  │
│ Clipping            │ sutherland   │ Graphics     │ main.py      │
│ Rasterização        │ scanline_    │ Graphics     │ main.py      │
│ Textura mapping     │ scanline_tex │ Graphics     │ main.py      │
│                     │              │              │              │
│ Pontos/vidas        │ score/lives  │ Game Mgr     │ manager.py   │
│ Destruição ast.     │ handle_ast   │ Game Mgr     │ manager.py   │
│ Dificuldade         │ update_diff  │ Game Mgr     │ manager.py   │
│ Respawn offscreen   │ handle_offsc │ Game Mgr     │ manager.py   │
└─────────────────────┴──────────────┴──────────────┴──────────────┘
```

---

## Checklist de Conceitos CG Implementados

- [x] **Matrizes Homogêneas 3×3** para transformações 2D
- [x] **Transformações TRS** (Translação, Rotação, Escala)
- [x] **Composição de matrizes** para pipelines complexas
- [x] **Algoritmo de Bresenham** para rasterização de linhas
- [x] **Algoritmo de Scan-line** para preenchimento de polígonos
- [x] **Clipping de polígonos** (Sutherland-Hodgman)
- [x] **Mapeamento de texturas** com coordenadas UV
- [x] **Viewport transformation** (mundo → tela)
- [x] **Detecção de colisão** círculo-círculo
- [x] **Integração numérica** (Euler simples)
- [x] **Simulação de inércia** com atrito
- [x] **Wrap-around** (tela infinita)
- [x] **Transformação de pontos** através de matrizes

---

## Estrutura de Dados Principais

```python
# Entity Base
{
    vertices: Matrix(3, n),  # n vértices no modelo
    position: [x, y],        # Posição no mundo
    velocity: [vx, vy],      # Velocidade
    rotation: float,         # Ângulo em graus
    alive: bool              # Ativo?
}

# Ship
{
    + acceleration: 0.2
    + friction: 0.98
    + max_speed: 5.0
    + rotation_input: -1/0/1
    + thrust_input: bool
    + shoot_cooldown: int
    + invincible: bool
    + invincible_time: float
}

# Asteroid
{
    + size: 0/1/2  (SMALL/MEDIUM/LARGE)
    + rotation_speed: float
    + uvs: [(u, v)] × n
    + radius: 10/20/30
    + points: 100/50/20
}

# Bullet
{
    + speed: 7
    + max_distance: 400
    + distance_traveled: float
}

# Matrix
{
    rows: int
    cols: int
    data: [[...], [...], ...]
}
```

---

Este documento complementa a documentação técnica completa e oferece uma visão visual e estruturada de como o projeto se organiza.
