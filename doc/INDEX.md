# 📖 Índice de Documentação — Asteroids CG

**Bem-vindo!** Esta página ajuda você a encontrar a informação que procura.

---

## 🎯 Por Donde Começar?

### 1️⃣ Primeira Vez? Comece Aqui

- **[QUICK_START.md](QUICK_START.md)** — 5-10 minutos
  - O que é o projeto
  - Como rodar
  - 4 divisões principais
  - Cheat sheet de código

### 2️⃣ Quer Entender o Projeto?

- **[COMPLETE_DOCUMENTATION.md](COMPLETE_DOCUMENTATION.md)** — 30-45 minutos
  - Visão geral completa
  - Arquitetura do sistema
  - Explicação de cada módulo
  - Fluxo de execução

### 3️⃣ Quer Ver Diagramas?

- **[ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)** — 15-20 minutos
  - Estrutura de pastas vs responsabilidades
  - Fluxo de dados visual
  - Dependências entre módulos
  - Ciclo de vida de entidades

### 4️⃣ Quer Aprender Matemática?

- **[MATHEMATICAL_GUIDE.md](MATHEMATICAL_GUIDE.md)** — 45-60 minutos
  - Definições formais com notação matemática
  - Implementações em código
  - Exemplos numéricos
  - Derivações completas

---

## 📚 Por Tópico

### Arquitetura & Design

| Tópico | Arquivo | Tempo | Profundidade |
|--------|---------|-------|-------------|
| Visão geral da arquitetura | COMPLETE_DOCUMENTATION.md (seção 2) | 5 min | ⭐⭐⭐ |
| Camadas do sistema | COMPLETE_DOCUMENTATION.md (seção 3) | 10 min | ⭐⭐⭐⭐ |
| Dependências entre módulos | ARCHITECTURE_DIAGRAM.md (Dependências) | 5 min | ⭐⭐⭐ |
| Game loop | COMPLETE_DOCUMENTATION.md (seção 8) | 10 min | ⭐⭐⭐ |
| Fluxo de um frame | ARCHITECTURE_DIAGRAM.md (Frame timing) | 5 min | ⭐⭐⭐ |

### Módulo Math (Álgebra Linear)

| Tópico | Arquivo | Tempo | Profundidade |
|--------|---------|-------|-------------|
| Introdução ao Math | COMPLETE_DOCUMENTATION.md (seção 4) | 10 min | ⭐⭐ |
| Matrizes básico | MATHEMATICAL_GUIDE.md (1.1-1.3) | 15 min | ⭐⭐⭐⭐ |
| Transformações (TRS) | MATHEMATICAL_GUIDE.md (1.4) | 20 min | ⭐⭐⭐⭐⭐ |
| Composição de matrizes | MATHEMATICAL_GUIDE.md (1.5) | 10 min | ⭐⭐⭐⭐ |
| Operações vetoriais | MATHEMATICAL_GUIDE.md (Parte 2) | 15 min | ⭐⭐⭐ |
| Rotação em detalhe | MATHEMATICAL_GUIDE.md (1.4.3) | 10 min | ⭐⭐⭐⭐ |

### Física (Physics System)

| Tópico | Arquivo | Tempo | Profundidade |
|--------|---------|-------|-------------|
| Visão geral | COMPLETE_DOCUMENTATION.md (seção 6) | 5 min | ⭐⭐ |
| Integração numérica | MATHEMATICAL_GUIDE.md (3.1) | 10 min | ⭐⭐⭐ |
| Inércia & atrito | MATHEMATICAL_GUIDE.md (3.2-3.3) | 10 min | ⭐⭐⭐⭐ |
| Velocidade máxima | MATHEMATICAL_GUIDE.md (3.4) | 5 min | ⭐⭐ |
| Implementação em código | COMPLETE_DOCUMENTATION.md (seção 6, Physics System) | 10 min | ⭐⭐⭐ |
| Wrap-around | ARCHITECTURE_DIAGRAM.md (Ciclo de vida) | 5 min | ⭐⭐⭐ |

### Colisão (Collision System)

| Tópico | Arquivo | Tempo | Profundidade |
|--------|---------|-------|-------------|
| Visão geral | COMPLETE_DOCUMENTATION.md (seção 6, Collision System) | 5 min | ⭐⭐ |
| Colisão círculo-círculo | MATHEMATICAL_GUIDE.md (4.1) | 5 min | ⭐⭐⭐ |
| Otimização sem raiz | MATHEMATICAL_GUIDE.md (4.2) | 5 min | ⭐⭐⭐ |
| Problemas múltiplos | MATHEMATICAL_GUIDE.md (4.3) | 5 min | ⭐⭐⭐ |

### Gráficos (Graphics System)

