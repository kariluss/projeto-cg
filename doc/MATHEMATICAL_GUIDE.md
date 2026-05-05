# 🧮 Guia Matemático Detalhado — Asteroids CG

## Introdução

Este documento detalha **todos os conceitos matemáticos** utilizados no projeto Asteroids, desde álgebra linear até física computacional. Cada conceito é acompanhado por:

- **Definição formal** (notação matemática)
- **Implementação em código** (Python)
- **Aplicação prática** no projeto
- **Exemplos numéricos** concretos

---

## Parte 1: Matrizes e Transformações Geométricas

### 1.1 Matrizes — Conceito Base

Uma **matriz** é um arranjo rectangular de números organizados em linhas e colunas.

$$M_{m \times n} = \begin{pmatrix} 
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{pmatrix}$$

**Notação:** $M_{ij}$ denota o elemento na linha $i$, coluna $j$.

#### Implementação em Código

```python
class Matrix:
    def __init__(self, rows, cols, data=None):
        self.rows = rows
        self.cols = cols
        self.data = data or [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Acessar elemento
    def get(self, i, j):
        return self.data[i][j]
    
    # Alterar elemento
    def set(self, i, j, value):
        self.data[i][j] = value
```

---

### 1.2 Multiplicação de Matrizes

**Definição:** Se $A$ é $m \times p$ e $B$ é $p \times n$, então $C = A \times B$ é $m \times n$ onde:

$$C_{ij} = \sum_{k=1}^{p} A_{ik} \cdot B_{kj}$$

**Propriedade crucial:** $A \times B \neq B \times A$ (não-comutativa!)

#### Implementação em Código

```python
def __matmul__(self, other):
    """Multiplicação matricial usando operador @"""
    if self.cols != other.rows:
        raise ValueError('Dimensões incompatíveis')
    
    result = Matrix(self.rows, other.cols)
    for i in range(self.rows):
        for j in range(other.cols):
            for k in range(self.cols):
                result.data[i][j] += self.data[i][k] * other.data[k][j]
    return result
```

#### Exemplo Numérico

$$\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix} \times \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix} = \begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix}$$

**Cálculo:**
- $C_{11} = 1 \cdot 5 + 2 \cdot 7 = 5 + 14 = 19$ ✓
- $C_{12} = 1 \cdot 6 + 2 \cdot 8 = 6 + 16 = 22$ ✓
- $C_{21} = 3 \cdot 5 + 4 \cdot 7 = 15 + 28 = 43$ ✓
- $C_{22} = 3 \cdot 6 + 4 \cdot 8 = 18 + 32 = 50$ ✓

---

### 1.3 Coordenadas Homogêneas

**O grande segredo da Computação Gráfica:** Representar pontos 2D como vetores 3D!

Um ponto $(x, y)$ é representado como:

$$\vec{p} = \begin{pmatrix} x \\ y \\ 1 \end{pmatrix}$$

**Por quê?** Permite representar translação como multiplicação matricial.

#### Sem coordenadas homogêneas

Translação é uma **operação especial**:
$$p' = p + t \quad \text{(adição, não multiplicação)}$$

#### Com coordenadas homogêneas

Translação é apenas uma **multiplicação matricial**:
$$p' = T \cdot p \quad \text{(multiplicação)}$$

Isso unifica todas as transformações 2D!

---

### 1.4 Transformações Geométricas 2D

#### 1.4.1 Identidade

$$I = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

Aplicar identidade não altera nada: $I \cdot p = p$.

```python
def get_identity_matrix(n=3):
    return Matrix(n, n, [[1 if i == j else 0 for j in range(n)] for i in range(n)])
```

---

#### 1.4.2 Translação

**Definição:** Mover um ponto $(x, y)$ por deslocamento $(t_x, t_y)$.

