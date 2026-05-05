# 🎯 Guia Rápido — Asteroids CG

*Documentação resumida. Para detalhes, consulte os outros arquivos.*

---

## O Que é Este Projeto?

Um **jogo arcade clássico de 1979**, implementado em Python com foco educacional em **Computação Gráfica**:

- ✅ Transformações geométricas (matrizes 3×3)
- ✅ Rasterização manual (Bresenham, Scan-line)
- ✅ Detecção de colisão
- ✅ Física computacional (inércia, atrito)
- ✅ Renderização 2D com Pygame

**Arquitetura:** Camadas estritamente separadas (Math → Physics → Graphics → Game Engine).

---

## Como Rodar?

```bash
# Instalar dependência
pip install pygame

# Executar
python -m src.main

# Ou via Docker
docker build -t asteroids-cg .
docker run -it asteroids-cg
```

**Controles:**
- Setas: Mover/Rotacionar
- Espaço: Atirar
- P: Pausar
- ESC: Sair

---

## Estrutura de Pastas

```
src/
├── main.py ..................... Ponto de entrada
├── config.py ................... Constantes (FPS, resolução)
└── modules/
    ├── core/engine.py ......... Game loop (coordena tudo)
    ├── math/math.py ........... Álgebra linear
    ├── entities/ .............. Ship, Asteroid, Bullet
    ├── physics/ ............... Movimento, colisão
    └── graphics/ .............. Renderização, rasterização
```

---

## 4 Divisões Principais do Código

### 1️⃣ **MATH** (Álgebra Linear)
**Arquivo:** `src/modules/math/math.py`

**Responsável por:**
- Multiplicação de matrizes
- Transformações: Translação, Rotação, Escala
- Operações vetoriais: Magnitude, Normalização

**Ninguém mais implementa cálculos — tudo passa por aqui!**

**Funções principais:**
```python
Matrix @ Matrix              # Multiplicação
get_translation_matrix(tx, ty)
get_rotation_matrix(angle)
get_scale_matrix(sx, sy)
magnitude(v), normalize(v)
from_angle(theta, len)
distance(p1, p2)
```

---

### 2️⃣ **PHYSICS** (Movimento e Colisão)
**Arquivos:** `src/modules/physics/PhysicsSystem.py`, `CollisionSystem.py`

**PhysicsSystem:**
- Integração numérica: `position += velocity` (Euler)
- Aplicar friction: `velocity *= 0.98`
- Limitar velocidade máxima
- Wrap-around: Tela infinita
- Aplicar controls (rotação, impulso)

**CollisionSystem:**
- Detectar colisões círculo-círculo (sem √)
- Bullet-Asteroid
- Ship-Asteroid

**Fórmula de colisão (otimizada):**
```python
dx² + dy² < (r1 + r2)²  # Sem raiz quadrada!
```

---

### 3️⃣ **GRAPHICS** (Renderização)
**Arquivos:** `src/modules/graphics/renderer.py`, `main.py`

**Pipeline por entidade:**
1. **Transform:** Aplica TRS (Translação × Rotação × Escala)
2. **Clip:** Recorta contra limites da tela (Sutherland-Hodgman)
3. **Rasterize:** Converte polígono em pixels
   - Nave: Scan-line sólida (branca)
   - Asteroides: Scan-line com textura (lua)
   - Bullets: Ponto 3×3

**Viewport transformation:** Mapeamento mundo → tela (para radar/minimapa)

---

### 4️⃣ **GAME** (Regras de Negócio)
**Arquivo:** `src/modules/game/manager.py`

**Responsável por:**
- Pontuação: +20 (grande), +50 (médio), +100 (pequeno)
- Vidas: 7 iniciais
- Dificuldade: +1 asteroide grande a cada 500 pontos
- Spawn/Respawn de asteroides
- Destruição de asteroides: Cria 2 menores (1 homing, 1 aleatório)

**Limite técnico:** Máximo 20 asteroides pequenos (performance)

---

## As 3 Entidades

