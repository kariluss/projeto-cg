# System Specification — Asteroids (CG Course Project)

## 1. System Overview

O sistema é um motor gráfico 2D minimalista construído sobre o `Pygame`. Ele opera no modo "pixel-perfect" e gerencia o pipeline de renderização a partir de uma estrutura de dados de vértices.

## 2. Architecture Layers

- `Core`: Gerencia o _Game Loop_, o estado global (pausado, rodando, game over) e processamento de eventos do sistema.
- `Physics`: Camada de abstração matemática para vetores ($2D$) e inércia.
- `Graphics`: Módulo de renderização bruta (`Bresenham`, `Scan-line`) que recebe listas de vértices.
- `Math`: Módulo de utilidades para transformações afins (Matrizes $3 \times 3$, rotações, translações, vetores).
- `Game`: Controla os pontos, ondas de asteroides, etc.
- `Entities`: Classes (`Ship`, `Asteroid`, `Bullet`) que mantêm o estado e a lógica comportamental.

## 3. Technical Constraints

- A renderização deve ser feita frame a frame, limpando e redesenhando a tela.
- **Matrizes:** Operações de transformações devem ser realizadas via multiplicação de matrizes 3x3 (homogêneas) no módulo `Math` que é e precisa ser uma implementação própria para fim educacional.
- **Rastreio:** A detecção de colisão deve ser feita via _Bounding Boxes_ ou distância euclidiana simples.

## 4. Data Model

### Vértices

- Representados como `tuple` ou `list` $[x, y, 1]$.
- O espaço do modelo deve ser normalizado antes de qualquer transformação.

### Matrizes

- Matrizes $3 \times 3$ seguindo a convenção de coordenadas homogêneas para 2D.
- Ordem de aplicação: $P_{world} = T \times R \times S \times P_{model}$.

## 5. Rendering Pipeline

1. **Modelagem:** Entidade fornece vértices no _Espaço do Modelo_.
2. **Transformação:** `Math` aplica matrizes para mover vértices ao _Espaço do Mundo_.
3. **Clipping:** Algoritmo simples de recorte contra os limites da tela (`Viewport`).
4. **Rasterização:** `Graphics` converte vetores transformados para pixels no `Frame Buffer`.

## 6. Logic Flow

- `main.py` -> `core.loop` -> `game.update` -> `physics.process` -> `graphics.render` -> `display.flip`.

## 7. Persistence (Config)

- Variáveis globais de controle (FPS, largura, altura) definidas em arquivo `config.py` ou carregadas via `json`.
