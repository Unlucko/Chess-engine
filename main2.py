
import pygame
import sys

# Inicializar pygame
pygame.init()

# Constantes
ANCHO, ALTO = 640, 640
FILAS, COLUMNAS = 8, 8
TAMAÑO_CASILLA = ANCHO // COLUMNAS

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MARRON_CLARO = (240, 217, 181)
MARRON_OSCURO = (181, 136, 99)
AZUL = (0, 100, 255)
VERDE = (0, 255, 0)

class Pieza:
    def __init__(self, fila, columna, color):
        self.fila = fila
        self.columna = columna
        self.color = color
        self.seleccionada = False
        self.siendo_arrastrada = False
        self.pos_arrastre = None
        
    def dibujar(self, pantalla):
        if self.siendo_arrastrada and self.pos_arrastre:
            # Si está siendo arrastrada, dibujar en la posición del mouse
            x, y = self.pos_arrastre
        else:
            # Posición normal en el tablero
            x = self.columna * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2
            y = self.fila * TAMAÑO_CASILLA + TAMAÑO_CASILLA // 2
        
        # Dibujar círculo para representar la pieza
        color_pieza = NEGRO if self.color == 'negro' else BLANCO
        pygame.draw.circle(pantalla, color_pieza, (x, y), TAMAÑO_CASILLA // 3)
        pygame.draw.circle(pantalla, NEGRO, (x, y), TAMAÑO_CASILLA // 3, 3)
        
        # Resaltar si está seleccionada
        if self.seleccionada:
            pygame.draw.circle(pantalla, VERDE, (x, y), TAMAÑO_CASILLA // 3, 5)

class Tablero:
    def __init__(self):
        self.tablero = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.pieza_seleccionada = None
        self.pieza_arrastrada = None
        self.turno = 'blanco'
        self.crear_piezas()
    
    def crear_piezas(self):
        # Crear piezas negras (arriba)
        for col in range(COLUMNAS):
            if col % 2 == 1:  # Solo en casillas impares de la fila 0
                self.tablero[0][col] = Pieza(0, col, 'negro')
            if col % 2 == 0:  # Solo en casillas pares de la fila 2
                self.tablero[2][col] = Pieza(2, col, 'negro')
        
        # Fila intermedia de piezas negras
        for col in range(COLUMNAS):
            if col % 2 == 1:
                self.tablero[1][col] = Pieza(1, col, 'negro')
        
        # Crear piezas blancas (abajo)
        for col in range(COLUMNAS):
            if col % 2 == 0:  # Solo en casillas pares de la fila 5
                self.tablero[5][col] = Pieza(5, col, 'blanco')
            if col % 2 == 1:  # Solo en casillas impares de la fila 7
                self.tablero[7][col] = Pieza(7, col, 'blanco')
        
        # Fila intermedia de piezas blancas
        for col in range(COLUMNAS):
            if col % 2 == 0:
                self.tablero[6][col] = Pieza(6, col, 'blanco')
    
    def dibujar_tablero(self, pantalla):
        # IMPORTANTE: Limpiar la pantalla primero
        pantalla.fill(BLANCO)
        
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                # Alternar colores del tablero
                color = MARRON_CLARO if (fila + col) % 2 == 0 else MARRON_OSCURO
                rect = pygame.Rect(col * TAMAÑO_CASILLA, fila * TAMAÑO_CASILLA, 
                                 TAMAÑO_CASILLA, TAMAÑO_CASILLA)
                pygame.draw.rect(pantalla, color, rect)
                
                # Dibujar pieza si existe y no está siendo arrastrada
                pieza = self.tablero[fila][col]
                if pieza and not pieza.siendo_arrastrada:
                    pieza.dibujar(pantalla)
        
        # Dibujar pieza siendo arrastrada al final (por encima de todo)
        if self.pieza_arrastrada:
            self.pieza_arrastrada.dibujar(pantalla)
        
        # Resaltar casilla seleccionada
        if self.pieza_seleccionada and not self.pieza_seleccionada.siendo_arrastrada:
            fila, col = self.pieza_seleccionada.fila, self.pieza_seleccionada.columna
            rect = pygame.Rect(col * TAMAÑO_CASILLA, fila * TAMAÑO_CASILLA, 
                             TAMAÑO_CASILLA, TAMAÑO_CASILLA)
            pygame.draw.rect(pantalla, AZUL, rect, 5)
    
    def obtener_casilla_desde_mouse(self, pos):
        x, y = pos
        fila = y // TAMAÑO_CASILLA
        col = x // TAMAÑO_CASILLA
        if 0 <= fila < FILAS and 0 <= col < COLUMNAS:
            return fila, col
        return None
    
    def seleccionar_pieza(self, fila, col):
        pieza = self.tablero[fila][col]
        
        if self.pieza_seleccionada:
            # Si ya hay una pieza seleccionada
            if pieza and pieza.color == self.turno and pieza != self.pieza_seleccionada:
                # Seleccionar nueva pieza del mismo color
                self.pieza_seleccionada.seleccionada = False
                self.pieza_seleccionada = pieza
                pieza.seleccionada = True
            elif pieza == self.pieza_seleccionada:
                # Deseleccionar la misma pieza
                pieza.seleccionada = False
                self.pieza_seleccionada = None
            else:
                # Intentar mover a casilla vacía o capturar pieza enemiga
                self.mover_pieza(fila, col)
        else:
            # No hay pieza seleccionada
            if pieza and pieza.color == self.turno:
                self.pieza_seleccionada = pieza
                pieza.seleccionada = True
    
    def mover_pieza(self, nueva_fila, nueva_col):
        if self.pieza_seleccionada and self.es_movimiento_valido(nueva_fila, nueva_col):
            # Guardar posición anterior
            fila_anterior = self.pieza_seleccionada.fila
            col_anterior = self.pieza_seleccionada.columna
            
            # Mover la pieza
            self.tablero[nueva_fila][nueva_col] = self.pieza_seleccionada
            self.tablero[fila_anterior][col_anterior] = None
            
            # Actualizar posición de la pieza
            self.pieza_seleccionada.fila = nueva_fila
            self.pieza_seleccionada.columna = nueva_col
            self.pieza_seleccionada.seleccionada = False
            
            # Cambiar turno
            self.turno = 'negro' if self.turno == 'blanco' else 'blanco'
            self.pieza_seleccionada = None
    
    def iniciar_arrastre(self, fila, col):
        """Inicia el arrastre de una pieza"""
        pieza = self.tablero[fila][col]
        if pieza and pieza.color == self.turno:
            self.pieza_arrastrada = pieza
            pieza.siendo_arrastrada = True
            pieza.seleccionada = True
            return True
        return False
    
    def actualizar_arrastre(self, pos_mouse):
        """Actualiza la posición de la pieza siendo arrastrada"""
        if self.pieza_arrastrada:
            self.pieza_arrastrada.pos_arrastre = pos_mouse
    
    def finalizar_arrastre(self, pos_mouse):
        """Finaliza el arrastre y mueve la pieza si es válido"""
        if not self.pieza_arrastrada:
            return
        
        casilla_destino = self.obtener_casilla_desde_mouse(pos_mouse)
        if casilla_destino:
            nueva_fila, nueva_col = casilla_destino
            if self.es_movimiento_valido_arrastre(nueva_fila, nueva_col):
                self.mover_pieza_arrastre(nueva_fila, nueva_col)
            else:
                # Movimiento inválido, regresar pieza a su posición
                self.cancelar_arrastre()
        else:
            # Fuera del tablero, cancelar arrastre
            self.cancelar_arrastre()
    
    def cancelar_arrastre(self):
        """Cancela el arrastre y regresa la pieza a su posición original"""
        if self.pieza_arrastrada:
            self.pieza_arrastrada.siendo_arrastrada = False
            self.pieza_arrastrada.seleccionada = False
            self.pieza_arrastrada.pos_arrastre = None
            self.pieza_arrastrada = None
    
    def mover_pieza_arrastre(self, nueva_fila, nueva_col):
        """Mueve la pieza arrastrada a la nueva posición"""
        if self.pieza_arrastrada:
            # Guardar posición anterior
            fila_anterior = self.pieza_arrastrada.fila
            col_anterior = self.pieza_arrastrada.columna
            
            # Mover la pieza
            self.tablero[nueva_fila][nueva_col] = self.pieza_arrastrada
            self.tablero[fila_anterior][col_anterior] = None
            
            # Actualizar posición de la pieza
            self.pieza_arrastrada.fila = nueva_fila
            self.pieza_arrastrada.columna = nueva_col
            self.pieza_arrastrada.siendo_arrastrada = False
            self.pieza_arrastrada.seleccionada = False
            self.pieza_arrastrada.pos_arrastre = None
            
            # Cambiar turno
            self.turno = 'negro' if self.turno == 'blanco' else 'blanco'
            self.pieza_arrastrada = None
    
    def es_movimiento_valido_arrastre(self, nueva_fila, nueva_col):
        """Verifica si el movimiento de arrastre es válido"""
        if not self.pieza_arrastrada:
            return False
            
        # Verificar límites
        if not (0 <= nueva_fila < FILAS and 0 <= nueva_col < COLUMNAS):
            return False
        
        # No puede moverse a la misma posición
        if nueva_fila == self.pieza_arrastrada.fila and nueva_col == self.pieza_arrastrada.columna:
            return False
        
        pieza_destino = self.tablero[nueva_fila][nueva_col]
        
        # No puede moverse a casilla ocupada por pieza del mismo color
        if pieza_destino and pieza_destino.color == self.pieza_arrastrada.color:
            return False
        
        # Movimiento básico: una casilla en diagonal (como damas)
        diff_fila = abs(nueva_fila - self.pieza_arrastrada.fila)
        diff_col = abs(nueva_col - self.pieza_arrastrada.columna)
        
        return diff_fila == 1 and diff_col == 1

def main():
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ajedrez - Pygame (Arrastre)")
    reloj = pygame.time.Clock()
    
    tablero = Tablero()
    arrastrando = False
    
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    pos = pygame.mouse.get_pos()
                    casilla = tablero.obtener_casilla_desde_mouse(pos)
                    if casilla:
                        fila, col = casilla
                        if tablero.iniciar_arrastre(fila, col):
                            arrastrando = True
            
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1 and arrastrando:  # Soltar clic izquierdo
                    pos = pygame.mouse.get_pos()
                    tablero.finalizar_arrastre(pos)
                    arrastrando = False
            
            elif evento.type == pygame.MOUSEMOTION:
                if arrastrando:
                    pos = pygame.mouse.get_pos()
                    tablero.actualizar_arrastre(pos)
        
        # CLAVE: Dibujar todo en cada frame
        tablero.dibujar_tablero(pantalla)
        
        # Mostrar de quién es el turno
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"Turno: {tablero.turno.capitalize()}", True, NEGRO)
        pantalla.blit(texto, (10, 10))
        
        # Mostrar instrucciones
        fuente_pequeña = pygame.font.Font(None, 24)
        instruccion = fuente_pequeña.render("Arrastra las piezas con el mouse", True, NEGRO)
        pantalla.blit(instruccion, (10, ALTO - 30))
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()