import heapq
from tools.modules import *

def check_labirynth(labirynth, msg):
    print(f"\033[91m |||||||||||||||||||||||||||||||||||||||{msg}|||||||||||||||||||||||||||||||||||||| \033[0m")

    for nrow, row in enumerate(labirynth):
        for nnode, node in enumerate(row):
            if node['right'] is None and node['left'] is None and node['down'] is None and node['top'] is None:
                print(f'[{nrow}, {nnode}] NONE |', end='')

    print(f"\033[91m \n |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| \033[0m")

# Heurística de distância manhattan
def heuristic(pos, goal):

    """A distância de Manhattan é uma heurística que estima o custo
     mínimo para se mover de pos para goal em uma grade, considerando
      apenas movimentos na horizontal e vertical."""

    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def apply_heuristic(labyrinth, goal):
    for row in labyrinth:
        for node in row:
            l, c = labyrinth.index(row), row.index(node)
            node["CustoHeuristico"] = heuristic([l,c], goal)
    return labyrinth


def A_STAR(labyrinth, node_start, node_goal):
# Função de busca A*
    open_set = [(0, node_start)]
    came_from = {}
    g_score = {node['id']: float('inf') for row in labyrinth for node in row}
    g_score[node_start['id']] = 0
    moves = {node_start['id']: ""}  # Rastreia os movimentos associados a cada nó
    x = 1

    while len(open_set) != 0:

        current = heapq.heappop(open_set)

        if isinstance(current[1], dict):
            current = current[1]
        elif isinstance(current[2], dict):
            current = current[2]
        else:
            continue

        if current['id'] == node_goal['id']:
            cost_path = []
            path_moves = []  # Rastreia os movimentos do caminho

            while current['id'] in came_from.keys():
                cost_path.insert(0, (current['custo']+current['CustoHeuristico']))
                path_moves.insert(0, moves[current['id']])
                current = came_from[current['id']]
            print("Vamo retorna")
            return cost_path, path_moves


        # Atualizando os pesos
        for direction in ["left", "right", "top", "down"]:

            neighbor = current[direction]

            # Evitar dar de cara nas bordas do mapa
            if isinstance(neighbor, dict):
                #print(g_score)
                tentative_g_score = g_score[current['id']] + neighbor['custo']

                if tentative_g_score < g_score[neighbor['id']]:

                    # Atualizando aqueles pesos +inf
                    came_from[neighbor['id']] = current
                    g_score[neighbor['id']] = tentative_g_score

                    # Importantissimo, aqui que controlamos a decisão do A*
                    f_score = tentative_g_score + heuristic(neighbor['pos'], node_goal['pos'])

                    heapq.heappush(open_set, (f_score, neighbor['id'], neighbor))

                    # Atualize os movimentos para o vizinho
                    moves[neighbor['id']] = direction

    return None


def new_no(id=0, terra="solidoplano", pos=[], custoheuristico=1, left="", right="", top="", down=""):
    return {
        "id": id,
        "pos": pos,
        "custo": terreno[terra],
        "CustoHeuristico": custoheuristico,
        "left": left,
        "right": right,
        "top": top,
        "down": down,
        "terreno":terra,
        "image":images[terra],
    }


# Função para sortear terreno de forma enviesada
def sortear_terreno(probabilidade_solidoplano=0.5):
    if random.random() < probabilidade_solidoplano:
        return "solidoplano"
    else:
        return random.choice(list(terreno.keys())[1:])  # Escolhe aleatoriamente entre os terrenos restantes excluindo "solidoplano"


def reformat_labyrinth(lab_reformat, reforma=True):

    if reforma:
        for x in lab_reformat:
            for y in x:
                y['top'] = None
                y['down'] = None
                y['left'] = None
                y['right'] = None

    else:
        print('|||'*40)
        print("Entramo no else")
        print('|||' * 40)
        for x in range(len(lab_reformat)):
            for y in range(len(lab_reformat[0])):
                # x = linha
                # y = coluna

                if x != 0:
                    if lab_reformat[x - 1][y]["terreno"] != "muro":
                        lab_reformat[x][y]["top"] = lab_reformat[x - 1][y]

                if x != len(lab_reformat) - 1:
                    if lab_reformat[x + 1][y]["terreno"] != "muro":
                        lab_reformat[x][y]["down"] = lab_reformat[x + 1][y]

                if y != 0:
                    if lab_reformat[x][y - 1]["terreno"] != "muro":
                        lab_reformat[x][y]["left"] = lab_reformat[x][y - 1]

                if y != len(lab_reformat[0]) - 1:
                    if lab_reformat[x][y + 1]["terreno"] != "muro":
                        lab_reformat[x][y]["right"] = lab_reformat[x][y + 1]

    return lab_reformat

# Função para criar um labirinto

def create_labyrinth(i=6, j=5):

    """Criando uma matriz de nós e os interligando"""
    labirynth = []
    ids = 0

    for l in range(i):
        lab = []
        for c in range(j):
            lab.append(new_no(id = ids, pos=[l, c],terra=sortear_terreno()))
            ids += 1
        labirynth.append(lab)

    # Conectar os nós
    for x in range(i):
        for y in range(j):
            # x = linha
            # y = coluna

            if x != 0:
                if labirynth[x-1][y]["terreno"] != "muro":
                    labirynth[x][y]["top"] = labirynth[x-1][y]

            if x != i-1:
                if labirynth[x+1][y]["terreno"] != "muro":
                    labirynth[x][y]["down"] = labirynth[x+1][y]

            if y != 0:
                if labirynth[x][y-1]["terreno"] != "muro":
                    labirynth[x][y]["left"] = labirynth[x][y-1]

            if y != j-1:
                if labirynth[x][y+1]["terreno"] != "muro":
                    labirynth[x][y]["right"] = labirynth[x][y+1]

    check_labirynth(labirynth, 'Dentro mas depois da criação')

    return labirynth


# Desenha o labirinto
def draw_labyrinth():
    x = 6
    y = 5

    # Configurações da tela e célula
    largura_tela = 600
    altura_tela = 500
    largura_celula = largura_tela // 5  # 5 colunas
    altura_celula = altura_tela // 6  # 6 linhas


    return