| Entidade | Raio | Vidas | Pontos | Velocidade | Destruição |
|----------|------|-------|--------|-----------|-----------|
| **Ship** | 13 | 1* | — | 0-5 | Tele de volta |
| **Asteroid Grande** | 30 | — | 20 | 1-3 | 2 Médios |
| **Asteroid Médio** | 20 | — | 50 | 1.5-4.5 | 2 Pequenos |
| **Asteroid Pequeno** | 10 | — | 100 | 2-6 | Nada |
| **Bullet** | 2 | — | — | 7 (fixo) | Desaparece |

*= Nave perde uma vida ao colidir, começa com 7

---

## Fluxo de um Frame (30 FPS = 33.3 ms)

```
1. INPUT
   └─ Teclado → ship.rotation_input, ship.thrust_input

2. PHYSICS UPDATE (~3 ms)
   ├─ apply_controls()      [rotação + impulso]
   ├─ update_all()          [position += velocity; velocity *= friction]
   └─ apply_wrap_around()   [tela infinita]

3. BULLET/ASTEROID LOGIC (~2 ms)
   ├─ Bullets: distance_traveled += speed
   └─ Asteroids: respawn se offscreen

4. COLLISION DETECTION (~5 ms)
   ├─ Bullet-Asteroid → handle_asteroid_destruction()
   └─ Ship-Asteroid → lives--; respawn ou game_over

5. DIFFICULTY UPDATE
   └─ Se score aumentou, spawn novos asteroides

6. RENDERING (~15-20 ms)
   ├─ Transform TRS
   ├─ Clip (Sutherland-Hodgman)
   ├─ Rasterize (Scan-line)
   └─ Draw UI + Radar

Total: ~25-30 ms ✓
```

---

## Matemática em 60 Segundos

### Transformações (Matrizes 3×3)

Ponto 2D $(x, y)$ representado como $\begin{pmatrix} x \\ y \\ 1 \end{pmatrix}$

