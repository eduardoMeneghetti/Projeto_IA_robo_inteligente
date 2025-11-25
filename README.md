# 🤖 Robô Explorador - Sistema de Navegação Inteligente

Um jogo de exploração automática onde um robô navega por um grid desconhecido, coletando presentes e evitando obstáculos usando algoritmos de busca (DFS e BFS).

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Como Funciona](#como-funciona)
- [Instalação](#instalação)
- [Estrutura do Código](#estrutura-do-código)
- [Algoritmos Utilizados](#algoritmos-utilizados)
- [Elementos do Jogo](#elementos-do-jogo)
- [Sistema de Pontuação](#sistema-de-pontuação)
- [Funções Principais](#funções-principais)


## 🎯 Sobre o Projeto

O Robô Explorador é um sistema de navegação autônoma que utiliza algoritmos de busca para explorar um ambiente desconhecido. O robô aprende o mapa progressivamente, planejando rotas eficientes e tomando decisões estratégicas.

### Objetivo

- Explorar todas as células alcançáveis do grid
- Coletar todos os presentes disponíveis
- Evitar zumbis e pedras
- Chegar à porta de saída após completar a exploração

---

## 🎮 Como Funciona

### Fluxo do Jogo
```
INÍCIO
  ↓
Gerar Grid Aleatório (6x6)
  ↓
┌──────────────────────────────┐
│   LOOP PRINCIPAL             │
│                              │
│  1. Robô analisa situação    │
│  2. Planeja próximo movimento│
│  3. Executa movimento         │
│  4. Atualiza conhecimento     │
│  5. Verifica conclusão        │
└──────────────────────────────┘
  ↓
FIM (porta alcançada ou limite atingido)
```

### Estratégia do Robô

1. **Exploração Sistemática**: Usa BFS para encontrar células não visitadas mais próximas
2. **Planejamento de Rota**: Calcula o caminho mais curto usando BFS
3. **Aprendizado Progressivo**: Registra obstáculos descobertos e ajusta estratégia
4. **Decisão Inteligente**: Só vai para a porta após explorar tudo alcançável

---

## 🔧 Instalação

### Requisitos
```bash
Python 3.7+
pygame
```

### Instalando Dependências
```bash
pip install pygame
```

### Estrutura de Arquivos
```
projeto/
│
├── robo_explorador.py
├── image/
│   ├── robo.png
│   ├── door.png
│   ├── presente.png
│   ├── zombies.png
│   └── pedra.png
└── README.md
```

### Executando
```bash
python robo_explorador.py
```

---

## 🏗️ Estrutura do Código

### Configurações Iniciais
```python
LINHAS = 6                              # Altura do grid
COLUNAS = 6                             # Largura do grid
QTD_PRESENTES = random.randint(3, 9)   # Presentes aleatórios (3-9)
QTD_ZUMBIS = 3                          # Quantidade de zumbis
QTD_PEDRAS = 4                          # Quantidade de pedras
```

### Variáveis de Estado Globais

| Variável | Tipo | Descrição |
|----------|------|-----------|
| `visitadas` | `set` | Células que o robô já pisou |
| `conhecidas` | `set` | Células que o robô já viu/descobriu |
| `bloqueios_conhecidos` | `set` | Zumbis e pedras descobertos |
| `presentes_coletados` | `set` | Presentes já coletados |
| `pontos` | `int` | Pontuação atual |
| `caminho_planejado` | `list` | Próximos passos a executar |
| `ultimos_passos` | `deque` | Histórico dos últimos 10 movimentos |

### Símbolos do Grid

| Símbolo | Significado |
|---------|-------------|
| `'E'` | Empty (vazio/caminho livre) |
| `'R'` | Robô (posição inicial) |
| `'P'` | Presente (+10 pontos) |
| `'Z'` | Zumbi (-20 pontos, respawn) |
| `'PD'` | Pedra (-5 pontos, bloqueio) |
| `'S'` | Saída/Porta (+50 se explorou tudo) |

---

## 🧠 Algoritmos Utilizados

### 1. DFS (Depth-First Search) - Busca em Profundidade

**Função:** `dfs_mapear_alcancaveis(pos_inicial, bloqueios)`

**Propósito:** Mapear TODAS as células alcançáveis a partir de uma posição

**Como funciona:**
- Usa uma **PILHA** (LIFO - Last In, First Out)
- Explora o máximo possível em uma direção antes de voltar
- Não se preocupa com distância, apenas com alcançabilidade

**Retorna:** `set` de posições alcançáveis
```python
# Exemplo de uso:
alcancaveis = dfs_mapear_alcancaveis((robo_l, robo_c), bloqueios_conhecidos)
# Retorna: {(0,0), (0,1), (1,0), (1,1), ...}
```

**Visualização:**
```
R → → → →     (vai fundo primeiro)
    ↓
    → → →
```

### 2. BFS (Breadth-First Search) - Busca em Largura

**Função:** `bfs_encontrar_caminho(origem, destino, bloqueios)`

**Propósito:** Encontrar o MENOR caminho entre dois pontos

**Como funciona:**
- Usa uma **FILA** (FIFO - First In, First Out)
- Explora em camadas (círculos concêntricos)
- Garante o caminho mais curto

**Retorna:** `list` de posições formando o caminho
```python
# Exemplo de uso:
caminho = bfs_encontrar_caminho((2,2), (5,5), bloqueios_conhecidos)
# Retorna: [(2,3), (2,4), (3,4), (4,4), (5,4), (5,5)]
```

**Visualização:**
```
    3 3 3
  2 2 2 2     (expande em círculos)
1 1 R 1 1
  2 2 2 2
    3 3 3
```

---

## 🎲 Elementos do Jogo

### Presentes 🎁
- **Quantidade:** 3 a 9 (aleatório)
- **Pontuação:** +10 pontos cada
- **Comportamento:** Desaparecem após coleta

### Zumbis 🧟
- **Quantidade:** 3
- **Pontuação:** -20 pontos
- **Comportamento:** Causam respawn do robô na posição inicial

### Pedras 🪨
- **Quantidade:** 4
- **Pontuação:** -5 pontos
- **Comportamento:** Bloqueiam passagem

### Porta 🚪
- **Quantidade:** 1
- **Pontuação:** 
  - +50 pontos se explorou tudo
  - -10 pontos se entrou cedo
- **Comportamento:** Finaliza o jogo quando apropriado

---

## 📊 Sistema de Pontuação

| Ação | Pontos | Observações |
|------|--------|-------------|
| Coletar presente | **+10** | - |
| Descobrir pedra | **-5** | Não move para a pedra |
| Descobrir zumbi | **-20** | Causa respawn |
| Chegar na porta (cedo) | **-10** | Ainda há células para explorar |
| Chegar na porta (correto) | **+50** | Explorou tudo alcançável |

---

## 🔧 Funções Principais

### `gerar_grid()`

Gera o mapa aleatório do jogo.

**O que faz:**
1. Cria grid 6x6 vazio
2. Gera lista de todas as 36 posições
3. Embaralha as posições
4. Distribui elementos aleatoriamente

**Garante:** Nenhuma sobreposição de elementos
```python
grid = gerar_grid()
# Retorna matriz 6x6 com elementos distribuídos
```

---

### `dfs_mapear_alcancaveis(pos_inicial, bloqueios)`

Mapeia território alcançável usando DFS.

**Parâmetros:**
- `pos_inicial`: Tupla (linha, coluna) de onde começar
- `bloqueios`: Set de posições bloqueadas (zumbis/pedras)

**Retorna:** Set de todas as posições alcançáveis

**Complexidade:** O(L × C) onde L = linhas, C = colunas

**Exemplo:**
```python
alcancaveis = dfs_mapear_alcancaveis((2, 2), {(1,1), (3,3)})
# Retorna todas as células que pode chegar sem passar por (1,1) e (3,3)
```

---

### `bfs_encontrar_caminho(origem, destino, bloqueios)`

Encontra o menor caminho entre dois pontos usando BFS.

**Parâmetros:**
- `origem`: Tupla (linha, coluna) inicial
- `destino`: Tupla (linha, coluna) final
- `bloqueios`: Set de posições a evitar

**Retorna:** 
- Lista de posições formando o caminho (sem incluir origem)
- `None` se não há caminho

**Complexidade:** O(L × C)

**Exemplo:**
```python
caminho = bfs_encontrar_caminho((0,0), (2,2), bloqueios)
# Retorna: [(0,1), (1,1), (1,2), (2,2)]
```

---

### `encontrar_celula_nao_visitada_mais_proxima_com_bloqueios(bloqueios)`

Encontra a célula não visitada mais próxima.

**O que faz:**
1. Usa DFS para mapear células alcançáveis
2. Filtra apenas as não visitadas
3. Usa BFS para encontrar a mais próxima

**Retorna:** Tupla (linha, coluna) da célula mais próxima ou `None`

**Por que usa DFS + BFS:**
- DFS: "Quais células posso alcançar?" (mapeamento)
- BFS: "Qual está mais perto?" (medição de distância)
```python
celula = encontrar_celula_nao_visitada_mais_proxima_com_bloqueios(bloqueios_temporarios)
# Retorna: (3, 4) - a célula não visitada mais próxima
```

---

### `mover_robo()`

Função principal que controla o comportamento do robô.

**Fluxo de Decisão:**
```
1. Registra posição atual como visitada

2. Tem caminho planejado?
   SIM → Segue próximo passo do plano
   NÃO → Planeja novo caminho
   
3. Ao planejar novo caminho:
   a) Mapeia células alcançáveis (DFS)
   b) Verifica se explorou tudo
   c) Se sim → planeja caminho para porta (BFS)
   d) Se não → encontra célula não visitada (DFS+BFS)
                 e planeja caminho até ela (BFS)

4. Executa movimento e verifica conteúdo:
   - Zumbi → Respawn e recalcula
   - Pedra → Marca como bloqueio e recalcula
   - Presente → Coleta e continua
   - Porta → Verifica se pode entrar
   - Vazio → Move normalmente

5. Atualiza estados e retorna se o jogo acabou
```

**Retorna:** `True` se jogo acabou, `False` se continua

---

### `escolher_movimento_local()`

Função de fallback para escolher movimento quando BFS falha.

**Heurísticas (em ordem de prioridade):**

| Heurística | Pontuação | Objetivo |
|------------|-----------|----------|
| Célula não visitada | +2000 | Priorizar exploração |
| Bloqueio conhecido | -99999 | Evitar obstáculos |
| Posição anterior | -600 | Evitar vai-e-volta |
| Movimento repetido | -400 × repetições | Evitar loops |

**Retorna:** Tupla (linha, coluna, conteúdo) do melhor movimento

**Quando é usada:** Apenas quando BFS não consegue planejar caminho
```python
movimento = escolher_movimento_local()
# Retorna: (2, 3, 'E') - melhor movimento baseado em heurísticas
```

---

### `aciona_morte_robo()`

Reinicia o robô após encontrar um zumbi.

**O que faz:**
1. Incrementa contador de mortes
2. Reseta posição do robô para inicial
3. Limpa histórico de movimentos
4. Reseta contador de progresso
```python
aciona_morte_robo()
# Robô volta para posição_inicial_robo
```

---

## 🔄 Prevenção de Loops

O código implementa múltiplas camadas de proteção contra loops infinitos:

### Camada 1: Histórico Recente
```python
ultimos_passos = deque(maxlen=10)  # Últimos 10 movimentos
# Penaliza movimentos que aparecem muito no histórico
```

### Camada 2: Posição Anterior
```python
posicao_anterior = (robo_l, robo_c)
# Evita vai-e-volta imediato (A→B→A→B)
```

### Camada 3: Conjunto de Visitadas
```python
visitadas = set()
# BFS nunca retorna para células já visitadas no mesmo caminho
```

### Camada 4: Limite de Passos
```python
MAX_PASSOS = 500
# Para o jogo se passar de 500 movimentos (segurança)
```

### Camada 5: Limpeza de Plano
```python
if encontrou_obstaculo:
    caminho_planejado.clear()  # Força replanejamento
```

---

## 🎨 Interface Gráfica (Pygame)

### Configuração Visual
```python
TAM = 80  # Cada célula tem 80x80 pixels
Tela: 480x480 pixels (6 células × 80 pixels)
FPS: 5 (5 movimentos por segundo)
```

### Carregamento de Imagens

O jogo tenta carregar imagens da pasta `image/`. Se falhar, cria quadrados coloridos:
```python
imagens = {
    'R': 'image/robo.png',      # Robô
    'S': 'image/door.png',       # Porta
    'P': 'image/presente.png',   # Presente
    'Z': 'image/zombies.png',    # Zumbi
    'PD': 'image/pedra.png',     # Pedra
    'E': quadrado cinza (60,60,60)  # Vazio
}
```

### Loop de Renderização
```python
1. Captura eventos (fechar janela)
2. Executa lógica do jogo (mover_robo)
3. Desenha grid completo
4. Desenha robô por cima
5. Atualiza tela
6. Aguarda próximo frame (clock.tick)
```

---

## 📈 Estatísticas Finais

Ao final do jogo, são exibidas:
```
🏁 FIM DE JOGO
Pontuação final: XXX
Presentes coletados: X/Y
Mortes por zumbi: X
Células conhecidas: XX
Células visitadas: XX
Bloqueios descobertos: X
Passos totais: XXX
```

---

## 🧪 Exemplos de Execução

### Exemplo 1: Exploração Bem-Sucedida
```
Grid gerado com 5 presentes, 3 zumbis, 4 pedras

Movimento 1: Indo para (0,1) - célula vazia
Movimento 2: Indo para (0,2) - célula vazia
Movimento 3: Indo para (1,2) - Presente coletado! +10 pontos
...
Movimento 45: DESCOBRIU um Zumbi em (3,4)! -20 pontos
Robô reiniciado na posição inicial. Total de mortes: 1
...
Movimento 89: ✅ Tudo explorado! (Visitadas: 28, Alcançáveis: 28)
Movimento 90: Indo para a porta! Caminho: 6 passos
Movimento 96: Porta alcançada! Explorou tudo! +50 pontos

🏁 FIM DE JOGO
Pontuação final: 35
Presentes coletados: 5/5
Mortes por zumbi: 1
Células visitadas: 28
Passos totais: 96
```

### Exemplo 2: Mapa com Área Isolada
```
Grid com área isolada por pedras:

R . . | . P .
. . . | X X X
. P . | . . .

O robô explora a área esquerda completamente,
descobre que a área direita é inacessível,
e vai direto para a porta após explorar tudo alcançável.
```

---

## 🐛 Tratamento de Casos Especiais

### Caso 1: Porta Descoberta Cedo
```python
# Robô encontra a porta mas ainda há células não visitadas
if conteudo == 'S' and len(nao_visitadas) > 0:
    pontos -= 10
    return False  # Não entra, continua explorando
```

### Caso 2: Área Completamente Bloqueada
```python
# Se não há células alcançáveis não visitadas
if len(nao_visitadas) == 0:
    # Vai para a porta (explorou tudo possível)
```

### Caso 3: Obstáculo no Caminho Planejado
```python
if conteudo in ['Z', 'PD']:
    bloqueios_conhecidos.add((nl, nc))
    caminho_planejado.clear()  # Recalcula novo caminho
```

### Caso 4: Sem Movimento Possível
```python
melhor_movimento = escolher_movimento_local()
if melhor_movimento is None:
    return True  # Finaliza o jogo
```

---

## 📚 Conceitos de Ciência da Computação

### Grafos
O grid é representado como um **grafo não-direcionado**:
- Vértices: Células do grid
- Arestas: Conexões entre células adjacentes
- Pesos: Todos têm peso 1 (movimento unitário)

### Complexidade

| Operação | Complexidade | Justificativa |
|----------|--------------|---------------|
| DFS | O(V + E) | V = células, E = conexões |
| BFS | O(V + E) | Mesma justificativa |
| Buscar em Set | O(1) | Hash table |
| Movimento | O(1) | Acesso direto |

**No grid 6×6:**
- V = 36 células
- E ≈ 60 conexões (média)
- DFS/BFS ≈ O(96) operações

### Estruturas de Dados

| Estrutura | Uso | Por quê |
|-----------|-----|---------|
| `set` | visitadas, bloqueios | Busca O(1), sem duplicatas |
| `list` | caminho_planejado | Ordem importa (sequência) |
| `deque` | BFS, histórico | Inserção/remoção O(1) nas pontas |
| `dict` | imagens | Acesso rápido por chave |

---

## 🎓 Aprendizados e Insights

### Design Patterns Utilizados

1. **Strategy Pattern**: Diferentes estratégias (DFS, BFS, heurísticas)
2. **State Pattern**: Robô mantém estado (visitadas, conhecidas, bloqueios)
3. **Pathfinding Pattern**: Planejamento e execução separados

### Decisões de Design

**Por que DFS para mapeamento?**
- Usa menos memória que BFS
- Não precisa calcular distâncias
- Apenas verifica alcançabilidade

**Por que BFS para pathfinding?**
- Garante caminho mais curto
- Importante para eficiência do robô
- Evita zigue-zagues desnecessários

**Por que separar planejamento de execução?**
- Permite otimizar rota completa
- Evita decisões míopes
- Facilita recuperação de erros

---

## 🚀 Possíveis Melhorias

### Algoritmos
- [ ] Implementar A* para caminhos ainda mais eficientes
- [ ] Usar algoritmo de Dijkstra para pesos variáveis
- [ ] Adicionar memória de longo prazo entre execuções

### Gameplay
- [ ] Múltiplos níveis com dificuldade crescente
- [ ] Power-ups e habilidades especiais
- [ ] Sistema de ranking/highscore
- [ ] Modo manual vs automático

### Visualização
- [ ] Mostrar caminho planejado na tela
- [ ] Animações suaves de movimento
- [ ] Heatmap de células visitadas
- [ ] Debug mode com informações em tempo real

### Performance
- [ ] Cache de caminhos calculados
- [ ] Otimização de recálculo apenas em mudanças
- [ ] Paralelização de busca de múltiplos alvos

---

## 📖 Referências

### Algoritmos
- [DFS - Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [BFS - Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Pathfinding - Red Blob Games](https://www.redblobgames.com/pathfinding/)

### Pygame
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pygame Tutorials](https://www.pygame.org/wiki/tutorials)

---

## 👨‍💻 Autor

Desenvolvido por @eduardoMeneghetti como projeto educacional de algoritmos de busca e inteligência artificial.

## 📄 Licença

Este projeto é livre para uso educacional e modificação.

---

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Áreas de interesse:
- Otimização de algoritmos
- Novos modos de jogo
- Melhorias visuais
- Documentação adicional

---

**Versão:** 1.0  
**Última atualização:** 2025
