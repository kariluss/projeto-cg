# Product Specification — Asteroids

## 1. Proposta

Criar um jogo de arcade 2D baseado no clássico Asteroids (1979). O jogador deve sobreviver em um campo de asteroides controlando uma nave espacial, destruindo as rochas espaciais para acumular pontos enquanto evita colisões.

## 2. Core Gameplay Loop

- O jogador controla uma nave.
- Asteroides vagam pelo espaço em direções e velocidades aleatórias e constantes.
- O jogador atira projéteis para destruir os asteroides.
- Ao ser atingido, o asteroide se divide em dois pedaços menores.
- O número de asteroides e sua velocidade aumentam com o tempo.
- O jogo termina quando o jogador perde todas as suas vidas.
- **Colisões:** O sistema de colisão deve ser preciso para garantir uma experiência de jogo justa.
- **Menu e Estados:** O jogo deve possuir um menu inicial demonstrando primitivas gráficas e permitir reiniciar após o Game Over.

---

## 2. Interface e Menus

### 2.1 Menu Inicial (START_MENU)
O jogo inicia em uma tela de demonstração técnica que comprova a implementação dos algoritmos de rasterização.
*   **Elementos Visuais:**
    *   **Fundo:** Preenchimento com gradiente suave (Azul Escuro para Preto).
    *   **Planeta Central:** Desenvolvido com algoritmo de Ponto Médio e preenchido com Flood Fill.
    *   **Anéis:** Elipses de ponto médio ao redor do planeta.
    *   **Lasers de Fundo:** Linhas geradas aleatoriamente e recortadas por uma janela retangular central usando o algoritmo de Cohen-Sutherland.
*   **Interações:**
    *   `ENTER`: Inicia o jogo (transição para `RUNNING`).
    *   `ESC`: Sai da aplicação.

### 2.2 Game Over (GAME_OVER)
Exibido quando as vidas chegam a zero.
*   **Interações:**
    *   `SPACE`: Reinicia o jogo completamente (reseta score, vidas e entidades).
    *   `ESC`: Sai da aplicação.

---

## 3. Game Entities

### 3.1 A Nave (Player)

- **Ações:** Rotacionar (esquerda/direita), Acelerar (frente) e Atirar (espaço).
- **Movimento:** Possui inércia. Ao parar de acelerar, a nave continua deslizando na direção do último impulso, desacelerando gradativamente.

### 3.2 Asteroides

- Divididos em 3 tamanhos: Grande, Médio e Pequeno.
- Quando um asteroide Grande é destruído, ele gera dois Médios. Um Médio gera dois Pequenos. O Pequeno é destruído por completo.
- Asteroides menores viajam em velocidades maiores.

### 3.3 Tiros

- Disparados pela ponta da nave.
- Viajam em linha reta com velocidade constante.
- Possuem tempo de vida limitado (após uma certa distância desaparecem).

## 4. Environment & Rules (The World)

- **Tela Infinita:** Caso o player ultrapasse uma borda da tela, ele reaparece no lado oposto. Mas isso não se aplica aos asteroides, eles somem ao passar das bordas para serem recriados aleatoriamente.
- **Colisão:** Qualquer toque físico entre a Nave e um Asteroide resulta na destruição da Nave e perda de uma vida.

## 5. Player Progression & Scoring

- O jogador inicia com 7 vidas.
- Pontuação é ganha ao destruir asteroides.
- **Escalabilidade e Dificuldade:** O jogo deve aumentar o número de asteroides à medida que o jogador progride.