**Translação:**
$$\begin{pmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ 1 \end{pmatrix} = \begin{pmatrix} x + t_x \\ y + t_y \\ 1 \end{pmatrix}$$

**Rotação:**
$$\begin{pmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

**Escala:**
$$\begin{pmatrix} s_x & 0 & 0 \\ 0 & s_y & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

**Composição (ordem inversa!):**
$$\text{Resultado} = T \cdot R \cdot S \cdot \text{vértices}$$

### Vetores

| Operação | Fórmula |
|----------|---------|
| Magnitude | $\|\vec{v}\| = \sqrt{v_x^2 + v_y^2}$ |
| Normalizar | $\hat{v} = \vec{v} / \|\vec{v}\|$ |
| Distância | $d = \sqrt{(p2_x - p1_x)^2 + (p2_y - p1_y)^2}$ |
| Ângulo → Vetor | $\vec{d}(\theta) = [\sin\theta, -\cos\theta]$ |

### Física

| Conceito | Fórmula |
|----------|---------|
| Movimento | $p_{t+1} = p_t + v_t$ |
| Atrito | $v_{t+1} = v_t \times 0.98$ |
| Aceleração | $v_{t+1} = v_t + a$ |
| Max Speed | $\text{se } \|\vec{v}\| > v_{max}: \vec{v} = \text{normalize}(\vec{v}) \times v_{max}$ |

### Colisão (sem √)

```python
# Colisão se:
dx² + dy² < (r1 + r2)²
```

---

## Arquitetura em 1 Diagrama

```
Engine (game loop)
    ↓
    ├─ PhysicsSystem ────┐
    │                    ↓
    ├─ CollisionSystem   Entidades (Ship, Asteroid, Bullet)
    │                    ↑
    ├─ Renderer ─────────┘
    │
    └─ GameManager
    
Todos usam: Math (matrizes, vetores)
```

---

## Configurações Importantes

**config.py:**
- `SCREEN_WIDTH = 800`, `SCREEN_HEIGHT = 600`
- `FPS = 30`
- `MAX_SMALL_ASTEROIDS = 20` (limite de performance)
- `ASTEROID_ROTATION = True` (desabilitar economiza CPU)

---

## Performance (30 FPS)

| Operação | Tempo | Notas |
|----------|-------|-------|
| Transformações | ~2-3 ms | Matrizes 3×3 |
| Colisão | ~5 ms | Sem √ |
| Rasterização | ~15-20 ms | **Maior custo** |
| Clipping | ~1-2 ms | Sutherland-Hodgman |
| Atualização Física | ~3 ms | Integração Euler |

**Otimizações implementadas:**
- ✅ Comparação colisão sem raiz quadrada
- ✅ Cache de world points (reutiliza transformações)
- ✅ Limite MAX_SMALL_ASTEROIDS
- ✅ Matriz radar pre-extraída

---

## Conceitos de CG Aprendidos

- [x] Matrizes homogêneas 3×3
- [x] Transformações TRS
- [x] Composição de matrizes
- [x] Bresenham (linhas)
- [x] Scan-line (polígonos)
- [x] Sutherland-Hodgman (clipping)
- [x] Mapeamento UV (texturas)
- [x] Viewport transformation
- [x] Detecção de colisão
- [x] Integração numérica (Euler)

---

## Para Entender Mais

| Tópico | Arquivo |
|--------|---------|
| **Visão completa** | `COMPLETE_DOCUMENTATION.md` |
| **Arquitetura visual** | `ARCHITECTURE_DIAGRAM.md` |
| **Matemática detalhada** | `MATHEMATICAL_GUIDE.md` |
| **Especificação técnica** | `system-spec.md` |
| **Especificação de jogo** | `prod-spec.md` |

---

## Cheat Sheet — Operações Comuns

### Criar uma matriz

```python
from src.modules.math.math import *

T = get_translation_matrix(100, 200)
R = get_rotation_matrix(math.radians(45))
S = get_scale_matrix(20, 20)
transform = T @ R @ S
```

### Transformar vértices

```python
world_vertices = transform @ entity.vertices
points = [(world_vertices.data[0][i], world_vertices.data[1][i]) 
          for i in range(world_vertices.cols)]
```

### Verificar colisão

```python
from src.modules.physics.CollisionSystem import CollisionSystem

if CollisionSystem.check_collision(c1, r1, c2, r2):
    # Houve colisão!
    pass
```

### Calcular velocidade de projétil

```python
from src.modules.physics.PhysicsSystem import PhysicsSystem

velocity = PhysicsSystem.calculate_bullet_velocity(ship.rotation, bullet_speed)
```

### Atualizar física

```python
from src.modules.physics.PhysicsSystem import PhysicsSystem

PhysicsSystem.apply_controls(ship, thrust, rotation_input)
PhysicsSystem.update_all([ship, bullets, asteroids])
PhysicsSystem.apply_wrap_around(ship)
```

---

## FAQ Rápido

**P: Por que usar matrizes homogêneas 3×3 para 2D?**
R: Permite representar translação como multiplicação matricial (não adição). Unifica todas transformações.

**P: Por que não usar raiz quadrada na colisão?**
R: Porque $\sqrt{...}$ é lenta. Se $a < b$, então $a^2 < b^2$ para positivos.

**P: Como a nave não sai disparada?**
R: Aplicar `friction = 0.98` reduz velocidade 2% a cada frame. + `max_speed = 5.0`.

**P: Por que ordem inversa na composição TRS?**
R: $T \cdot R \cdot S \cdot v$ aplica primeiro $S$, depois $R$, depois $T$ (lê da direita para esquerda).

**P: O que é "tela infinita"?**
R: Se sair de um lado, reaparece do outro. Implementado com `apply_wrap_around()`.

**P: Por que asteroides têm 3 tamanhos?**
R: Aumenta progressividade: grande (fácil) → médio → pequeno (difícil, mais pontos).

**P: Qual é o limite de asteroides?**
R: Máximo 12 grandes. Máximo 20 pequenos (performance). Médios ilimitados.

---

## Resumo em 1 Sentença

**Asteroids é um jogo arcade que implementa transformações geométricas (matrizes), física computacional (inércia/atrito), detecção de colisão otimizada, e rasterização manual de polígonos — tudo em camadas bem separadas, com Math como base.**

---

*Última atualização: 2026*
