# System Specification — Asteroids (CG Course Project)

## 1. System Overview

O sistema é um motor gráfico 2D minimalista construído sobre o `Pygame`. Ele opera no modo "pixel-perfect" e gerencia o pipeline de renderização a partir de uma estrutura de dados de vértices.

## 2. Architecture Layers (Strict Layering)

- `Core`: Gerencia o _Game Loop_, o estado global (pausado, rodando, game over) e orquestra a comunicação entre os sistemas.
- `Math`: O núcleo matemático do projeto. Provê abstrações de Álgebra Linear. **Nenhuma outra camada deve implementar cálculos matriciais próprios.**
- `Physics System`: Sistema que processa a movimentação, inércia e colisões. As entidades **não** processam sua própria física.
- `Graphics System`: Módulo de renderização bruta (`Bresenham`, `Scan-line`) e a Pipeline de Transformação. As entidades **não** possuem métodos de desenho.
- `Game`: Gerenciamento de regras de alto nível (pontuação, ondas).
- `Entities`: Recipientes puros de dados (Data Models). Contêm apenas estado (posição, velocidade, vértices locais, etc). **Proibido importar Pygame ou Graphics nestas classes.**

## 3. Technical Constraints

- A renderização deve ser feita frame a frame, limpando e redesenhando a tela.
- **Matemática:** O módulo `Math` é a base para todos os cálculos do sistema (vetoriais e matriciais).
- **Performance:** Devido ao custo computacional da rasterização via Scan-line em Python, o sistema limita o número máximo de asteroides pequenos simultâneos (`MAX_SMALL_ASTEROIDS`) para evitar quedas bruscas de FPS.

## 4. Data Model

### Vértices

- Representados como `tuple` ou `list` $[x, y, 1]$.
- **Normalização:** O espaço do modelo **deve** ser normalizado entre $[-1, 1]$ no arquivo da entidade. O tamanho real deve ser definido por uma Matriz de Escala durante a renderização.

## 5. Rendering Pipeline

1. **Modelagem:** Entidade fornece vértices no _Espaço do Modelo_.
2. **Transformação:** `Math` aplica matrizes para mover vértices ao _Espaço do Mundo_.
3. **Clipping:** Algoritmo simples de recorte contra os limites da tela (`Viewport`).
4. **Rasterização:** `Graphics` converte vetores transformados para pixels no `Frame Buffer`.

## 6. Logic Flow

- `main.py` -> `core.loop` -> `game.update` -> `physics.process` -> `graphics.render` -> `display.flip`.

## 7. Persistence (Config)

- Variáveis globais de controle (FPS, largura, altura) definidas em arquivo `config.py` ou carregadas via `json`.
