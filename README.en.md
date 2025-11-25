# 🤖 Robot Explorer - Intelligent Navigation System

An automatic exploration game where a robot navigates through an unknown grid, collecting gifts and avoiding obstacles using search algorithms (DFS and BFS).

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Code Structure](#code-structure)
- [Algorithms Used](#algorithms-used)
- [Game Elements](#game-elements)
- [Scoring System](#scoring-system)
- [Main Functions](#main-functions)

---

## 🎯 About the Project

Robot Explorer is an autonomous navigation system that uses search algorithms to explore an unknown environment. The robot learns the map progressively, planning efficient routes and making strategic decisions.

### Objective

- Explore all reachable cells in the grid
- Collect all available gifts
- Avoid zombies and rocks
- Reach the exit door after completing exploration

---

## 🎮 How It Works

### Game Flow
```
START
  ↓
Generate Random Grid (6x6)
  ↓
┌──────────────────────────────┐
│   MAIN LOOP                  │
│                              │
│  1. Robot analyzes situation │
│  2. Plans next movement      │
│  3. Executes movement        │
│  4. Updates knowledge        │
│  5. Checks completion        │
└──────────────────────────────┘
  ↓
END (door reached or limit hit)
```

### Robot Strategy

1. **Systematic Exploration**: Uses BFS to find nearest unvisited cells
2. **Route Planning**: Calculates shortest path using BFS
3. **Progressive Learning**: Records discovered obstacles and adjusts strategy
4. **Intelligent Decision**: Only goes to door after exploring everything reachable

---

## 🔧 Installation

### Requirements
```bash
Python 3.7+
pygame
```

### Installing Dependencies
```bash
pip install pygame
```

### File Structure
```
project/
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

### Running
```bash
python robo_explorador.py
```

---

## 🏗️ Code Structure

### Initial Configuration
```python
LINHAS = 6                              # Grid height (rows)
COLUNAS = 6                             # Grid width (columns)
QTD_PRESENTES = random.randint(3, 9)   # Random gifts (3-9)
QTD_ZUMBIS = 3                          # Number of zombies
QTD_PEDRAS = 4                          # Number of rocks
```

### Global State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `visitadas` | `set` | Cells the robot has stepped on |
| `conhecidas` | `set` | Cells the robot has seen/discovered |
| `bloqueios_conhecidos` | `set` | Discovered zombies and rocks |
| `presentes_coletados` | `set` | Already collected gifts |
| `pontos` | `int` | Current score |
| `caminho_planejado` | `list` | Next steps to execute |
| `ultimos_passos` | `deque` | History of last 10 movements |

### Grid Symbols

| Symbol | Meaning |
|--------|---------|
| `'E'` | Empty (free path) |
| `'R'` | Robot (initial position) |
| `'P'` | Present/Gift (+10 points) |
| `'Z'` | Zombie (-20 points, respawn) |
| `'PD'` | Rock/Stone (-5 points, blockage) |
| `'S'` | Exit/Door (+50 if explored everything) |

---

## 🧠 Algorithms Used

### 1. DFS (Depth-First Search)

**Function:** `dfs_mapear_alcancaveis(pos_inicial, bloqueios)`

**Purpose:** Map ALL reachable cells from a position

**How it works:**
- Uses a **STACK** (LIFO - Last In, First Out)
- Explores as far as possible in one direction before backtracking
- Doesn't care about distance, only about reachability

**Returns:** `set` of reachable positions
```python
# Usage example:
alcancaveis = dfs_mapear_alcancaveis((robo_l, robo_c), bloqueios_conhecidos)
# Returns: {(0,0), (0,1), (1,0), (1,1), ...}
```

**Visualization:**
```
R → → → →     (goes deep first)
    ↓
    → → →
```

### 2. BFS (Breadth-First Search)

**Function:** `bfs_encontrar_caminho(origem, destino, bloqueios)`

**Purpose:** Find the SHORTEST path between two points

**How it works:**
- Uses a **QUEUE** (FIFO - First In, First Out)
- Explores in layers (concentric circles)
- Guarantees shortest path

**Returns:** `list` of positions forming the path
```python
# Usage example:
caminho = bfs_encontrar_caminho((2,2), (5,5), bloqueios_conhecidos)
# Returns: [(2,3), (2,4), (3,4), (4,4), (5,4), (5,5)]
```

**Visualization:**
```
    3 3 3
  2 2 2 2     (expands in circles)
1 1 R 1 1
  2 2 2 2
    3 3 3
```

---

## 🎲 Game Elements

### Gifts 🎁
- **Quantity:** 3 to 9 (random)
- **Score:** +10 points each
- **Behavior:** Disappear after collection

### Zombies 🧟
- **Quantity:** 3
- **Score:** -20 points
- **Behavior:** Cause robot respawn at initial position

### Rocks 🪨
- **Quantity:** 4
- **Score:** -5 points
- **Behavior:** Block passage

### Door 🚪
- **Quantity:** 1
- **Score:** 
  - +50 points if explored everything
  - -10 points if entered early
- **Behavior:** Ends game when appropriate

---

## 📊 Scoring System

| Action | Points | Notes |
|--------|--------|-------|
| Collect gift | **+10** | - |
| Discover rock | **-5** | Doesn't move to rock |
| Discover zombie | **-20** | Causes respawn |
| Reach door (early) | **-10** | Still cells to explore |
| Reach door (correct) | **+50** | Explored everything reachable |

---

## 🔧 Main Functions

### `gerar_grid()`

Generates the random game map.

**What it does:**
1. Creates empty 6x6 grid
2. Generates list of all 36 positions
3. Shuffles positions
4. Distributes elements randomly

**Guarantees:** No element overlap
```python
grid = gerar_grid()
# Returns 6x6 matrix with distributed elements
```

---

### `dfs_mapear_alcancaveis(pos_inicial, bloqueios)`

Maps reachable territory using DFS.

**Parameters:**
- `pos_inicial`: Tuple (row, column) of starting point
- `bloqueios`: Set of blocked positions (zombies/rocks)

**Returns:** Set of all reachable positions

**Complexity:** O(R × C) where R = rows, C = columns

**Example:**
```python
alcancaveis = dfs_mapear_alcancaveis((2, 2), {(1,1), (3,3)})
# Returns all cells reachable without passing through (1,1) and (3,3)
```

---

### `bfs_encontrar_caminho(origem, destino, bloqueios)`

Finds shortest path between two points using BFS.

**Parameters:**
- `origem`: Tuple (row, column) starting point
- `destino`: Tuple (row, column) end point
- `bloqueios`: Set of positions to avoid

**Returns:** 
- List of positions forming the path (excluding origin)
- `None` if no path exists

**Complexity:** O(R × C)

**Example:**
```python
caminho = bfs_encontrar_caminho((0,0), (2,2), bloqueios)
# Returns: [(0,1), (1,1), (1,2), (2,2)]
```

---

### `encontrar_celula_nao_visitada_mais_proxima_com_bloqueios(bloqueios)`

Finds the nearest unvisited cell.

**What it does:**
1. Uses DFS to map reachable cells
2. Filters only unvisited ones
3. Uses BFS to find the nearest

**Returns:** Tuple (row, column) of nearest cell or `None`

**Why use DFS + BFS:**
- DFS: "Which cells can I reach?" (mapping)
- BFS: "Which is closest?" (distance measurement)
```python
celula = encontrar_celula_nao_visitada_mais_proxima_com_bloqueios(bloqueios_temporarios)
# Returns: (3, 4) - the nearest unvisited cell
```

---

### `mover_robo()`

Main function controlling robot behavior.

**Decision Flow:**
```
1. Register current position as visited

2. Has planned path?
   YES → Follow next step of plan
   NO → Plan new path
   
3. When planning new path:
   a) Map reachable cells (DFS)
   b) Check if explored everything
   c) If yes → plan path to door (BFS)
   d) If no → find unvisited cell (DFS+BFS)
                and plan path to it (BFS)

4. Execute movement and check content:
   - Zombie → Respawn and recalculate
   - Rock → Mark as blockage and recalculate
   - Gift → Collect and continue
   - Door → Check if can enter
   - Empty → Move normally

5. Update states and return if game ended
```

**Returns:** `True` if game ended, `False` if continues

---

### `escolher_movimento_local()`

Fallback function to choose movement when BFS fails.

**Heuristics (in priority order):**

| Heuristic | Score | Goal |
|-----------|-------|------|
| Unvisited cell | +2000 | Prioritize exploration |
| Known blockage | -99999 | Avoid obstacles |
| Previous position | -600 | Avoid back-and-forth |
| Repeated movement | -400 × repetitions | Avoid loops |

**Returns:** Tuple (row, column, content) of best movement

**When used:** Only when BFS can't plan path
```python
movimento = escolher_movimento_local()
# Returns: (2, 3, 'E') - best movement based on heuristics
```

---

### `aciona_morte_robo()`

Resets robot after encountering a zombie.

**What it does:**
1. Increments death counter
2. Resets robot position to initial
3. Clears movement history
4. Resets progress counter
```python
aciona_morte_robo()
# Robot returns to posicao_inicial_robo
```

---

## 🔄 Loop Prevention

The code implements multiple layers of protection against infinite loops:

### Layer 1: Recent History
```python
ultimos_passos = deque(maxlen=10)  # Last 10 movements
# Penalizes movements appearing too much in history
```

### Layer 2: Previous Position
```python
posicao_anterior = (robo_l, robo_c)
# Avoids immediate back-and-forth (A→B→A→B)
```

### Layer 3: Visited Set
```python
visitadas = set()
# BFS never returns to already visited cells in same path
```

### Layer 4: Step Limit
```python
MAX_PASSOS = 500
# Stops game if exceeding 500 movements (safety)
```

### Layer 5: Plan Clearing
```python
if encontrou_obstaculo:
    caminho_planejado.clear()  # Forces replanning
```

---

## 🎨 Graphical Interface (Pygame)

### Visual Configuration
```python
TAM = 80  # Each cell is 80x80 pixels
Screen: 480x480 pixels (6 cells × 80 pixels)
FPS: 5 (5 movements per second)
```

### Image Loading

The game tries to load images from `image/` folder. If it fails, creates colored squares:
```python
imagens = {
    'R': 'image/robo.png',      # Robot
    'S': 'image/door.png',       # Door
    'P': 'image/presente.png',   # Gift
    'Z': 'image/zombies.png',    # Zombie
    'PD': 'image/pedra.png',     # Rock
    'E': gray square (60,60,60)  # Empty
}
```

### Rendering Loop
```python
1. Capture events (close window)
2. Execute game logic (mover_robo)
3. Draw complete grid
4. Draw robot on top
5. Update screen
6. Wait for next frame (clock.tick)
```

---

## 📈 Final Statistics

At game end, displays:
```
🏁 GAME OVER
Final score: XXX
Gifts collected: X/Y
Zombie deaths: X
Known cells: XX
Visited cells: XX
Discovered blockages: X
Total steps: XXX
```

---

## 🧪 Execution Examples

### Example 1: Successful Exploration
```
Grid generated with 5 gifts, 3 zombies, 4 rocks

Movement 1: Going to (0,1) - empty cell
Movement 2: Going to (0,2) - empty cell
Movement 3: Going to (1,2) - Gift collected! +10 points
...
Movement 45: DISCOVERED a Zombie at (3,4)! -20 points
Robot reset at initial position. Total deaths: 1
...
Movement 89: ✅ Everything explored! (Visited: 28, Reachable: 28)
Movement 90: Going to door! Path: 6 steps
Movement 96: Door reached! Explored everything! +50 points

🏁 GAME OVER
Final score: 35
Gifts collected: 5/5
Zombie deaths: 1
Visited cells: 28
Total steps: 96
```

### Example 2: Map with Isolated Area
```
Grid with area isolated by rocks:

R . . | . P .
. . . | X X X
. P . | . . .

Robot explores left area completely,
discovers right area is inaccessible,
and goes straight to door after exploring everything reachable.
```

---

## 🐛 Special Case Handling

### Case 1: Door Discovered Early
```python
# Robot finds door but still has unvisited cells
if conteudo == 'S' and len(nao_visitadas) > 0:
    pontos -= 10
    return False  # Doesn't enter, continues exploring
```

### Case 2: Completely Blocked Area
```python
# If no reachable unvisited cells exist
if len(nao_visitadas) == 0:
    # Go to door (explored everything possible)
```

### Case 3: Obstacle in Planned Path
```python
if conteudo in ['Z', 'PD']:
    bloqueios_conhecidos.add((nl, nc))
    caminho_planejado.clear()  # Recalculates new path
```

### Case 4: No Possible Movement
```python
melhor_movimento = escolher_movimento_local()
if melhor_movimento is None:
    return True  # Ends game
```

---

## 📚 Computer Science Concepts

### Graphs
The grid is represented as an **undirected graph**:
- Vertices: Grid cells
- Edges: Connections between adjacent cells
- Weights: All have weight 1 (unit movement)

### Complexity

| Operation | Complexity | Justification |
|-----------|------------|---------------|
| DFS | O(V + E) | V = cells, E = connections |
| BFS | O(V + E) | Same justification |
| Set Search | O(1) | Hash table |
| Movement | O(1) | Direct access |

**In 6×6 grid:**
- V = 36 cells
- E ≈ 60 connections (average)
- DFS/BFS ≈ O(96) operations

### Data Structures

| Structure | Use | Why |
|-----------|-----|-----|
| `set` | visited, blockages | O(1) search, no duplicates |
| `list` | planned_path | Order matters (sequence) |
| `deque` | BFS, history | O(1) insertion/removal at ends |
| `dict` | images | Fast key access |

---

## 🎓 Learnings and Insights

### Design Patterns Used

1. **Strategy Pattern**: Different strategies (DFS, BFS, heuristics)
2. **State Pattern**: Robot maintains state (visited, known, blockages)
3. **Pathfinding Pattern**: Planning and execution separated

### Design Decisions

**Why DFS for mapping?**
- Uses less memory than BFS
- Doesn't need to calculate distances
- Only checks reachability

**Why BFS for pathfinding?**
- Guarantees shortest path
- Important for robot efficiency
- Avoids unnecessary zigzags

**Why separate planning from execution?**
- Allows complete route optimization
- Avoids myopic decisions
- Facilitates error recovery

---

## 🚀 Possible Improvements

### Algorithms
- [ ] Implement A* for even more efficient paths
- [ ] Use Dijkstra's algorithm for variable weights
- [ ] Add long-term memory between executions

### Gameplay
- [ ] Multiple levels with increasing difficulty
- [ ] Power-ups and special abilities
- [ ] Ranking/highscore system
- [ ] Manual vs automatic mode

### Visualization
- [ ] Show planned path on screen
- [ ] Smooth movement animations
- [ ] Heatmap of visited cells
- [ ] Debug mode with real-time information

### Performance
- [ ] Cache calculated paths
- [ ] Optimize recalculation only on changes
- [ ] Parallelize search for multiple targets

---

## 📖 References

### Algorithms
- [DFS - Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [BFS - Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Pathfinding - Red Blob Games](https://www.redblobgames.com/pathfinding/)

### Pygame
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pygame Tutorials](https://www.pygame.org/wiki/tutorials)

---

## 👨‍💻 Author

Developed by @eduardoMeneghetti as an educational project on search algorithms and artificial intelligence.

## 📄 License

This project is free for educational use and modification.

---

## 🤝 Contributions

Suggestions and improvements are welcome! Areas of interest:
- Algorithm optimization
- New game modes
- Visual improvements
- Additional documentation

---

**Version:** 1.0  
**Last updated:** 2024