import pygame
import random
import copy
from collections import deque

#CONFIGURAÇÕES INICIAIS
LINHAS = 6
COLUNAS = 6
QTD_PRESENTES = random.randint(3, 9)
QTD_ZUMBIS = 3
QTD_PEDRAS = 4


#INICIALIZAÇÃO DO AMBIENTE
def encontrar_robo(grid):
    for i in range(LINHAS):
        for j in range(COLUNAS):
            if grid[i][j] == 'R':
                return i, j
    return None, None

def gerar_grid():
    grid = [['E' for _ in range(COLUNAS)] for _ in range(LINHAS)]
    posicoes = [(i, j) for i in range(LINHAS) for j in range(COLUNAS)]
    random.shuffle(posicoes)

    for _ in range(QTD_PRESENTES):
        i, j = posicoes.pop()
        grid[i][j] = 'P'

    for _ in range(QTD_ZUMBIS):
        i, j = posicoes.pop()
        grid[i][j] = 'Z'

    i, j = posicoes.pop()
    grid[i][j] = 'S'

    i, j = posicoes.pop()
    grid[i][j] = 'R'

    for _ in range(QTD_PEDRAS):
        i, j = posicoes.pop()
        grid[i][j] = 'PD'

    return grid

pontos = 0
vivo = True
memoria = {}
visitado = set()
presentes_coletados = set()
tentativas = 0  # Contador de tentativas
historico_posicoes = []  # Histórico das últimas N posições
MAX_HISTORICO = 20  # Tamanho do histórico para detectar loops
contador_loop = 0  # Contador de detecções de loop

grid = gerar_grid()
grid_inicial = copy.deepcopy(grid)

robo_i, robo_j = encontrar_robo(grid)
robo_inicial = (robo_i, robo_j)
visitado.add(robo_inicial)
historico_posicoes.append((robo_i, robo_j))

print("="*50)
print("🤖 ROBÔ INTELIGENTE INICIADO!")
print(f"📍 Posição inicial: {robo_inicial}")
print(f"🎁 Total de presentes: {QTD_PRESENTES}")
print(f"🧟 Zumbis: {QTD_ZUMBIS} | 🪨 Pedras: {QTD_PEDRAS}")
print("="*50)

deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
direcoes = {
    "CIMA": (-1, 0),
    "BAIXO": (1, 0),
    "ESQUERDA": (0, -1),
    "DIREITA": (0, 1)
}

def posicoes_robo(i, j):
    percepcoes = {}
    memoria[(i, j)] = grid[i][j]

    for nome, (di, dj) in direcoes.items():
        ni, nj = i + di, j + dj
        if 0 <= ni < LINHAS and 0 <= nj < COLUNAS:
            conteudo = grid[ni][nj]
            percepcoes[nome] = conteudo
            memoria[(ni, nj)] = conteudo
        else:
            percepcoes[nome] = 'PAREDE'
    return percepcoes

def calcular_celulas_alcancaveis():
    alcancaveis = set()
    fila = deque([robo_inicial])
    alcancaveis.add(robo_inicial)
    
    while fila:
        x, y = fila.popleft()
        
        for di, dj in deltas:
            nx, ny = x + di, y + dj
            
            if not (0 <= nx < LINHAS and 0 <= ny < COLUNAS):
                continue
            
            if (nx, ny) in alcancaveis:
                continue
            
            conteudo = memoria.get((nx, ny), None)
            
            # Bloqueia pedras e zumbis
            if conteudo in ('PD', 'Z'):
                continue
            
            alcancaveis.add((nx, ny))
            fila.append((nx, ny))
    
    return alcancaveis

