# System Specification — Asteroids (CG Course Project)

## 1. System Overview

O sistema é um motor gráfico 2D minimalista construído sobre o `Pygame`. Ele opera no modo "pixel-perfect" e gerencia o pipeline de renderização a partir de uma estrutura de dados de vértices.

## 2. Architecture Layers (Strict Layering)

- **Core:** Gerencia o _Game Loop_, o estado global (START_MENU, RUNNING, PAUSED, GAME_OVER) e orquestra a comunicação entre os sistemas.
- **Math:** O núcleo matemático do projeto. Provê abstrações de Álgebra Linear (Vetores e Matrizes).
- **Physics System:** Sistema que processa a movimentação, inércia e colisões.
- **Graphics System:** Módulo de renderização bruta, implementando algoritmos clássicos de computação gráfica sem o uso de funções `draw` nativas (exceto bordas de UI).
- **Game:** Gerenciamento de regras de alto nível (pontuação, ondas).
- **Entities:** Recipientes puros de dados (Nave, Asteroides, Tiros).

## 3. Graphics Module Detail

Este módulo é o coração visual do projeto. Toda a rasterização é feita "na mão" usando `setPixel`.

*   **Algoritmos Implementados:**
    *   **Bresenham:** Desenho de linhas.
    *   **DDA:** Alternativa para desenho de linhas.
    *   **Ponto Médio para Círculo:** Gerador de circunferências com simetria de 8 vias.
    *   **Ponto Médio para Elipse:** Gerador de elipses com simetria de 4 vias e divisão em duas regiões.
    *   **Scanline Fill:** Preenchimento de polígonos.
    *   **Scanline Gradient Fill:** Preenchimento com interpolação de cores entre vértices.
    *   **Flood Fill:** Algoritmo de preenchimento por inundação (iterativo via pilha).
    *   **Cohen-Sutherland:** Recorte de linhas contra janela retangular.
    *   **Sutherland-Hodgman:** Recorte de polígonos contra viewport.
    *   **Scanline Texture:** Rasterização de imagens (texturas) sobre polígonos com interpolação UV.

## 4. Technical Constraints

- A renderização deve ser feita frame a frame, limpando e redesenhando a tela.
- **Matemática:** O módulo `Math` é a base para todos os cálculos do sistema (vetoriais e matriciais).
- **Performance:** Devido ao custo computacional da rasterização via Scan-line em Python, o sistema limita o número máximo de asteroides pequenos simultâneos (`MAX_SMALL_ASTEROIDS`).

## 5. Logic Flow & States

- **Loop:** `main.py` -> `core.loop` -> `game.update` -> `physics.process` -> `graphics.render`.
- **Estados:**
    - `START_MENU`: Tela inicial demonstrando os algoritmos. Prova técnica.
    - `RUNNING`: Jogo em execução.
    - `PAUSED`: Jogo pausado.
    - `GAME_OVER`: Fim de jogo, permite reiniciar com `SPACE`.

## 6. Rendering Pipeline

1. **Modelagem:** Entidade fornece vértices no _Espaço do Modelo_.
2. **Transformação:** `Math` aplica matrizes para mover vértices ao _Espaço do Mundo_.
3. **Clipping:** Recorte contra os limites da tela (`Viewport`).
4. **Rasterização:** `Graphics` converte vetores transformados para pixels no `Frame Buffer`.
