import pygame
from queue import PriorityQueue
import sys

FILAS = 6  
COLS  = 7  
ANCHO_VENTANA = 700
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Algoritmo A* (8 direcciones)")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
VERDE = (0, 200, 0)
ROJO = (200, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (64, 224, 208)

# Costes
COSTE_ORTO = 10
COSTE_DIAG = 14

class Nodo:
    def __init__(self, fila, col, ancho, total_filas, total_cols):
        self.fila = fila
        self.col = col
        self.x = col * ancho
        self.y = fila * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.total_cols = total_cols
        self.vecinos = []
        self.g = self.h = self.f = float('inf')

    def __lt__(self, other): return False
    def __eq__(self, other): return (self.fila, self.col) == (other.fila, other.col)
    def __hash__(self): return hash((self.fila, self.col))

    def get_pos(self): return self.fila, self.col
    def es_pared(self): return self.color == NEGRO
    def es_inicio(self): return self.color == NARANJA
    def es_fin(self): return self.color == PURPURA

    def restablecer(self): self.color = BLANCO
    def hacer_inicio(self): self.color = NARANJA
    def hacer_cerrado(self): self.color = ROJO
    def hacer_abierto(self): self.color = VERDE
    def hacer_pared(self): self.color = NEGRO
    def hacer_camino(self): self.color = AZUL
    def hacer_fin(self): self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = self.fila + dr, self.col + dc
                if 0 <= r < self.total_filas and 0 <= c < self.total_cols:
                    if not grid[r][c].es_pared():
                        self.vecinos.append(grid[r][c])

def heuristica(p1, p2):
    (r1, c1), (r2, c2) = p1, p2
    dx, dy = abs(c1 - c2), abs(r1 - r2)
    return COSTE_ORTO * (dx + dy) + (COSTE_DIAG - 2 * COSTE_ORTO) * min(dx, dy)

def reconstruir_camino(came_from, actual, dibujar):
    while actual in came_from:
        actual = came_from[actual]
        if not actual.es_inicio():
            actual.hacer_camino()
        dibujar()

def algoritmo_a_estrella(dibujar, grid, inicio, fin):
    for fila in grid:
        for nodo in fila:
            nodo.g = nodo.h = nodo.f = float('inf')

    contador = 0
    open_set = PriorityQueue()
    inicio.g = 0
    inicio.h = heuristica(inicio.get_pos(), fin.get_pos())
    inicio.f = inicio.g + inicio.h
    open_set.put((inicio.f, contador, inicio))
    came_from = {}
    open_set_hash = {inicio}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        actual = open_set.get()[2]
        open_set_hash.remove(actual)

        if actual == fin:
            reconstruir_camino(came_from, fin, dibujar)
            fin.hacer_fin()
            inicio.hacer_inicio()
            return True

        for vecino in actual.vecinos:
            dr, dc = abs(vecino.fila - actual.fila), abs(vecino.col - actual.col)
            coste = COSTE_DIAG if (dr == 1 and dc == 1) else COSTE_ORTO
            temp_g = actual.g + coste

            if temp_g < vecino.g:
                came_from[vecino] = actual
                vecino.g = temp_g
                vecino.h = heuristica(vecino.get_pos(), fin.get_pos())
                vecino.f = vecino.g + vecino.h
                if vecino not in open_set_hash:
                    contador += 1
                    open_set.put((vecino.f, contador, vecino))
                    open_set_hash.add(vecino)
                    if not vecino.es_fin():
                        vecino.hacer_abierto()

        dibujar()
        if not actual.es_inicio():
            actual.hacer_cerrado()

    return False

def crear_grid(filas, cols, ancho):
    grid = []
    tam = ancho // max(filas, cols)
    for r in range(filas):
        grid.append([])
        for c in range(cols):
            grid[r].append(Nodo(r, c, tam, filas, cols))
    return grid

def dibujar_grid(ventana, filas, cols, ancho):
    tam = ancho // max(filas, cols)
    for c in range(cols+1):
        pygame.draw.line(ventana, GRIS, (c*tam, 0), (c*tam, tam*filas))
    for r in range(filas+1):
        pygame.draw.line(ventana, GRIS, (0, r*tam), (tam*cols, r*tam))

def dibujar(ventana, grid, filas, cols, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_grid(ventana, filas, cols, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, cols, ancho):
    tam = ancho // max(filas, cols)
    x, y = pos
    return y // tam, x // tam

def main(ventana, ancho):
    grid = crear_grid(FILAS, COLS, ancho)
    inicio = fin = None
    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, COLS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                fila, col = obtener_click_pos(pygame.mouse.get_pos(), FILAS, COLS, ancho)
                nodo = grid[fila][col]
                if event.button == 1:
                    if not inicio and nodo != fin:
                        inicio = nodo
                        inicio.hacer_inicio()
                    elif not fin and nodo != inicio:
                        fin = nodo
                        fin.hacer_fin()
                    elif nodo != inicio and nodo != fin:
                        nodo.hacer_pared()
                elif event.button == 3:
                    nodo.restablecer()
                    if nodo == inicio: inicio = None
                    elif nodo == fin: fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)
                    algoritmo_a_estrella(lambda: dibujar(ventana, grid, FILAS, COLS, ancho), grid, inicio, fin)

                if event.key == pygame.K_c:
                    inicio = fin = None
                    grid = crear_grid(FILAS, COLS, ancho)

    pygame.quit()

if __name__ == "__main__":
    main(VENTANA, ANCHO_VENTANA)