$$T(t_x, t_y) = \begin{pmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{pmatrix}$$

**Aplicação:**
$$\begin{pmatrix} x' \\ y' \\ 1 \end{pmatrix} = \begin{pmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ 1 \end{pmatrix} = \begin{pmatrix} x + t_x \\ y + t_y \\ 1 \end{pmatrix}$$

```python
def get_translation_matrix(tx, ty):
    return Matrix(3, 3, [[1, 0, tx], [0, 1, ty], [0, 0, 1]])
```

**Exemplo:** Mover ponto $(2, 3)$ por $(5, -1)$

$$T(5, -1) = \begin{pmatrix} 1 & 0 & 5 \\ 0 & 1 & -1 \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} 2 \\ 3 \\ 1 \end{pmatrix} = \begin{pmatrix} 7 \\ 2 \\ 1 \end{pmatrix}$$

Resultado: $(7, 2)$ ✓

---

#### 1.4.3 Rotação

**Definição:** Girar um ponto em torno da origem por ângulo $\theta$ (radianos).

$$R(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

**Derivação geométrica:**
- Ponto original em coordenadas polares: $r = \sqrt{x^2 + y^2}$, $\alpha = \arctan(y/x)$
- Após rotação por $\theta$: novo ângulo é $\alpha + \theta$
- Conversão para cartesianas: $x' = r \cos(\alpha + \theta)$, $y' = r \sin(\alpha + \theta)$
- Aplicar identidades trigonométricas → matriz acima

```python
def get_rotation_matrix(angle):
    # angle em radianos
    c, s = math.cos(angle), math.sin(angle)
    return Matrix(3, 3, [[c, -s, 0], [s, c, 0], [0, 0, 1]])
```

**Exemplo:** Girar ponto $(1, 0)$ por $90°$ (π/2 radianos)

$$\cos(90°) = 0, \quad \sin(90°) = 1$$

$$R(90°) = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \\ 1 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \\ 1 \end{pmatrix}$$

Resultado: $(0, 1)$ — ponto girado 90° ✓

---

#### 1.4.4 Escala

**Definição:** Multiplicar coordenadas por fatores $s_x$ e $s_y$.

$$S(s_x, s_y) = \begin{pmatrix} s_x & 0 & 0 \\ 0 & s_y & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

**Aplicação:**
$$\begin{pmatrix} x' \\ y' \\ 1 \end{pmatrix} = \begin{pmatrix} s_x \cdot x \\ s_y \cdot y \\ 1 \end{pmatrix}$$

```python
def get_scale_matrix(sx, sy):
    return Matrix(3, 3, [[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
```

**Exemplo:** Escalar ponto $(2, 3)$ por fator $(2, 0.5)$

$$S(2, 0.5) = \begin{pmatrix} 2 & 0 & 0 \\ 0 & 0.5 & 0 \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} 2 \\ 3 \\ 1 \end{pmatrix} = \begin{pmatrix} 4 \\ 1.5 \\ 1 \end{pmatrix}$$

Resultado: $(4, 1.5)$ ✓

---

### 1.5 Composição de Transformações (Muito Importante!)

**Problema:** Como aplicar múltiplas transformações?

**Solução:** Multiplicar as matrizes na ordem **inversa** de aplicação.

Se queremos aplicar:
1. Escala
2. Rotação
3. Translação

A matriz composta é:
$$M = T \cdot R \cdot S$$

(Note: T, R, S de trás para frente!)

#### Por quê a ordem inversa?

Porque **multiplicação de matrizes é associativa**:

$$(T \cdot R \cdot S) \cdot v = T \cdot (R \cdot (S \cdot v))$$

Lemos da direita para esquerda:
1. Primeiro: $S \cdot v$ (escala)
2. Depois: $R \cdot (...)$ (rotação)
3. Finalmente: $T \cdot (...)$ (translação)

#### Exemplo Prático no Asteroids

Renderizar um asteroide com:
- Escala: raio = 20
- Rotação: 45°
- Translação: posição $(400, 300)$

```python
T = get_translation_matrix(400, 300)
R = get_rotation_matrix(math.radians(45))
S = get_scale_matrix(20, 20)

# Composição na ordem INVERSA
transform = T @ R @ S

# Aplicar aos vértices
world_vertices = transform @ asteroid.vertices
```

**Visualmente:**
```
Vértice no modelo: [-0.5, 0.3, 1]  (no espaço [-1, 1])
       │
       ▼ (multiplicar por S)
Escala: [-10, 6, 1]
       │
       ▼ (multiplicar por R)
Rotação: [-5.3, 9.4, 1]
       │
       ▼ (multiplicar por T)
Mundo: [394.7, 309.4, 1]
```

---

### 1.6 Matriz Transposta

**Definição:** Inverter linhas e colunas.

$$A^T_{ij} = A_{ji}$$

**Propriedade em CG:** Usar para passar de "vértices em linhas" para "vértices em colunas".

```python
@property
def T(self):
    t = [list(t) for t in list(zip(*self.data))]
    return Matrix(len(t), len(t[0]), t)
```

**Exemplo:**
$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix} \quad \Rightarrow \quad A^T = \begin{pmatrix} 1 & 4 \\ 2 & 5 \\ 3 & 6 \end{pmatrix}$$

