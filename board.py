import pygame as pg
import constants as con

class Cell:
    def __init__(self, display: pg.display, Xpos: int, Ypos: int):
        self.display = display
        self.__xpos = Xpos
        self.__ypos = Ypos
        self.__width = con.WIDTH / con.ROWS
        self.__heigth = con.HEIGTH / con.COLUMNS
        self.__occupied = False
        self.__principal = False

    def occupy():
        pass

    def drawCell(self) -> None:
        rectan = pg.Rect(self.__xpos, self.__ypos,self.__width,self.__heigth) 
        pg.draw.rect(self.display,
                     con.COLORS[(self.__principal+1)%2],
                     rectan)   

class Board:
    def __init__(self):
        self.height = con.HEIGTH
        self.width = con.WIDTH
        self.rows = con.ROWS
        self.columns = con.COLUMNS
        self.board = []

    def buildBoard(self):
        pass


    def drawBoard(self):
        pass


