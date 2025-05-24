import pygame as pg
import constants as con

class Piece:
    def __init__(self, kind: str, color: bool, display: pg.display, Xpos, Ypos, image=None):
        self.xpos = Xpos
        self.ypos = Ypos
        self.__kind = kind
        self.__color = color
        self.__display = display
        self.image = None
        self.rect = None
        self.dragged = False
        # NUEVO: Posición de arrastre
        self.drag_pos = None
        self.cell_x = Xpos  # Posición original en el tablero
        self.cell_y = Ypos
        
        # Cargar imagen al crear la pieza
        self.loadImage()
    
    def loadImage(self):
        """Carga la imagen de la pieza una sola vez"""
        self.image = pg.image.load('images/white-pawn.png')
        self.image = pg.transform.scale(self.image, 
                                      (con.WIDTH//con.COLUMNS, con.HEIGTH//con.ROWS))
        self.updateRect()
    
    def updateRect(self):
        """Actualiza el rect basado en la posición actual"""
        if self.dragged and self.drag_pos:
            # Si está siendo arrastrada, centrar en la posición del mouse
            self.rect = self.image.get_rect(center=self.drag_pos)
        else:
            # Posición normal en la celda
            cell_center_x = self.cell_x + (con.WIDTH // con.COLUMNS) // 2
            cell_center_y = self.cell_y + (con.HEIGTH // con.ROWS) // 2
            self.rect = self.image.get_rect(center=(cell_center_x, cell_center_y))
    
    def startDrag(self, mouse_pos):
        """Inicia el arrastre"""
        self.dragged = True
        self.drag_pos = mouse_pos
        self.updateRect()
    
    def updateDrag(self, mouse_pos):
        """Actualiza la posición durante el arrastre"""
        if self.dragged:
            self.drag_pos = mouse_pos
            self.updateRect()
    
    def stopDrag(self):
        """Detiene el arrastre"""
        self.dragged = False
        self.drag_pos = None
        self.updateRect()
    
    def drawPiece(self):
        """Dibuja la pieza en su posición actual"""
        self.updateRect()
        self.__display.blit(self.image, self.rect)