**No Asteroids:**
```python
# Vértices como linhas (3 × n):
vertices = Matrix(3, 7, [[x1, x2, ...], [y1, y2, ...], [1, 1, ...]])

# Para aplicar transformação, precisa ser coluna (3 × 1 por vértice)
# Mas multiplicamos: transform @ vertices (3×3 @ 3×7 = 3×7)
# Internamente, cada coluna é tratada como um vértice

# Outra abordagem (menos eficiente):
# vertices_transposed = vertices.T  # 7 × 3
# world_verts = (transform @ vertices_transposed.T).T
```

---

## Parte 2: Álgebra Vetorial

### 2.1 Vetores 2D

Um **vetor** em 2D é um par de números que representa direção e magnitude.

$$\vec{v} = \begin{pmatrix} v_x \\ v_y \end{pmatrix}$$

**Interpretações:**
- **Deslocamento:** Mover de um ponto para outro
- **Velocidade:** Taxa de mudança de posição
- **Direção:** Aponta para onde algo está viajando

---

### 2.2 Magnitude (Norma)

A **magnitude** de um vetor é seu "comprimento".

$$\|\vec{v}\| = \sqrt{v_x^2 + v_y^2}$$

**Derivação:** Teorema de Pitágoras no plano 2D.

```python
def magnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2)
```

**Exemplo:**
$$\vec{v} = \begin{pmatrix} 3 \\ 4 \end{pmatrix} \quad \Rightarrow \quad \|\vec{v}\| = \sqrt{9 + 16} = \sqrt{25} = 5$$

**No Asteroids:** Usado para:
- Verificar se uma entidade move muito rápido (limitar velocidade máxima)
- Calcular distância entre dois pontos

---

### 2.3 Normalização

**Normalizar** um vetor significa criar um novo vetor na mesma direção, mas com magnitude 1.

$$\hat{v} = \frac{\vec{v}}{\|\vec{v}\|} = \begin{pmatrix} v_x / \|\vec{v}\| \\ v_y / \|\vec{v}\| \end{pmatrix}$$

```python
def normalize(v):
    mag = magnitude(v)
    if mag == 0:
        return [0.0, 0.0]
    return [v[0] / mag, v[1] / mag]
```

**Exemplo:**
$$\vec{v} = \begin{pmatrix} 3 \\ 4 \end{pmatrix}, \quad \|\vec{v}\| = 5$$
$$\hat{v} = \begin{pmatrix} 3/5 \\ 4/5 \end{pmatrix} = \begin{pmatrix} 0.6 \\ 0.8 \end{pmatrix} \quad \Rightarrow \quad \|\hat{v}\| = 1$$

**No Asteroids:**
```python
# Se velocidade > max_speed, normalizar e escalar
speed = magnitude(velocity)
if speed > max_speed:
    velocity = [normalize(velocity)[0] * max_speed,
                normalize(velocity)[1] * max_speed]
```

---

### 2.4 Ângulo para Vetor

Converter um **ângulo em radianos** para um **vetor unitário** (ou com magnitude específica).

$$\vec{d}(\theta) = \begin{pmatrix} \sin(\theta) \\ -\cos(\theta) \end{pmatrix}$$

**Nota especial:** Por que seno em $x$ e cosseno em $y$?

- Ângulo $0°$ aponta para cima (negativo Y no Pygame)
- Ângulo $90°$ aponta para a direita

Sem o inverso de Y, teria que ser $\cos(\theta)$ e $\sin(\theta)$.

```python
def from_angle(angle, length=1.0):
    return [length * math.sin(angle), 
            length * -math.cos(angle)]
```

**Exemplos:**
$$\theta = 0° = 0 \text{ rad} \quad \Rightarrow \quad \vec{d} = \begin{pmatrix} \sin(0) \\ -\cos(0) \end{pmatrix} = \begin{pmatrix} 0 \\ -1 \end{pmatrix} \text{ (para cima)}$$

$$\theta = 90° = \pi/2 \text{ rad} \quad \Rightarrow \quad \vec{d} = \begin{pmatrix} \sin(\pi/2) \\ -\cos(\pi/2) \end{pmatrix} = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \text{ (para direita)}$$

