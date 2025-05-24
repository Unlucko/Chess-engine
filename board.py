import pygame as pg
import constants as con
import pieces

class Cell:
    def __init__(self, display: pg.display, Xpos: int, Ypos: int, principality: bool):
        self.__display = display
        self.__xpos = Xpos
        self.__ypos = Ypos
        self.__width = con.WIDTH / con.ROWS
        self.__heigth = con.HEIGTH / con.COLUMNS
        self.occupied = False
        self.__principal = principality
        self.rect = None
        self.piece = None

    def occupy(self):
        pass

    def drawCell(self) -> None:
        self.rect = pg.Rect(self.__xpos, self.__ypos,self.__width,self.__heigth) 
        pg.draw.rect(self.__display,
                     con.COLORS[(self.__principal+1)%2],
                     self.rect) 

    def __repr__(self):
        return f"{self.__xpos}{self.__ypos}"

class Board:
    def __init__(self, display: pg.display):
        self.__display = display
        self.__rows = con.ROWS
        self.__columns = con.COLUMNS
        self.__board = []
        self.drawBoard()
        self.drawPieces()

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
        self.buildBoard()
        for row in range(self.__rows):
            for col in range(self.__columns):
                self.__board[row][col].drawCell()
                pg.display.update()
    
    def drawPieces(self):
        piece = pieces.Piece(0,0,self.__display, 0,0)
        self.__board[0][0].occupied = True
        self.__board[0][0].piece = piece        
        piece.drawPiece()
        pg.display.update()

    def mouseMovementHandler(self, cell, rel):
        print(rel)
        cell.piece.dragPiece(rel)
        self.drawBoard()

    def mouseClickHandler(self, positions: tuple) -> tuple:
        for row in self.__board:
            for col in row:
                if col.rect.collidepoint(positions) and col.occupied:
                    return col
                    

