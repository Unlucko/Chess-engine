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

        self.drag_pos = None
        self.cell_x = Xpos  
        self.cell_y = Ypos
        

        self.loadImage()
    
    def loadImage(self):

        self.image = pg.image.load('images/white-pawn.png')
        self.image = pg.transform.scale(self.image, 
                                      (con.WIDTH//con.COLUMNS, con.HEIGTH//con.ROWS))
        self.updateRect()
    
    def updateRect(self):

        if self.dragged and self.drag_pos:

            self.rect = self.image.get_rect(center=self.drag_pos)
        else:

            cell_center_x = self.cell_x + (con.WIDTH // con.COLUMNS) // 2
            cell_center_y = self.cell_y + (con.HEIGTH // con.ROWS) // 2
            self.rect = self.image.get_rect(center=(cell_center_x, cell_center_y))
    
    def startDrag(self, mouse_pos):

        self.dragged = True
        self.drag_pos = mouse_pos
        self.updateRect()
    
    def updateDrag(self, mouse_pos):

        if self.dragged:
            self.drag_pos = mouse_pos
            self.updateRect()
    
    def stopDrag(self, mouse_pos):

        self.dragged = False
        self.drag_pos = None
        self.updateRect()


    def drawPiece(self):

        self.updateRect()
        self.__display.blit(self.image, self.rect)