$$\theta = 180° = \pi \text{ rad} \quad \Rightarrow \quad \vec{d} = \begin{pmatrix} \sin(\pi) \\ -\cos(\pi) \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \end{pmatrix} \text{ (para baixo)}$$

**No Asteroids:**
```python
# Calcular velocidade de projétil baseado em rotação da nave
rotation_rad = math.radians(ship.rotation)
velocity = from_angle(rotation_rad, bullet_speed)

# Ou: calcular impulso de aceleração
thrust_vec = from_angle(rotation_rad, acceleration)
ship.velocity[0] += thrust_vec[0]
ship.velocity[1] += thrust_vec[1]
```

---

### 2.5 Distância Entre Dois Pontos

$$d = \sqrt{(p2_x - p1_x)^2 + (p2_y - p1_y)^2}$$

Essencialmente a **magnitude do vetor diferença**.

```python
def distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx**2 + dy**2)
```

**Exemplo:**
$$p1 = (1, 2), \quad p2 = (4, 6)$$
$$d = \sqrt{(4-1)^2 + (6-2)^2} = \sqrt{9 + 16} = \sqrt{25} = 5$$

---

### 2.6 Vetor de Ponto a Ponto (com Velocidade)

Criar um **vetor velocidade** apontando de $p1$ em direção a $p2$, com magnitude específica.

$$\vec{v} = \text{speed} \times \frac{p2 - p1}{\|p2 - p1\|}$$

```python
def vector_from_points(p1, p2, speed=1.0):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    mag = magnitude([dx, dy])
    if mag == 0:
        return [0.0, 0.0]
    return [(dx / mag) * speed, (dy / mag) * speed]
```

**Exemplo:**
$$p1 = (0, 0), \quad p2 = (3, 4), \quad \text{speed} = 10$$
$$\text{direção} = \frac{(3, 4)}{5} = (0.6, 0.8)$$
$$\vec{v} = 10 \times (0.6, 0.8) = (6, 8)$$

**No Asteroids:** Quando um asteroide é destruído, um pedaço viaja em direção à nave (homing):
```python
homing_velocity = vector_from_points(asteroid.position, ship.position, speed=1.0)
new_asteroid = Asteroid(asteroid.position, new_size, homing_velocity)
```

---

## Parte 3: Física Computacional

### 3.1 Integração Numérica — Método de Euler

**Problema:** Como atualizar posição baseada em velocidade?

**Solução (simples):** Método de Euler

$$p_{t+1} = p_t + v_t \cdot \Delta t$$

Em nosso projeto, $\Delta t = 1$ frame (implícito), então:

$$p_{t+1} = p_t + v_t$$

```python
def update_entity(entity):
    entity.position[0] += entity.velocity[0]
    entity.position[1] += entity.velocity[1]
```

**Acurácia:** Método de Euler é de primeira ordem, ou seja, erro acumula com o tempo. Mas para um jogo arcade em 30 FPS, é suficiente.

**Exemplo:**
```
Posição inicial: (100, 200)
Velocidade: (2, -1)

Frame 1: p = (100, 200) + (2, -1) = (102, 199)
Frame 2: p = (102, 199) + (2, -1) = (104, 198)
Frame 3: p = (104, 198) + (2, -1) = (106, 197)
```

---

### 3.2 Aceleração e Velocidade

**Velocidade** é a taxa de mudança de posição:
$$\vec{v} = \frac{d\vec{p}}{dt}$$

**Aceleração** é a taxa de mudança de velocidade:
$$\vec{a} = \frac{d\vec{v}}{dt}$$

**Integração discreta:**
$$v_{t+1} = v_t + a \cdot \Delta t$$

Com $\Delta t = 1$:
$$v_{t+1} = v_t + a$$

**No Asteroids:**
```python
def apply_controls(entity, thrust_input, rotation_input):
    entity.rotation += rotation_input * 4  # Rotação angular
    
    if thrust_input:
        # Calcular aceleração na direção que a nave aponta
        rad = math.radians(entity.rotation)
        thrust_vec = from_angle(rad, entity.acceleration)
        
        # Somar aceleração à velocidade
        entity.velocity[0] += thrust_vec[0]
        entity.velocity[1] += thrust_vec[1]
```

---

### 3.3 Atrito e Desaceleração