def bfs_para_objetivo(inicio, objetivo_func, evitar_zumbis=True, evitar_porta=False):
    fila = deque([(inicio, [])])
    vistos = {inicio}

    while fila:
        (x, y), caminho = fila.popleft()

        # Testa se chegou no objetivo
        if objetivo_func((x, y)):
            if caminho:
                return caminho[0]  # Retorna primeira direção
            return None

        # Expande vizinhos
        for nome_dir in ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]:
            di, dj = direcoes[nome_dir]
            nx, ny = x + di, y + dj

            if not (0 <= nx < LINHAS and 0 <= ny < COLUNAS):
                continue
            if (nx, ny) in vistos:
                continue

            conteudo_mem = memoria.get((nx, ny), None)
            
            # Bloqueia pedras
            if conteudo_mem == 'PD':
                continue
                
            # Bloqueia zumbis se pedido
            if evitar_zumbis and conteudo_mem == 'Z':
                continue
            
            # Bloqueia porta se pedido (para forçar exploração)
            if evitar_porta and conteudo_mem == 'S':
                continue

            vistos.add((nx, ny))
            fila.append(((nx, ny), caminho + [nome_dir]))

    return None

def encontrar_presente_seguro():
    def eh_presente_seguro(pos):
        if memoria.get(pos) != 'P':
            return False
        if pos in presentes_coletados:
            return False
            
        # Verifica se tem zumbi adjacente
        x, y = pos
        for di, dj in deltas:
            nx, ny = x + di, y + dj
            if 0 <= nx < LINHAS and 0 <= ny < COLUNAS:
                if memoria.get((nx, ny)) == 'Z':
                    return False
        return True
    
    # Evita porta no caminho até explorar tudo
    evitar_porta = not (explorou_tudo() and not existe_presente_alcancavel())
    return bfs_para_objetivo((robo_i, robo_j), eh_presente_seguro, evitar_porta=evitar_porta)

def detectar_loop():
    if len(historico_posicoes) < 10:
        return False
    
    # Verifica se as últimas 10 posições são muito repetitivas
    ultimas_10 = historico_posicoes[-10:]
    posicoes_unicas = len(set(ultimas_10))
    
    # Se visitou menos de 4 posições únicas nas últimas 10 movimentos = loop
    if posicoes_unicas <= 3:
        return True
    
    return False

def encontrar_caminho_de_fuga():
    pos_atual = (robo_i, robo_j)
    
    # Pega células visitadas, ordenadas por distância
    celulas_visitadas = list(visitado)
    
    def distancia_manhattan(pos):
        return abs(pos[0] - robo_i) + abs(pos[1] - robo_j)
    
    # Ordena por distância (mais longe primeiro)
    celulas_visitadas.sort(key=distancia_manhattan, reverse=True)
    
    # Tenta encontrar caminho para células distantes
    for celula_distante in celulas_visitadas[:10]:  # Testa as 10 mais distantes
        if distancia_manhattan(celula_distante) < 3:
            continue  
        
        # Ignora a porta
        if memoria.get(celula_distante) == 'S':
            continue
        
    
        def eh_destino(pos):
            return pos == celula_distante
        
        direcao = bfs_para_objetivo(pos_atual, eh_destino, evitar_zumbis=True, evitar_porta=True)
        if direcao:
            print(f"🔄 FUGA DE LOOP: Indo para posição distante {celula_distante}")
            return direcao
    
    return None

def encontrar_celula_inexplorada():
    # Calcula todas as células alcançáveis considerando conhecimento atual
    alcancaveis = calcular_celulas_alcancaveis()
    
    # Células não visitadas (EXCETO a porta, para não travar)
    nao_visitadas = alcancaveis - visitado
    
    # Remove a porta das células a explorar (para não tentar ir até ela)
    nao_visitadas_sem_porta = set()
    for pos in nao_visitadas:
        if memoria.get(pos) != 'S':
            nao_visitadas_sem_porta.add(pos)
    
    if not nao_visitadas_sem_porta:
        return None
    
    # BFS para encontrar a mais próxima, EVITANDO a porta como passagem
    def eh_nao_visitada(pos):
        #return pos in nao_visitadas_sem_porta
    
        return bfs_para_objetivo((robo_i, robo_j), eh_nao_visitada, evitar_porta=True)

    # Calcula todas as células alcançáveis considerando conhecimento atual
    alcancaveis = calcular_celulas_alcancaveis()
    
    # Células não visitadas (EXCETO a porta, para não travar)
    nao_visitadas = alcancaveis - visitado
    
    # Remove a porta das células a explorar (para não tentar ir até ela)
    nao_visitadas_sem_porta = set()
    for pos in nao_visitadas:
        if memoria.get(pos) != 'S':
            nao_visitadas_sem_porta.add(pos)
    
    if not nao_visitadas_sem_porta:
        return None
    
    # BFS para encontrar a mais próxima
    def eh_nao_visitada(pos):
        return pos in nao_visitadas_sem_porta
    
    return bfs_para_objetivo((robo_i, robo_j), eh_nao_visitada)

