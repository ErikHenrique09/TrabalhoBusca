import os
import copy
import json
import streamlit as st
from tools.func import *
from tools.classes import *

def sort_final_start(labirinto, linhas, colunas):

    l_ini, l_fim = 0, linhas-1#random.randint(0, linhas - 1), random.randint(0, linhas - 1)
    c_ini, c_fim = 0, colunas-1#random.randint(0, colunas - 1), random.randint(0, colunas - 1)

    #while True:
        #l_fim, c_fim = random.randint(0, linhas - 1), random.randint(0, colunas - 1)
        #if l_fim != l_ini or c_fim != c_ini:
            #break

    labirinto[l_ini][c_ini]['terreno'] = 'start'
    labirinto[l_ini][c_ini]['image'] = images['start']

    labirinto[l_fim][c_fim]['custo'] = 0
    labirinto[l_fim][c_fim]['custoheuristico'] = 0
    labirinto[l_fim][c_fim]['terreno'] = 'final'
    labirinto[l_fim][c_fim]['image'] = images['final']

    return labirinto[l_ini][c_ini], labirinto[l_fim][c_fim]

def draw_labyrinth(tela, labirinto, screen_config):
    for i in range(screen_config['linhas']):
        for j in range(screen_config['colunas']):
            terreno = labirinto[i][j]["terreno"]
            imagem = pygame.image.load(images[terreno])
            imagem_redimensionada = pygame.transform.scale(imagem, (screen_config['largura_celula'], screen_config['altura_celula']))
            tela.blit(imagem_redimensionada, (j * screen_config['largura_celula'], i * screen_config['altura_celula']))

def generate_screen_config(colunas=10, linhas=10, screen_size=100):
    return {
        "linhas": linhas,
        "colunas": colunas,
        # Configurações da tela e célula
        "largura_tela": colunas * screen_size,
        "altura_tela": linhas * screen_size,
        "largura_celula": colunas*screen_size // colunas,
        "altura_celula": linhas*screen_size // linhas,
        "largura_altura_tela":(colunas*screen_size, linhas*screen_size),
        # Defina cores
        "branco": (255, 255, 255)
    }


def run_game(loops, linhas, colunas, screen_size):
    # Inicializa o pygame
    pygame.init()

    #informações da tela
    screen_config = generate_screen_config(colunas, linhas, screen_size)

    # Inicialize a tela
    tela = pygame.display.set_mode(screen_config['largura_altura_tela'])
    pygame.display.iconify()

    if f'previous_labirynth{linhas}X{colunas}.json' not in os.listdir(os.path.abspath('')):

        # Crie o labirinto
        labirinto = create_labyrinth(screen_config['linhas'], screen_config['colunas'])

        l2 = copy.deepcopy(labirinto)
        l2 = reformat_labyrinth(l2.copy())

        # Converte a lista em uma string JSON
        json_string = json.dumps(l2,indent=4)

        # Escreve a string JSON em um arquivo
        with open(f"previous_labirynth{linhas}X{colunas}.json", "w") as arquivo:
            arquivo.write(json_string)

        arquivo.close()
    else:
        with open(f"previous_labirynth{linhas}X{colunas}.json", "r") as arquivo:
            # Leia o conteúdo do arquivo (string JSON)
            json_string = arquivo.read()

            # Analise a string JSON de volta para uma lista
            l2 = json.loads(json_string)
        arquivo.close()

        labirinto = l2.copy()

        labirinto = reformat_labyrinth(labirinto, reforma=False).copy()

    # Sorteando inicio e fim
    node_ini, node_goal = sort_final_start(labirinto, screen_config['linhas'], screen_config['colunas'])

    # Aplica a heuristica
    labirinto = apply_heuristic(labirinto, node_goal['pos'])

    try:
        cost_path, move_paths = A_STAR(labirinto, node_ini, node_goal)
        actions = move_paths
        actions.insert(0, 'draw')

    except:
        st.warning("Não foram encontradas soluções coerentes")
        pass

    agente = Agente(labirinto, node_ini['pos'])
    progress = 0
    # Loop principal
    for action in actions:

        #sleep(0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Desenhe o labirinto
        tela.fill(screen_config['branco'])
        draw_labyrinth(tela, labirinto, screen_config)

        # Desenhe o agente na nova posição
        # Suponha que a posição do agente seja agente.posicao

        if action != 'draw':
            # Mova o agente (exemplo: mover para a direita)
            agente.mover(action)

        pygame.draw.circle(
            tela,
            color=(255, 0, 0), # Cor da bola
            center=(
                        agente.posicao[1] * screen_config['largura_celula'] + screen_config['largura_celula'] // 2,
                        agente.posicao[0] * screen_config['altura_celula'] + screen_config['altura_celula'] // 2
                ),
            radius=screen_config['largura_celula']//2
        )

        # Bagulho virou um gerador de frames
        yield pygame.surfarray.array3d(tela)

    pygame.quit()


#run_game(1)