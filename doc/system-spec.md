# System Specification — Asteroids (CG Course Project)

## 1. System Overview

O sistema é um motor gráfico 2D minimalista construído sobre o `Pygame`. Ele opera no modo "pixel-perfect" e gerencia o pipeline de renderização a partir de uma estrutura de dados de vértices.

## 2. Architecture Layers

- `Core`: Gerencia o _Game Loop_, o estado global (pausado, rodando, game over) e processamento de eventos do sistema.
- `Math`: O núcleo matemático do projeto. Provê abstrações de Álgebra Linear, cálculos vetoriais e transformações afins utilizando Matrizes $3 \times 3$ em coordenadas homogêneas.
- `Physics`: Camada de lógica física que utiliza o módulo `Math`.
- `Graphics`: Módulo de renderização bruta (`Bresenham`, `Scan-line`) que recebe listas de vértices.
- `Game`: Controla os pontos, ondas de asteroides, etc.
- `Entities`: Classes (`Ship`, `Asteroid`, `Bullet`) que mantêm o estado e a lógica comportamental.

## 3. Technical Constraints

- A renderização deve ser feita frame a frame, limpando e redesenhando a tela.
- **Matemática:** O módulo `Math` é a base para todos os cálculos do sistema (vetoriais e matriciais).

## 4. Data Model

### Vértices

- Representados como `tuple` ou `list` $[x, y, 1]$.
- O espaço do modelo deve ser normalizado antes de qualquer transformação.

## 5. Rendering Pipeline

1. **Modelagem:** Entidade fornece vértices no _Espaço do Modelo_.
2. **Transformação:** `Math` aplica matrizes para mover vértices ao _Espaço do Mundo_.
3. **Clipping:** Algoritmo simples de recorte contra os limites da tela (`Viewport`).
4. **Rasterização:** `Graphics` converte vetores transformados para pixels no `Frame Buffer`.

## 6. Logic Flow

- `main.py` -> `core.loop` -> `game.update` -> `physics.process` -> `graphics.render` -> `display.flip`.

## 7. Persistence (Config)

- Variáveis globais de controle (FPS, largura, altura) definidas em arquivo `config.py` ou carregadas via `json`.
