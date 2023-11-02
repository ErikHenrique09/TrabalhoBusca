from tools.modules import  *
import streamlit as st
import imageio
import main
import os

# Variável para controlar se o gerador já foi inicializado
gerador_inicializado = False
frame_generator = None

st.set_page_config(
    page_title="Labirynth",
    layout="wide",
)

col1, col2 = st.columns([0.5,0.5], gap="large")

with col1:
    # -=-=-==-=-=-=-=-=-==-=--==--=-=-=-=-==--=-=-=-=--=--=-=-==-=-=-=-=-=-==-=--==--=-=-=-=-==--=-=-=-=--=--=-=-==-=-=-=-=-=-==-=--==--=-=-=-=-==--=-=-=-=--=-
    st.title("Labirynth Game")
    formatacao_justify = """<p style="text-align: justify;">{}</p>"""
    formatacao_bold = """<b style="text-align: justify;">{}</b>"""
    txt1 = "O trabalho consiste em implementar um sistema de navegação automática de um agente utilizando o algoritmo de busca A* com a heuristica de distância manhattan"

    txt3 = ("""A distância de Manhattan é uma heurística que estima o custo mínimo para se mover de pos para goal em uma grade, considerando apenas movimentos na horizontal e vertical.""")

    st.write(formatacao_bold.format(txt1), unsafe_allow_html=True)

    for imagem, custo in terreno.items():

        if imagem == 'muro':
            continue
        image_path = '/'.join(images[imagem].split('/')[-2:])

        col3, col4 = st.columns([0.5,0.5], gap='small')


        col3.image(image_path, width=50)
        col4.write(f"Custo: {custo}")

    st.write(formatacao_justify.format(txt3), unsafe_allow_html=True)

    # -= -= -= = -= -= -= -= -= -= = -= - -==- -= -= -= -= -= =- -= -= -= -= - -= --=-=-==-=-=-=-=-=-==-=--==--=-=-=-=-==--=-=-=-=--=--=-=-==-=-=-=-=-=-==-=--==

    st.title("Algorithm | Labirynth Size")

    # O usuario seleciona o algoritmo
    algorithm = st.selectbox("Algorithm Select", ["A*"])

    # Seleciona o tamanho do tabuleiro
    size = st.selectbox("Product Select", ["10X10","20X20"])

    # Definições
    loops = 1
    colunas = int(size.split('X')[0])
    linhas = int(size.split('X')[1])

    # Pra 10X10 70 deu bom
    # Pra 15X15 45 deu bom

    if colunas == 10:
        screen_size = 100
        fps = 2
    elif colunas == 20:
        screen_size = 50
        fps = 4

    frame_generator = main.run_game(loops, linhas, colunas, screen_size)

    col2.title("Game")

    play = st.button("Iniciar Jogo", use_container_width=True, type="secondary")

    # Logica de exibição
    if play:
        with st.spinner("Encontrando a melhor rota..."):

            images = [x for x in frame_generator]

            imageio.mimsave('game.gif',images, fps=fps)

            col2.image('game.gif')

        st.success('Feito!')

        frame_generator = main.run_game(loops, linhas, colunas, screen_size)

        play = False

        os.remove(f"{os.path.abspath('')}\\previous_labirynth{linhas}X{colunas}.json")

    else:

        col2.image(next(frame_generator))

        st.write("Pressione o botão para iniciar o algoritmo")




