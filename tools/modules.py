import os.path

import pygame
import sys
import numpy
from time import sleep
import random
import imageio
from collections import deque

PATH = os.path.abspath('').replace('\\','/')

# Estrutura de terreno

terreno = {
   "solidoplano": 1,
   "arenoso": 4,
   "rochoso": 10,
   "pantano": 20,
   "muro": float("inf")
}

images = {
   "solidoplano": PATH+'/images/terreno_solido_plano.png',
   "rochoso": PATH+'/images/terreno_rochoso.png',
   "arenoso": PATH+'/images/terreno_arenoso.png',
   "pantano": PATH+'/images/terreno_pantano.png',
   "muro": PATH+'/images/terreno_muro.png',
   "final": PATH+'/images/final_path.png',
   "start": PATH+'/images/start_terren.png'
}


# Os tipos de terrenos que compõem o ambiente são:
#   Solido e plano – Custo: +1
#   Rochoso – Custo: +10
#   Arenosos– Custo: +4
#   Pântano – Custo: +20

# Estrutura de terreno

# Cada nó do grafo tera a seguinte estrutura
# nó padrao =
#   {
#       "id": 0             ,
#       "custo": terreno["solidoplano"],
#       "CustoHeuristico": 4,
#       "left":             ,
#       "right":            ,
#       "up":               ,
#       "down":             ,
#   }
