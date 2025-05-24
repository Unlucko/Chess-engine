import pygame as pg
import constants as con

class Cell:
    def __init__(self, display: pg.display, Xpos: int, Ypos: int, principality: bool):
        self.display = display
        self.__xpos = Xpos
        self.__ypos = Ypos
        self.__width = con.WIDTH / con.ROWS
        self.__heigth = con.HEIGTH / con.COLUMNS
        self.__occupied = False
        self.__principal = principality

    def occupy():
        pass

    def drawCell(self) -> None:
        rectan = pg.Rect(self.__xpos, self.__ypos,self.__width,self.__heigth) 
        pg.draw.rect(self.display,
                     con.COLORS[(self.__principal+1)%2],
                     rectan)   

class Board:
    def __init__(self, display: pg.display):
        self.__display = display
        self.__height = con.HEIGTH
        self.__width = con.WIDTH
        self.__rows = con.ROWS
        self.__columns = con.COLUMNS
        self.__board = []
        self.buildBoard()

    def buildBoard(self):
        for row in range(self.__rows):
            vec = []
            for col in range(self.__columns):
                curXPos = row * (con.WIDTH / con.ROWS) 
                curYPos = col * (con.HEIGTH / con.COLUMNS)
                curCell = Cell(self.__display,
                               curXPos,
                               curYPos,
                               principality=(row+col)%2)
                vec.append(curCell)
            self.__board.append(vec)

    def updateBoard(self):
        pass

    def drawBoard(self):
        for row in range(self.__rows):
            for col in range(self.__columns):
                self.__board[row][col].drawCell()
                pg.display.update()