| Tópico | Arquivo | Tempo | Profundidade |
|--------|---------|-------|-------------|
| Visão geral | COMPLETE_DOCUMENTATION.md (seção 7) | 5 min | ⭐⭐ |
| Pipeline de renderização | COMPLETE_DOCUMENTATION.md (seção 7) | 15 min | ⭐⭐⭐⭐ |
| Transformação TRS | ARCHITECTURE_DIAGRAM.md (Transformação passo a passo) | 10 min | ⭐⭐⭐⭐ |
| Clipping Sutherland-Hodgman | COMPLETE_DOCUMENTATION.md (seção 5) | 10 min | ⭐⭐⭐⭐ |
| Viewport transformation | MATHEMATICAL_GUIDE.md (Parte 5) | 15 min | ⭐⭐⭐⭐ |
| Rasterização | MATHEMATICAL_GUIDE.md (Parte 6) | 15 min | ⭐⭐⭐ |

### Entidades

| Tópico | Arquivo | Tempo | Profundidade |
|--------|---------|-------|-------------|
| Visão geral | COMPLETE_DOCUMENTATION.md (seção 5) | 5 min | ⭐⭐ |
| Ship (nave) | COMPLETE_DOCUMENTATION.md (seção 5, Ship) | 5 min | ⭐⭐⭐ |
| Asteroids | COMPLETE_DOCUMENTATION.md (seção 5, Asteroids) | 5 min | ⭐⭐⭐ |
| Bullets | COMPLETE_DOCUMENTATION.md (seção 5, Bullets) | 5 min | ⭐⭐ |
| Ciclo de vida | ARCHITECTURE_DIAGRAM.md (Ciclo de vida) | 10 min | ⭐⭐⭐⭐ |

### Game Manager

| Tópico | Arquivo | Tempo | Profundidade |
|--------|---------|-------|-------------|
| Visão geral | COMPLETE_DOCUMENTATION.md (seção 6, Game Manager) | 5 min | ⭐⭐⭐ |
| Pontuação | ARCHITECTURE_DIAGRAM.md (Esquema de pontuação) | 5 min | ⭐⭐ |
| Progressão de dificuldade | ARCHITECTURE_DIAGRAM.md (Esquema de pontuação) | 5 min | ⭐⭐⭐ |

### Performance & Otimizações

| Tópico | Arquivo | Tempo | Profundidade |
|--------|---------|-------|-------------|
| Análise de performance | COMPLETE_DOCUMENTATION.md (seção 9) | 10 min | ⭐⭐⭐ |
| Otimizações implementadas | COMPLETE_DOCUMENTATION.md (seção 9) | 5 min | ⭐⭐⭐ |

---

## 🔍 Por Pergunta

### "Como funciona transformação TRS?"
1. **Rápido:** QUICK_START.md → Matemática em 60 segundos
2. **Detalhado:** MATHEMATICAL_GUIDE.md → Parte 1.5
3. **Implementação:** ARCHITECTURE_DIAGRAM.md → Transformação passo a passo
4. **Código:** COMPLETE_DOCUMENTATION.md → seção 5.6

### "Por que não usar √ na colisão?"
→ MATHEMATICAL_GUIDE.md → Parte 4.2

### "Como a nave tem inércia?"
→ MATHEMATICAL_GUIDE.md → Parte 3.2-3.3  
→ Ou: COMPLETE_DOCUMENTATION.md → seção 6, Physics System

### "Qual é o fluxo do game loop?"
→ ARCHITECTURE_DIAGRAM.md → Fluxo de um frame  
→ Ou: COMPLETE_DOCUMENTATION.md → seção 8

### "Como asteroides são destruídos?"
→ COMPLETE_DOCUMENTATION.md → seção 6, Game Manager  
→ Ou: ARCHITECTURE_DIAGRAM.md → Ciclo de vida

### "Por que máximo 20 asteroides pequenos?"
→ QUICK_START.md → Performance (30 FPS)  
→ Ou: COMPLETE_DOCUMENTATION.md → seção 9

### "Como o radar funciona?"
→ COMPLETE_DOCUMENTATION.md → seção 7, Radar  
→ Ou: MATHEMATICAL_GUIDE.md → Parte 5

### "Qual é a ordem de composição TRS?"
→ MATHEMATICAL_GUIDE.md → Parte 1.5  
→ Quick answer: T @ R @ S (ordem inversa!)

### "Como detectar colisão entre bullet e asteroide?"
→ COMPLETE_DOCUMENTATION.md → seção 6, Collision System  
→ Ou: ARCHITECTURE_DIAGRAM.md → Fluxo de dados

---

## 📊 Mapa Mental (Qual arquivo ler)

```
┌─ Quer visão rápida?
│  └─ QUICK_START.md
│
├─ Quer entender arquitetura?
│  └─ ARCHITECTURE_DIAGRAM.md
│
├─ Quer tudo em detalhe?
│  └─ COMPLETE_DOCUMENTATION.md
│
├─ Quer aprender matemática?
│  └─ MATHEMATICAL_GUIDE.md
│
└─ Quer especificações técnicas?
   ├─ system-spec.md
   └─ prod-spec.md
```

---

## ⏱️ Plano de Leitura (por tempo)

### 15 minutos (Iniciante)
1. QUICK_START.md (completo)

### 30 minutos (Intermediário)
1. QUICK_START.md (completo)
2. ARCHITECTURE_DIAGRAM.md (até seção "Fluxo de um Frame")

