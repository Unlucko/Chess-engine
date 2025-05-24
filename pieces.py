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
    
    def capture(self):
        pass

    def captured(self):
        pass

    def dragPiece(self, rel):
        self.rect.move_ip(*rel)
        self.__display.blit(self.image, rel)
        self.xpos, self.ypos = rel
        pg.display.update()
        pg.display.flip()

    def drawPiece(self):
        self.image = pg.image.load('images/white-pawn.png')
        self.image = pg.transform.scale(self.image, (con.WIDTH/con.COLUMNS,con.HEIGTH/con.ROWS))
        self.rect = self.image.get_rect(center=(50,50))
        self.__display.blit(self.image, (self.xpos, self.ypos))