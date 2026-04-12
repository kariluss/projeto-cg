# Product Specification — Asteroids

## 1. Proposta

Criar um jogo de arcade 2D baseado no clássico Asteroids (1979). O jogador deve sobreviver em um campo de asteroides controlando uma nave espacial, destruindo as rochas espaciais para acumular pontos enquanto evita colisões.

## 2. Core Gameplay Loop

- O jogador controla uma nave.
- Asteroides vagam pelo espaço em direções e velocidades aleatórias e constantes.
- O jogador atira projéteis para destruir os asteroides.
- Ao ser atingido, o asteroide se divide em pedaços menores e mais rápidos.
- O número de asteroides e sua velocidade aumentam com o tempo.
- O jogo termina quando o jogador perde todas as suas vidas.

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