def encontrar_porta():
    def eh_porta(pos):
        return memoria.get(pos) == 'S'
       
    return bfs_para_objetivo((robo_i, robo_j), eh_porta)

def explorou_tudo():
    alcancaveis = calcular_celulas_alcancaveis()
    
    # Remove a porta da contagem de células a explorar
    alcancaveis_sem_porta = set()
    for pos in alcancaveis:
        if memoria.get(pos) != 'S':
            alcancaveis_sem_porta.add(pos)
    
    nao_visitadas = alcancaveis_sem_porta - visitado
    
    if not nao_visitadas:
        print(f"✅ Exploração completa! Visitou {len(visitado)} células.")
        return True
    
    print(f"🔍 Explorando... Visitadas: {len(visitado)}, Faltam: {len(nao_visitadas)}")
    return False

def existe_presente_alcancavel():
    """Verifica se existe algum presente que podemos alcançar"""
    for pos, conteudo in memoria.items():
        if conteudo == 'P' and pos not in presentes_coletados:
            # Verifica se consegue chegar lá
            if bfs_para_objetivo((robo_i, robo_j), lambda p: p == pos):
                return True
    return False

def definir_direcao():
    percepcoes = posicoes_robo(robo_i, robo_j)

    # 0) DETECÇÃO DE LOOP: Se está preso, tenta fugir
    if detectar_loop():
        global contador_loop
        contador_loop += 1
        print(f"⚠️ LOOP DETECTADO #{contador_loop}! Tentando escapar...")
        
        direcao_fuga = encontrar_caminho_de_fuga()
        if direcao_fuga:
            return direcao_fuga
        
        # Se não encontrou fuga, limpa histórico e continua normalmente
        historico_posicoes.clear()
        historico_posicoes.append((robo_i, robo_j))

    # 1) PRIORIDADE MÁXIMA: Fugir de zumbi adjacente
    for direcao, conteudo in percepcoes.items():
        if conteudo == "Z":
            # Tenta qualquer direção que não seja zumbi, pedra ou porta
            opcoes_fuga = []
            for d, c in percepcoes.items():
                if c not in ("Z", "PD", "PAREDE", "S"):
                    opcoes_fuga.append(d)
            if opcoes_fuga:
                return random.choice(opcoes_fuga)
            # Se não tem fuga sem porta, aceita porta
            for d, c in percepcoes.items():
                if c not in ("Z", "PD", "PAREDE"):
                    return d
            return random.choice(list(direcoes.keys()))

    # 2) Buscar presente seguro (ALTA PRIORIDADE)
    direcao_presente = encontrar_presente_seguro()
    if direcao_presente:
        return direcao_presente

    # 3) CRUCIAL: Explorar células não visitadas (ANTES de ir para porta!)
    direcao_exploracao = encontrar_celula_inexplorada()
    if direcao_exploracao:
        return direcao_exploracao

    # 4) APENAS SE EXPLOROU TUDO: ir para porta
    if explorou_tudo() and not existe_presente_alcancavel():
        direcao_porta = encontrar_porta()
        if direcao_porta:
            print("🚪 Indo para a porta - mapa totalmente explorado!")
            return direcao_porta

    # 5) Movimento aleatório seguro (fallback - evita porta até explorar tudo)
    opcoes_seguras = []
    for d, c in percepcoes.items():
        # Evita pedra, zumbi, parede E porta (até explorar tudo)
        if c not in ("PD", "Z", "PAREDE", "S"):
            opcoes_seguras.append(d)
    
    if opcoes_seguras:
        # Prioriza direções que NÃO levam a posições recentes
        if len(historico_posicoes) > 5:
            posicoes_recentes = set(historico_posicoes[-5:])
            opcoes_novas = []
            for d in opcoes_seguras:
                di, dj = direcoes[d]
                ni, nj = robo_i + di, robo_j + dj
                if (ni, nj) not in posicoes_recentes:
                    opcoes_novas.append(d)
            
            if opcoes_novas:
                return random.choice(opcoes_novas)
        
        return random.choice(opcoes_seguras)
    
    # 6) Se ficou preso e só tem porta disponível
    # Verifica se realmente pode entrar (explorou tudo)
    if explorou_tudo() and not existe_presente_alcancavel():
        for d, c in percepcoes.items():
            if c == "S":
                print("🚪 Única saída é a porta - tentando entrar")
                return d
    
    # 7) Último recurso: tenta qualquer movimento válido (incluindo porta)
    for d, c in percepcoes.items():
        if c not in ("PD", "Z", "PAREDE"):
            return d

    return None

