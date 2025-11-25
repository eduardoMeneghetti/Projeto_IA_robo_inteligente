import pygame
import random
from collections import deque

# CONFIGURAÇÕES INICIAIS
LINHAS = 6
COLUNAS = 6
QTD_PRESENTES = random.randint(3, 9)
QTD_ZUMBIS = 3
QTD_PEDRAS = 4

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

    # Porta
    i, j = posicoes.pop()
    grid[i][j] = 'S'

    # Robô
    i, j = posicoes.pop()
    grid[i][j] = 'R'

    # Pedras
    for _ in range(QTD_PEDRAS):
        i, j = posicoes.pop()
        grid[i][j] = 'PD'

    return grid


# GERAR MAPA 
grid = gerar_grid()

# LOCALIZAR ROBÔ E PORTA
porta_pos = None
for i in range(LINHAS):
    for j in range(COLUNAS):
        if grid[i][j] == 'R':
            robo_l, robo_c = i, j
        if grid[i][j] == 'S':
            porta_pos = (i, j)

grid[robo_l][robo_c] = 'E'
posicao_inicial_robo = (robo_l, robo_c)


direcoes = [
    ("CIMA", -1, 0),
    ("BAIXO", 1, 0),
    ("ESQUERDA", 0, -1),
    ("DIREITA", 0, 1)
]


visitadas = set()
conhecidas = set()  
bloqueios_conhecidos = set() 
presentes_coletados = set()
pontos = 0
qtd_presentes_encontrados = 0

ultimos_passos = deque(maxlen=10)
posicao_anterior = None
mortes_por_zumbi = 0
movimentos_sem_progresso = 0
caminho_planejado = []


def bfs_encontrar_caminho(origem, destino, bloqueios):
    """Encontra o caminho mais curto usando BFS, evitando bloqueios conhecidos"""
    if origem == destino:
        return []
    
    fila = deque([(origem, [])])
    visitados_bfs = {origem}
    
    while fila:
        (l, c), caminho = fila.popleft()
        
        for nome, dl, dc in direcoes:
            nl, nc = l + dl, c + dc
            
            # Verifica limites
            if not (0 <= nl < LINHAS and 0 <= nc < COLUNAS):
                continue
            
            # Pula se já visitou no BFS
            if (nl, nc) in visitados_bfs:
                continue
            
            # Pula se é bloqueio conhecido
            if (nl, nc) in bloqueios:
                continue
            
            novo_caminho = caminho + [(nl, nc)]
            
            # Chegou no destino!
            if (nl, nc) == destino:
                return novo_caminho
            
            visitados_bfs.add((nl, nc))
            fila.append(((nl, nc), novo_caminho))
    
    return None  # Não há caminho


def dfs_mapear_alcancaveis(pos_inicial, bloqueios):
    """Mapeia todas as células alcançáveis a partir da posição inicial"""
    alcancaveis = set()
    pilha = [pos_inicial]
    explorados = {pos_inicial}
    
    while pilha:
        l, c = pilha.pop()
        
        if (l, c) not in bloqueios:
            alcancaveis.add((l, c))
        
        for _, dl, dc in direcoes:
            nl, nc = l + dl, c + dc
            
            if not (0 <= nl < LINHAS and 0 <= nc < COLUNAS):
                continue
            
            if (nl, nc) in explorados:
                continue
            
            explorados.add((nl, nc))
            
            if (nl, nc) in bloqueios:
                continue
            
            pilha.append((nl, nc))
    
    return alcancaveis


def encontrar_celula_nao_visitada_mais_proxima_com_bloqueios(bloqueios):
    """Encontra a célula não visitada mais próxima usando BFS"""
    alcancaveis = dfs_mapear_alcancaveis((robo_l, robo_c), bloqueios)
    nao_visitadas = alcancaveis - visitadas
    
    if not nao_visitadas:
        return None
    
    # BFS para encontrar a mais próxima
    fila = deque([((robo_l, robo_c), 0)])
    visitados_busca = {(robo_l, robo_c)}
    
    while fila:
        (l, c), dist = fila.popleft()
        
        # Se encontrou uma não visitada, retorna
        if (l, c) in nao_visitadas:
            return (l, c)
        
        for _, dl, dc in direcoes:
            nl, nc = l + dl, c + dc
            
            if not (0 <= nl < LINHAS and 0 <= nc < COLUNAS):
                continue
            
            if (nl, nc) in visitados_busca:
                continue
            
            if (nl, nc) in bloqueios:
                continue
            
            visitados_busca.add((nl, nc))
            fila.append(((nl, nc), dist + 1))
    
    return None


