# 🚀 Asteroids — Projeto de CG

Bem-vindo ao **Asteroids**, um projeto desenvolvido para a disciplina de **Computação Gráfica**.

Este jogo é um clone do clássico arcade de 1979, construído sobre um motor gráfico 2D minimalista. O objetivo principal do projeto é a implementação manual de transformações geométricas (matrizes 3x3) e algoritmos de rasterização, utilizando o Pygame apenas como base para a janela e entrada.

## 🛠️ Tecnologias

- **Linguagem:** Python 3.11+
- **Biblioteca:** Pygame
- **Engine:** Customizada (Matrizes homogêneas e rasterização manual)

## 📦 Como Rodar

### Localmente

Certifique-se de ter o Python instalado. Depois, instale o Pygame e execute o módulo principal:

```bash
pip install pygame
python -m src.main
```

### Via Docker

Se preferir, utilize o Docker para rodar o projeto em um ambiente isolado:

```bash
docker build -t asteroids-cg .
docker run -it asteroids-cg
```

## 🎮 Controles

- **Setas:** Movimentação (Rotação e Aceleração com inércia).
- **Espaço:** Disparo de projéteis.
- **Esc / P:** Pausar ou sair.

---

_Este é um projeto estritamente acadêmico._