Em um jogo real, há **resistência ao movimento** (ar, gravidade, etc.).

**Modelo simples:** Aplicar um **fator de friction** a cada frame.

$$v_{t+1} = v_t \times \text{friction}$$

Com $\text{friction} = 0.98$, a velocidade diminui 2% a cada frame.

```python
def update_entity(entity):
    entity.position[0] += entity.velocity[0]
    entity.position[1] += entity.velocity[1]
    
    if hasattr(entity, 'friction'):
        entity.velocity[0] *= entity.friction
        entity.velocity[1] *= entity.friction
```

**Análise temporal:** Após $n$ frames, a velocidade é:
$$v_n = v_0 \times \text{friction}^n$$

Com $v_0 = 5$ e $\text{friction} = 0.98$:
```
Frame 0: 5.0
Frame 10: 5.0 × 0.98^10 ≈ 4.1
Frame 50: 5.0 × 0.98^50 ≈ 1.8
Frame 100: 5.0 × 0.98^100 ≈ 0.7
Frame ∞: 0 (assintoticamente)
```

**Fórmula (limite):**
$$v_\infty = 0 \quad \text{pois} \quad 0.98^n \to 0 \text{ quando } n \to \infty$$

**No Asteroids:** Nave desacelera gradualmente após soltar o botão de impulso, criando "inércia".

---

### 3.4 Velocidade Máxima

Para evitar comportamento irreal, limitar a **velocidade máxima**:

$$\text{se } \|\vec{v}\| > v_{max}: \quad \vec{v} = \frac{\vec{v}}{\|\vec{v}\|} \times v_{max}$$

```python
def update_entity(entity):
    # ... atualizar posição e velocidade ...
    
    if hasattr(entity, 'max_speed'):
        speed = magnitude(entity.velocity)
        if speed > entity.max_speed:
            entity.velocity = [
                (entity.velocity[0] / speed) * entity.max_speed,
                (entity.velocity[1] / speed) * entity.max_speed
            ]
```

**Interpretação:** Normalizar a velocidade (obtém direção) e escalar para o máximo permitido.

**Exemplo:**
```
velocity = [4, 3]
speed = √(16 + 9) = 5
max_speed = 3

normalized = [4/5, 3/5] = [0.8, 0.6]
clamped = [0.8 × 3, 0.6 × 3] = [2.4, 1.8]
```

---

## Parte 4: Detecção de Colisão

### 4.1 Colisão Círculo-Círculo

Dois círculos **colidem** se a distância entre centros é menor que a soma dos raios.

$$\text{colisão} \Leftrightarrow d(c_1, c_2) < r_1 + r_2$$

Onde:
$$d(c_1, c_2) = \sqrt{(c2_x - c1_x)^2 + (c2_y - c1_y)^2}$$

**Implementação óbvia:**
```python
def check_collision(c1, r1, c2, r2):
    dist = distance(c1, c2)
    return dist < r1 + r2
```

**Problema:** Calcular $\sqrt{...}$ é caro computacionalmente.

### 4.2 Otimização: Comparação Sem Raiz Quadrada

**Ideia:** Se $a < b$, então $a^2 < b^2$ (para números positivos).

Logo:
$$d < r_1 + r_2 \Leftrightarrow d^2 < (r_1 + r_2)^2$$

```python
def check_collision(c1, r1, c2, r2):
    dx = c2[0] - c1[0]
    dy = c2[1] - c1[1]
    r_sum = r1 + r2
    return (dx * dx + dy * dy) < (r_sum * r_sum)
```

**Benefício:** Evita uma operação de raiz quadrada (sqrt é lenta).

**Exemplo:**
```
c1 = (10, 10), r1 = 5
c2 = (15, 13), r2 = 4

dx = 15 - 10 = 5
dy = 13 - 10 = 3
d² = 5² + 3² = 25 + 9 = 34
(r1 + r2)² = 9² = 81

34 < 81 → colisão! ✓
```

---

### 4.3 Problema em Asteroids: Colisões Múltiplas

Em cada frame, pode haver múltiplas colisões:
- Vários projéteis atingindo asteroides diferentes
- Um asteroide grande atingindo a nave

**Algoritmo:**
```python
def check_bullet_asteroid_collisions(bullets, asteroids):
    collisions = []
    for i, bullet in enumerate(bullets):
        for j, asteroid in enumerate(asteroids):
            if check_collision(bullet.get_center(), bullet.get_radius(),
                             asteroid.get_center(), asteroid.get_radius()):
                collisions.append((i, j))
    return collisions
```