def encontrar_celula_nao_visitada_mais_proxima():
    """Encontra a célula não visitada mais próxima usando BFS (sem bloqueios temporários)"""
    return encontrar_celula_nao_visitada_mais_proxima_com_bloqueios(bloqueios_conhecidos)


def mover_robo():
    global robo_l, robo_c, pontos, qtd_presentes_encontrados, posicao_anterior
    global movimentos_sem_progresso, caminho_planejado

    visitadas.add((robo_l, robo_c))
    conhecidas.add((robo_l, robo_c))
    
    # Verifica se existe caminho planejado
    if caminho_planejado:
        proximo = caminho_planejado.pop(0)
        nl, nc = proximo
    else:
        # Calcula células alcançáveis
        bloqueios_temporarios = bloqueios_conhecidos.copy()
        
        # Se a porta já foi encontrada mas ainda há exploração, trata como bloqueio temporário
        if porta_pos and porta_pos in conhecidas:
            alcancaveis_teste = dfs_mapear_alcancaveis((robo_l, robo_c), bloqueios_conhecidos)
            nao_visitadas_teste = alcancaveis_teste - visitadas - {porta_pos}
            if len(nao_visitadas_teste) > 0:
                bloqueios_temporarios.add(porta_pos)
        
        alcancaveis = dfs_mapear_alcancaveis((robo_l, robo_c), bloqueios_temporarios)
        nao_visitadas = alcancaveis - visitadas
        tudo_explorado = len(nao_visitadas) == 0
        
        if tudo_explorado:
            print(f"✅ Tudo explorado! (Visitadas: {len(visitadas)}, Alcançáveis: {len(alcancaveis)})")
            # Ir para a porta
            if porta_pos and porta_pos in conhecidas:
                # Recalcula sem bloqueio temporário para ir à porta
                caminho_planejado = bfs_encontrar_caminho((robo_l, robo_c), porta_pos, bloqueios_conhecidos)
                if caminho_planejado:
                    print(f"Indo para a porta! Caminho: {len(caminho_planejado)} passos")
                    proximo = caminho_planejado.pop(0)
                    nl, nc = proximo
                else:
                    print("Sem caminho para a porta!")
                    return True
            else:
                print("Porta não encontrada ou não alcançável!")
                return True
        else:
            # Encontrar célula não visitada mais próxima
            celula_alvo = encontrar_celula_nao_visitada_mais_proxima_com_bloqueios(bloqueios_temporarios)
            
            if celula_alvo:
                # Planejar caminho até lá
                caminho_planejado = bfs_encontrar_caminho((robo_l, robo_c), celula_alvo, bloqueios_temporarios)
                
                if caminho_planejado:
                    print(f"Planejando caminho para célula não visitada {celula_alvo}: {len(caminho_planejado)} passos")
                    proximo = caminho_planejado.pop(0)
                    nl, nc = proximo
                else:
                    # Se não há caminho, escolhe movimento local
                    print(f"Sem caminho para {celula_alvo}, escolhendo movimento local")
                    melhor_movimento = escolher_movimento_local()
                    if melhor_movimento is None:
                        return True
                    nl, nc, _ = melhor_movimento
            else:
                print("Nenhuma célula não visitada encontrada")
                return True

    # Executar movimento
    conteudo = grid[nl][nc]
    
    ultimos_passos.append((nl, nc))
    posicao_anterior = (robo_l, robo_c)

    # Descobrir o que tem em cada espaço
    if conteudo == 'Z':
        pontos -= 20
        print(f"DESCOBRIU um Zumbi em {(nl, nc)}! -20 pontos (Total: {pontos})")
        bloqueios_conhecidos.add((nl, nc))
        conhecidas.add((nl, nc))
        caminho_planejado.clear()  # Limpa o caminho
        aciona_morte_robo()
        return False

    if conteudo == 'PD':
        pontos -= 5
        print(f"DESCOBRIU uma Pedra em {(nl, nc)}! -5 pontos (Total: {pontos})")
        bloqueios_conhecidos.add((nl, nc))
        conhecidas.add((nl, nc))
        caminho_planejado.clear()  # Limpa o caminho
        return False

    if conteudo == 'P':
        pontos += 10
        qtd_presentes_encontrados += 1
        print(f"Presente coletado em {(nl, nc)}! +10 pontos (Total: {pontos})")
        presentes_coletados.add((nl, nc))
        grid[nl][nc] = 'E'

    if conteudo == 'S':
        conhecidas.add((nl, nc))
        # Calcula do ponto ATUAL (antes de mover), não da porta
        alcancaveis = dfs_mapear_alcancaveis((robo_l, robo_c), bloqueios_conhecidos)
        nao_visitadas = alcancaveis - visitadas - {(nl, nc)}  # Exclui a própria porta
        
        if len(nao_visitadas) == 0:
            pontos += 50
            print(f"Porta alcançada! Explorou tudo! +50 pontos (Total: {pontos})")
            robo_l, robo_c = nl, nc  # Move para a porta
            return True
        else:
            pontos -= 10
            print(f"Porta muito cedo! Ainda faltam {len(nao_visitadas)} células. -10 pontos (Total: {pontos})")
            print(f"Não entrando na porta ainda. Continuando exploração...")
            caminho_planejado.clear()
            # NÃO move para a porta, fica onde está
            return False

    # Movimento normal - AGORA O ROBÔ SE MOVE
    robo_l, robo_c = nl, nc
    movimentos_sem_progresso = 0
    
    return False