def resetar_robo():
    global robo_i, robo_j, vivo, grid, presentes_coletados, tentativas, historico_posicoes
    
    # Restaura o mapa original (MESMO mapa)
    grid[:] = copy.deepcopy(grid_inicial)
    
    # Reposiciona o robô na posição inicial
    robo_i, robo_j = robo_inicial
    grid[robo_i][robo_j] = 'R'
    
    # Reseta presentes coletados (precisa coletar novamente)
    presentes_coletados = set()
    
    # Limpa histórico de posições para nova tentativa
    historico_posicoes = [(robo_i, robo_j)]
    
    # MANTÉM: memoria e visitado (aprendizado!)
    # NÃO zera pontos - acumula ao longo das tentativas
    
    vivo = True
    tentativas += 1

    print("\n" + "="*50)
    print(f"🔄 TENTATIVA #{tentativas} - Robô reiniciou no mesmo mapa!")
    print(f"🧠 Memória preservada: {len(memoria)} células conhecidas")
    print(f"👣 Células já visitadas: {len(visitado)}")
    print(f"💰 Pontos acumulados: {pontos}")
    print("="*50 + "\n")

def movimento_agente():
    global robo_i, robo_j, pontos, vivo, grid, presentes_coletados

    if not vivo:
        return

    acao = definir_direcao()
    
    if acao is None:
        print("⚠️ Robô travado! Tentando destravar...")
        
        # Tenta movimento de fuga de loop forçado
        direcao_fuga = encontrar_caminho_de_fuga()
        if direcao_fuga:
            acao = direcao_fuga
            print(f"🔄 Destravando via fuga de loop: {direcao_fuga}")
        else:
            # Se travou, tenta qualquer movimento válido (EXCETO porta se não pode entrar)
            percepcoes = posicoes_robo(robo_i, robo_j)
            explorou = explorou_tudo()
            tem_presente = existe_presente_alcancavel()
            pode_entrar_porta = explorou and not tem_presente
            
            for d, c in percepcoes.items():
                # Se não pode entrar na porta, NÃO tenta
                if c == "S" and not pode_entrar_porta:
                    continue
                
                if c not in ("PD", "Z", "PAREDE"):
                    acao = d
                    print(f"🔄 Destravando com movimento: {d}")
                    break
        
        if acao is None:
            print("❌ Robô completamente bloqueado! Tentando qualquer coisa...")
            # Último recurso: movimento aleatório em qualquer direção válida
            percepcoes = posicoes_robo(robo_i, robo_j)
            for d, c in percepcoes.items():
                if c not in ("PD", "Z", "PAREDE"):
                    acao = d
                    break
            
            if acao is None:
                print("💀 Robô está totalmente cercado!")
                return

    di, dj = direcoes[acao]
    ni, nj = robo_i + di, robo_j + dj

    if not (0 <= ni < LINHAS and 0 <= nj < COLUNAS):
        return

    conteudo = grid[ni][nj]

    # Pedra
    if conteudo == 'PD':
        memoria[(ni, nj)] = 'PD'
        print("🪨 Bateu em pedra, tentando outro caminho...")
        return

    # Zumbi - MORRE e reinicia no mesmo mapa
    if conteudo == 'Z':
        memoria[(ni, nj)] = 'Z'
        pontos -= 10
        vivo = False
        print(f"☠️ Robô morreu! Pontos: {pontos}")
        resetar_robo()  # Reinicia no MESMO mapa
        return

    # Presente
    if conteudo == 'P':
        memoria[(ni, nj)] = 'P'
        presentes_coletados.add((ni, nj))
        pontos += 10
        print(f"🎁 Presente {len(presentes_coletados)}/{QTD_PRESENTES} coletado! Pontos: {pontos}")

    # Porta - verifica se REALMENTE pode entrar
    if conteudo == 'S':
        explorou = explorou_tudo()
        tem_presente = existe_presente_alcancavel()
        
        print(f"🚪 Na porta - Explorou: {explorou}, Tem presente: {tem_presente}")
        
        if explorou and not tem_presente:
            # VITÓRIA! Robô chegou na porta
            print("\n" + "🏆"*25)
            print(f"🎉 VITÓRIA NA TENTATIVA #{tentativas}!")
            print(f"💰 Pontos finais: {pontos}")
            print(f"🎁 Presentes coletados: {len(presentes_coletados)}/{QTD_PRESENTES}")
            print(f"📊 Células visitadas: {len(visitado)}/{LINHAS*COLUNAS}")
            print("🏆"*25 + "\n")
            
            # Para o jogo - robô venceu!
            global rodando
            rodando = False
            return
        else:
            # NÃO PODE ENTRAR - não faz movimento e força exploração
            print("❌ Porta bloqueada! Voltando para explorar...")
            # Força recalcular fuga para área não explorada
            historico_posicoes.clear()
            historico_posicoes.append((robo_i, robo_j))
            return

    # Movimento normal
    grid[robo_i][robo_j] = 'E'
    robo_i, robo_j = ni, nj
    grid[robo_i][robo_j] = 'R'
    visitado.add((robo_i, robo_j))
    
    # Atualiza histórico de posições
    historico_posicoes.append((robo_i, robo_j))
    if len(historico_posicoes) > MAX_HISTORICO:
        historico_posicoes.pop(0)  # Remove a mais antiga

