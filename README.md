# Projeto Asteroids - Arquitetura Inicial

Restrição principal: **Desenho de primitivas na unha (Bresenham, Scanline, Transformações Matriciais).**

Projeto dividido em 3 camadas estritas.

## 1. Motor Gráfico (Renderer / Rasterizer)

O "cego" para a lógica do jogo. Sua única responsabilidade é receber dados matemáticos (vértices e matrizes) e acender pixels na tela.

- **Rasterização de Linhas:** Implementação do Algoritmo de Bresenham.
- **Preenchimento de Polígonos:** Algoritmos de Scan-line ou Flood-fill.
- **Transformações Geométricas (Afins):** Multiplicação de matrizes para translação, rotação e escala.
  - Aplica a transformação de vetores e pontos através da notação matricial homogênea: $\mathbf{v'} = M \cdot \mathbf{v}$
- **Contrato:** Só aceita arrays de vértices (pontos 2D) e cores. Não sabe o que é uma "Nave" ou um "Asteroide".

## 2. Física e Lógica de Jogo (Game State)

O "cego" para a tela. Cuida inteiramente das regras do universo do jogo usando matemática vetorial pura.

- **Entidades:** Representação matemática da Nave, Asteroides e Tiros (posição $x, y$, ângulo $\theta$).
- **Cinemática:** Atualização de posições baseada em velocidade e aceleração vetorial ao longo do tempo.
- **Detecção de Colisão:** Testes de interseção (ex: Bounding Box, Bounding Circle ou Point-in-Polygon).
- **Contrato:** Expõe o estado atual dos objetos (seus vértices no _Espaço do Mundo_) para que o Core possa repassá-los ao Motor Gráfico.

## 3. Core / Game Loop

O maestro da aplicação. É a ponte entre o sistema operacional (I/O) e os dois módulos acima.

- **Input:** Captura eventos de teclado/mouse e repassa como "comandos" para o módulo de Física (ex: `nave.acelerar()`, `nave.girar()`).
- **Tempo:** Gerencia o `delta_time` para garantir que a física seja consistente independente do framerate.
- **Orquestração:**
  1. Lê input.
  2. Atualiza Física(delta_time).
  3. Limpa tela.
  4. Pega os vértices atualizados da Física e manda o Motor Gráfico desenhar.
  5. Atualiza o display (Swap buffers).