def escolher_movimento_local():
    """Escolhe o melhor movimento baseado em heurísticas locais"""
    melhor_pontuacao = -999999
    melhor_movimento = None

    for nome, dl, dc in direcoes:
        nl = robo_l + dl
        nc = robo_c + dc
        
        if not (0 <= nl < LINHAS and 0 <= nc < COLUNAS):
            continue

        conteudo = grid[nl][nc]
        pontuacao_temp = 0
        
        # Prioriza não visitadas
        if (nl, nc) not in visitadas:
            pontuacao_temp += 2000
            
        # Evita bloqueios conhecidos
        if (nl, nc) in bloqueios_conhecidos:
            pontuacao_temp -= 99999
        
        # Evita voltar
        if posicao_anterior == (nl, nc):
            pontuacao_temp -= 600
        
        # Penaliza loops (movimentos repetidos recentes)
        repeticoes = ultimos_passos.count((nl, nc))
        pontuacao_temp -= repeticoes * 400

        if pontuacao_temp > melhor_pontuacao:
            melhor_pontuacao = pontuacao_temp
            melhor_movimento = (nl, nc, conteudo)

    return melhor_movimento


def aciona_morte_robo():
    global robo_l, robo_c, mortes_por_zumbi, movimentos_sem_progresso
    mortes_por_zumbi += 1
    movimentos_sem_progresso = 0
    print(f"Robô reiniciado na posição inicial. Total de mortes: {mortes_por_zumbi}")
    robo_l, robo_c = posicao_inicial_robo
    ultimos_passos.clear()

# ----- PYGAME -----
TAM = 80

pygame.init()
tela = pygame.display.set_mode((COLUNAS * TAM, LINHAS * TAM))
pygame.display.set_caption("Robô Explorador - Exploração Completa")


def criar_quadrado(cor):
    superficie = pygame.Surface((TAM, TAM))
    superficie.fill(cor)
    return superficie


def carregar_imagem(nome):
    try:
        img = pygame.image.load(nome).convert_alpha()
        return pygame.transform.scale(img, (TAM, TAM))
    except:
        return criar_quadrado((200, 200, 200))


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
passos_totais = 0
MAX_PASSOS = 500  # Limite de segurança para evitar loops infinitos

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    passos_totais += 1
    
    if passos_totais > MAX_PASSOS:
        print(f"\n⚠️ Limite de {MAX_PASSOS} passos atingido!")
        rodando = False
        continue

    jogo_acabou = mover_robo()
    if jogo_acabou:
        print(f"\n{'='*40}")
        print(f"🏁 FIM DE JOGO")
        print(f"Pontuação final: {pontos}")
        print(f"Presentes coletados: {qtd_presentes_encontrados}/{QTD_PRESENTES}")
        print(f"Mortes por zumbi: {mortes_por_zumbi}")
        print(f"Células conhecidas: {len(conhecidas)}")
        print(f"Células visitadas: {len(visitadas)}")
        print(f"Bloqueios descobertos: {len(bloqueios_conhecidos)}")
        print(f"Passos totais: {passos_totais}")
        print(f"{'='*40}\n")
        rodando = False

    for i in range(LINHAS):
        for j in range(COLUNAS):
            tela.blit(imagens[grid[i][j]], (j * TAM, i * TAM))
            pygame.draw.rect(tela, (0, 0, 0), (j * TAM, i * TAM, TAM, TAM), 2)

    tela.blit(imagens['R'], (robo_c * TAM, robo_l * TAM))

    pygame.display.update()
    clock.tick(5)

pygame.quit()