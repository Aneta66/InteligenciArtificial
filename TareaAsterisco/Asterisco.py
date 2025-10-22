import pygame
import math
from queue import PriorityQueue
import sys

FILAS = 6  
COLS  = 7  
ANCHO_VENTANA = 700
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Algoritmo A* - Visualizador (8 direcciones)")


BLANCO  = (255, 255, 255)
NEGRO   = (0, 0, 0)
GRIS    = (200, 200, 200)
VERDE   = (0, 200, 0)     # abiertos
ROJO    = (200, 0, 0)     # cerrados
NARANJA = (255, 165, 0)   # inicio
PURPURA = (128, 0, 128)   # fin
AZUL    = (64, 224, 208)  # camino
AMARILLO= (255, 255, 0)

# Costes
COST_ARR_ABA = 10
COST_DIAG  = 14

# Fuente para texto en nodos
pygame.font.init()
FONT = pygame.font.SysFont('consolas', 12)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas, total_cols):
        self.fila = fila
        self.col = col
        self.x = col * ancho   # nota: x es columna
        self.y = fila * ancho  # y es fila
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.total_cols = total_cols
        self.vecinos = []
        # valores para mostrar
        self.g = float('inf')
        self.h = float('inf')
        self.f = float('inf')

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return isinstance(other, Nodo) and (self.fila, self.col) == (other.fila, other.col)

    def __hash__(self):
        return hash((self.fila, self.col))

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO
        self.g = self.h = self.f = float('inf')

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_cerrado(self):
        self.color = ROJO

    def hacer_abierto(self):
        self.color = VERDE

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_camino(self):
        self.color = AZUL

    def hacer_fin(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        # rect
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        # si hay valores, dibujarlos en pequeño
        if self.g != float('inf'):
            g_surf = FONT.render(f"G:{int(self.g)}", True, (0,0,0))
            ventana.blit(g_surf, (self.x + 3, self.y + 2))
        if self.h != float('inf'):
            h_surf = FONT.render(f"H:{int(self.h)}", True, (0,0,0))
            ventana.blit(h_surf, (self.x + 3, self.y + 14))
        if self.f != float('inf'):
            f_surf = FONT.render(f"F:{int(self.f)}", True, (0,0,0))
            ventana.blit(f_surf, (self.x + 3, self.y + 26))

    def actualizar_vecinos(self, grid):
        # 8 direcciones (incluye diagonales)
        self.vecinos = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r = self.fila + dr
                c = self.col + dc
                if 0 <= r < self.total_filas and 0 <= c < self.total_cols:
                    if not grid[r][c].es_pared():
                        self.vecinos.append(grid[r][c])


def heuristica_octile(p1, p2):
    # Heurística admisible para costes ortogonal=10, diagonal=14 (octile)
    (r1, c1) = p1
    (r2, c2) = p2
    dx = abs(c1 - c2)
    dy = abs(r1 - r2)
    # D = 10, D2 = 14
    D = COST_ARR_ABA
    D2 = COST_DIAG
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    # equivalencia: return D * max(dx, dy) + (D2 - D) * min(dx, dy) -- pero la fórmula de arriba es correcta

def reconstruir_camino(came_from, actual, dibujar):
    while actual in came_from:
        actual = came_from[actual]
        if not actual.es_inicio():
            actual.hacer_camino()
        dibujar()

def algoritmo_a_estrella(dibujar, grid, inicio, fin):
    # limpias valores previos
    for fila in grid:
        for nodo in fila:
            nodo.g = nodo.h = nodo.f = float('inf')

    contador = 0
    open_set = PriorityQueue()
    inicio.g = 0
    inicio.h = heuristica_octile(inicio.get_pos(), fin.get_pos())
    inicio.f = inicio.g + inicio.h
    open_set.put((inicio.f, contador, inicio))
    came_from = {}
    open_set_hash = {inicio}
    closed_list_order = []          # LC: orden de expansión
    open_snapshots = []             # LA snapshots (listas de nodos en algebraico) por cada expansión

    # Para imprimir legalmente en forma legible, función helper:
    def alg(nodo):
        # columnas alfabeticas si cols<=26, si no usar c#
        col = nodo.col + 1
        row = nodo.fila + 1
        if COLS <= 26:
            letra = chr(ord('A') + nodo.col)
            return f"{letra}{row}"
        else:
            return f"c{col}r{row}"

    while not open_set.empty():
        # guardamos snapshot actual de LA (con nombres)
        open_snapshot = [alg(n) for _,_,n in open_set.queue]
        open_snapshots.append(open_snapshot)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        if current not in open_set_hash:
            # ya fue gestionado antes
            continue
        open_set_hash.remove(current)
        # añadir a LC
        closed_list_order.append(current)

        # marcar actual como cerrado (si no es inicio)
        if not current.es_inicio():
            current.hacer_cerrado()

        # si llegamos a la meta reconstruimos
        if current == fin:
            reconstruir_camino(came_from, fin, dibujar)
            fin.hacer_fin()
            inicio.hacer_inicio()
            # imprimir LA y LC en consola
            print("\n--- Lista abierta (LA) snapshots (por expansión) ---")
            for i, snap in enumerate(open_snapshots):
                print(f"expansión {i+1}: {snap}")
            print("\n--- Lista cerrada (LC) orden de expansión ---")
            print([ ( (chr(ord('A')+n.col) + str(n.fila+1)) if COLS<=26 else f"c{n.col+1}r{n.fila+1}") for n in closed_list_order ])
            return True

        # explorar vecinos
        for vecino in current.vecinos:
            # coste del movimiento entre current y vecino
            dr = abs(vecino.fila - current.fila)
            dc = abs(vecino.col - current.col)
            if dr == 1 and dc == 1:
                move_cost = COST_DIAG
            else:
                move_cost = COST_ARR_ABA

            tentative_g = current.g + move_cost
            if tentative_g < vecino.g:
                came_from[vecino] = current
                vecino.g = tentative_g
                vecino.h = heuristica_octile(vecino.get_pos(), fin.get_pos())
                vecino.f = vecino.g + vecino.h
                if vecino not in open_set_hash:
                    contador += 1
                    open_set.put((vecino.f, contador, vecino))
                    open_set_hash.add(vecino)
                    if not vecino.es_fin():
                        vecino.hacer_abierto()

        dibujar()

    # si se vacía la open_set sin hallar fin:
    print("No se encontró camino.")
    return False

def crear_grid(filas, cols, ancho):
    grid = []
    ancho_nodo = ancho // max(filas, cols)
    for r in range(filas):
        grid.append([])
        for c in range(cols):
            nodo = Nodo(r, c, ancho_nodo, filas, cols)
            grid[r].append(nodo)
    return grid

def dibujar_grid(ventana, filas, cols, ancho):
    ancho_nodo = ancho // max(filas, cols)
    # verticales
    for c in range(cols+1):
        x = c * ancho_nodo
        pygame.draw.line(ventana, GRIS, (x, 0), (x, ancho_nodo * filas))
    # horizontales
    for r in range(filas+1):
        y = r * ancho_nodo
        pygame.draw.line(ventana, GRIS, (0, y), (ancho_nodo * cols, y))

def dibujar(ventana, grid, filas, cols, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)
    dibujar_grid(ventana, filas, cols, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, cols, ancho):
    ancho_nodo = ancho // max(filas, cols)
    x, y = pos
    col = x // ancho_nodo
    fila = y // ancho_nodo
    # límites
    if fila < 0: fila = 0
    if fila >= filas: fila = filas - 1
    if col < 0: col = 0
    if col >= cols: col = cols - 1
    return fila, col

def main(ventana, ancho):
    grid = crear_grid(FILAS, COLS, ancho)

    inicio = None
    fin = None

    corriendo = True

    instrucciones = True
    print("\nINSTRUCCIONES:")
    print("- Click izquierdo: primer click = inicio (naranja), segundo click = fin (púrpura), siguientes = paredes (negro).")
    print("- Click derecho: borrar casilla.")
    print("- Barra espacio: ejecutar A* (8 direcciones, orto=10, diag=14).")
    print("- C: limpiar tablero.\n")

    while corriendo:
        dibujar(ventana, grid, FILAS, COLS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            # usar get_pressed() aquí puede repetir acciones al mantener presionado,
            # por eso procesamos clics sólo cuando detectamos MOUSEBUTTONDOWN
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # izquierdo
                    pos = pygame.mouse.get_pos()
                    fila, col = obtener_click_pos(pos, FILAS, COLS, ancho)
                    nodo = grid[fila][col]
                    if not inicio and nodo != fin:
                        inicio = nodo
                        inicio.hacer_inicio()
                    elif not fin and nodo != inicio:
                        fin = nodo
                        fin.hacer_fin()
                    elif nodo != fin and nodo != inicio:
                        nodo.hacer_pared()
                elif event.button == 3:  # derecho
                    pos = pygame.mouse.get_pos()
                    fila, col = obtener_click_pos(pos, FILAS, COLS, ancho)
                    nodo = grid[fila][col]
                    nodo.restablecer()
                    if nodo == inicio:
                        inicio = None
                    elif nodo == fin:
                        fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    # actualizar vecinos
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)
                    # ejecutar A*
                    algoritmo_a_estrella(lambda: dibujar(ventana, grid, FILAS, COLS, ancho), grid, inicio, fin)

                if event.key == pygame.K_c:
                    inicio = None
                    fin = None
                    grid = crear_grid(FILAS, COLS, ancho)

     
    pygame.quit()

if __name__ == "__main__":
    main(VENTANA, ANCHO_VENTANA) 