# -----------------------
# Pygame
# -----------------------
TAM = 80

pygame.init()
tela = pygame.display.set_mode((COLUNAS * TAM, LINHAS * TAM))
pygame.display.set_caption("Robô Inteligente - Exploração Completa")

def carregar_imagem(nome):
    try:
        img = pygame.image.load(nome).convert_alpha()
        return pygame.transform.scale(img, (TAM, TAM))
    except:
        return criar_quadrado((200, 200, 200))

def criar_quadrado(cor):
    superficie = pygame.Surface((TAM, TAM))
    superficie.fill(cor)
    return superficie

imagens = {
    'R': carregar_imagem("image/robo.png"),
    'S': carregar_imagem("image/door.png"),
    'P': carregar_imagem("image/presente.png"),
    'Z': carregar_imagem("image/zombies.png"),
    'PD': carregar_imagem("image/pedra.png"),
    'E': criar_quadrado((60, 60, 60))
}

rodando = True
clock = pygame.time.Clock()

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    for i in range(LINHAS):
        for j in range(COLUNAS):
            tela.blit(imagens[grid[i][j]], (j * TAM, i * TAM))
            pygame.draw.rect(tela, (0, 0, 0), (j*TAM, i*TAM, TAM, TAM), 2)

    movimento_agente()

    pygame.display.update()
    clock.tick(10)  # 10 FPS

pygame.quit()