### 60 minutos (Avançado)
1. QUICK_START.md (completo)
2. COMPLETE_DOCUMENTATION.md (seções 1-4)
3. ARCHITECTURE_DIAGRAM.md (até "Transformação Passo a Passo")

### 2 horas (Muito Avançado)
1. Todos acima
2. MATHEMATICAL_GUIDE.md (Partes 1-3)
3. COMPLETE_DOCUMENTATION.md (seções 5-9)

### 4+ horas (Expert)
Ler todos os arquivos na ordem:
1. QUICK_START.md
2. ARCHITECTURE_DIAGRAM.md
3. COMPLETE_DOCUMENTATION.md
4. MATHEMATICAL_GUIDE.md
5. system-spec.md / prod-spec.md

---

## 🎓 Conceitos por Nível

### Iniciante
- O que é o projeto
- Como rodar
- Controles do jogo
- Estrutura de pastas
- 4 divisões principais

→ Leia: **QUICK_START.md**

### Intermediário
- Arquitetura do sistema
- Fluxo de dados
- Ciclo de vida de entidades
- Game loop
- Transformações TRS (conceitual)

→ Leia: **ARCHITECTURE_DIAGRAM.md** + **COMPLETE_DOCUMENTATION.md** (seções 1-3)

### Avançado
- Matemática de matrizes
- Física computacional
- Detecção de colisão otimizada
- Rasterização
- Clipping de polígonos

→ Leia: **MATHEMATICAL_GUIDE.md** + **COMPLETE_DOCUMENTATION.md** (seções 4-7)

### Expert
- Implementação completa
- Otimizações de performance
- Edge cases
- Bugs conhecidos
- Extensões possíveis

→ Leia: **Todos os arquivos** + Código-fonte

---

## 📄 Resumo dos Arquivos

| Arquivo | Tamanho | Foco | Público |
|---------|---------|------|---------|
| QUICK_START.md | ~2 KB | Resumo executivo | Iniciantes |
| ARCHITECTURE_DIAGRAM.md | ~8 KB | Visual + conceitual | Intermediários |
| COMPLETE_DOCUMENTATION.md | ~15 KB | Completo e técnico | Avançados |
| MATHEMATICAL_GUIDE.md | ~12 KB | Matemática profunda | Matemáticos |
| system-spec.md | ~2 KB | Especificação técnica | Arquitetos |
| prod-spec.md | ~1 KB | Especificação de produto | Game designers |

---

## 🔗 Referências Cruzadas

**Se está lendo:** QUICK_START.md
- Para detalhes → COMPLETE_DOCUMENTATION.md
- Para visualização → ARCHITECTURE_DIAGRAM.md
- Para matemática → MATHEMATICAL_GUIDE.md

**Se está lendo:** ARCHITECTURE_DIAGRAM.md
- Para código → COMPLETE_DOCUMENTATION.md
- Para cálculos → MATHEMATICAL_GUIDE.md
- Para rápida consulta → QUICK_START.md

**Se está lendo:** COMPLETE_DOCUMENTATION.md
- Para visão simplificada → QUICK_START.md
- Para diagramas → ARCHITECTURE_DIAGRAM.md
- Para fórmulas → MATHEMATICAL_GUIDE.md

**Se está lendo:** MATHEMATICAL_GUIDE.md
- Para aplicação prática → COMPLETE_DOCUMENTATION.md
- Para código → Ver `src/modules/math/math.py`
- Para visão geral → QUICK_START.md

---

## ✅ Checklist de Aprendizado

- [ ] Entendo o que é o projeto
- [ ] Sei como rodar
- [ ] Conheço as 4 divisões principais
- [ ] Entendo a arquitetura em camadas
- [ ] Sei o fluxo de um frame
- [ ] Entendo transformações TRS
- [ ] Entendo colisão círculo-círculo
- [ ] Sei como funciona o physics
- [ ] Entendo rasterização
- [ ] Sei como são entidades
- [ ] Conheço o game manager
- [ ] Entendo limites de performance
- [ ] Posso explicar para alguém

---

## 🆘 Precisa de Ajuda?

**Não entendo Matrizes:**
→ MATHEMATICAL_GUIDE.md → Parte 1 (leia cada seção)

**Não entendo por que ordem inversa em TRS:**
→ MATHEMATICAL_GUIDE.md → Parte 1.5 (explicação completa)

**Código está confuso:**
→ Leia ARCHITECTURE_DIAGRAM.md → "Checklist de Conceitos CG"

**Performance está ruim:**
→ COMPLETE_DOCUMENTATION.md → Seção 9

**Quer modificar o jogo:**
→ Primeiro leia QUICK_START.md → Cheat Sheet

---

## 📝 Notas

- Todos os documentos usam **notação matemática LaTeX** — se não renderizar, é apenas formatação visual, o texto é compreensível sem ela
- **Exemplos numéricos** estão em todos os documentos para clareza
- **Código em Python** está sempre comentado
- Sinta-se à vontade para **imprimir** ou **converter para PDF**

---

**Última atualização:** 2026  
**Status:** Documentação Completa ✅