**Complexidade:** $O(n_b \times n_a)$ onde $n_b$ = número de bullets, $n_a$ = número de asteroides.

**No projeto:** Com ~20 bullets e ~15 asteroides, são ~300 comparações por frame. Aceitável em 30 FPS.

---

## Parte 5: Transformação de Viewport

### 5.1 Problema

Temos um **mundo** (coordenadas do jogo) e queremos desenhar em uma **tela** (coordenadas de pixels).

**Mapeamento necessário:**
- Mundo: $[w_{xmin}, w_{xmax}] \times [w_{ymin}, w_{ymax}]$ = $[0, 800] \times [0, 600]$
- Radar: $[v_{xmin}, v_{xmax}] \times [v_{ymin}, v_{ymax}]$ = $[650, 800] \times [450, 600]$

### 5.2 Solução: Matriz de Viewport

$$M_{viewport} = T(v_{xmin}, v_{ymin}) \cdot S(s_x, s_y) \cdot T(-w_{xmin}, -w_{ymin})$$

Onde:
$$s_x = \frac{v_{xmax} - v_{xmin}}{w_{xmax} - w_{xmin}}, \quad s_y = \frac{v_{ymax} - v_{ymin}}{w_{ymax} - w_{ymin}}$$

**Algoritmo em 3 passos:**

1. **Transladar mundo para origem:** $T(-w_{xmin}, -w_{ymin})$
2. **Escalar para tamanho da viewport:** $S(s_x, s_y)$
3. **Transladar para posição da viewport:** $T(v_{xmin}, v_{ymin})$

```python
def get_window_to_viewport_matrix(w_xmin, w_ymin, w_xmax, w_ymax, 
                                  v_xmin, v_ymin, v_xmax, v_ymax):
    sx = (v_xmax - v_xmin) / (w_xmax - w_xmin)
    sy = (v_ymax - v_ymin) / (w_ymax - w_ymin)
    
    m_trans_origem = get_translation_matrix(-w_xmin, -w_ymin)
    m_escala = get_scale_matrix(sx, sy)
    m_trans_viewport = get_translation_matrix(v_xmin, v_ymin)
    
    return m_trans_viewport @ m_escala @ m_trans_origem
```

### 5.3 Exemplo Numérico

Mapeamento do mundo $[0, 800] \times [0, 600]$ para radar $[650, 800] \times [450, 600]$:

$$s_x = \frac{800 - 650}{800 - 0} = \frac{150}{800} = 0.1875$$
$$s_y = \frac{600 - 450}{600 - 0} = \frac{150}{600} = 0.25$$

Um ponto no mundo $(400, 300)$ (centro) seria mapeado para:
```
1. Transladar: (400, 300) (já está na origem relativa)
2. Escalar: (400 × 0.1875, 300 × 0.25) = (75, 75)
3. Transladar: (75 + 650, 75 + 450) = (725, 525) ✓
```

---

## Parte 6: Rasterização

### 6.1 Conceito

Converter **geometria vetorial** (polígonos) em **pixels**.

Pipeline:
```
Vértices (floats) → Clipping → Rasterização → Pixels (inteiros)
```

---

### 6.2 Algoritmo Bresenham (para linhas)

Desenha uma linha entre $(x_0, y_0)$ e $(x_1, y_1)$ usando apenas operações inteiras.

**Ideia:** Decidir em cada passo se avançar em x apenas ou em x e y.

```python
def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    err = dx - dy
    
    x, y = x0, y0
    while True:
        points.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    
    return points
```

---

### 6.3 Algoritmo Scan-line (para polígonos)

Preenche um polígono convexo linha por linha.

**Algoritmo:**
1. Para cada linha $y$ da tela
2. Encontre as intersecções com as arestas do polígono
3. Ordene as intersecções
4. Desenhe pixels entre pares de intersecções

---

## Conclusão

A matemática do Asteroids é fundamental para:

- **Transformações:** Mover, girar e escalar entidades
- **Física:** Simular movimento realista com inércia
- **Colisão:** Detectar quando objetos se tocam
- **Gráficos:** Converter mundo para pixels na tela

Cada conceito tem uma aplicação direta no código, implementado de forma eficiente para manter 30 FPS em Python puro.

---

*Guia Matemático Completo — Asteroids CG*
