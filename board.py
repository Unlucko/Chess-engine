import pygame as pg
import constants as con
import pieces

class Cell:
    def __init__(self, display: pg.display, Xpos: int, Ypos: int, principality: bool):
        self.__display = display
        self.xpos = Xpos
        self.ypos = Ypos
        self.__width = con.WIDTH / con.ROWS
        self.__heigth = con.HEIGTH / con.COLUMNS
        self.occupied = False
        self.__principal = principality
        self.rect = None
        self.piece = None

    def drawCell(self) -> None:
        self.rect = pg.Rect(self.xpos, self.ypos, self.__width, self.__heigth) 
        pg.draw.rect(self.__display,
                     con.COLORS[(self.__principal+1)%2],
                     self.rect) 

class Board:
    def __init__(self, display: pg.display):
        self.__display = display
        self.__rows = con.ROWS
        self.__columns = con.COLUMNS
        self.__board = []
        self.buildBoard()
        self.setupPieces()
        self.dragged_piece = None

    def buildBoard(self):
        for row in range(self.__rows):
            vec = []
            for col in range(self.__columns):
                curXPos = col * (con.WIDTH / con.COLUMNS) 
                curYPos = row * (con.HEIGTH / con.ROWS)    
                curCell = Cell(self.__display,
                               curXPos,
                               curYPos,
                               principality=(row+col)%2)
                vec.append(curCell)
            self.__board.append(vec)

    def setupPieces(self):
        piece = pieces.Piece("pawn", True, self.__display, 
                           self.__board[1][1].xpos, 
                           self.__board[1][1].ypos)
        self.__board[1][1].occupied = True
        self.__board[1][1].piece = piece

    def render(self):

        for row in range(self.__rows):
            for col in range(self.__columns):
                self.__board[row][col].drawCell()
        

        for row in range(self.__rows):
            for col in range(self.__columns):
                if (self.__board[row][col].occupied and 
                    self.__board[row][col].piece and 
                    not self.__board[row][col].piece.dragged):
                    self.__board[row][col].piece.drawPiece()
        

        if self.dragged_piece:
            self.dragged_piece.drawPiece()

    def startDrag(self, positions: tuple):

        for row in self.__board:
            for cell in row:
                if cell.rect.collidepoint(positions) and cell.occupied and cell.piece:
                    self.dragged_piece = cell.piece
                    self.dragged_piece.startDrag(positions)
                    return cell
        return None

    def updateDrag(self, mouse_pos):

        if self.dragged_piece:
            self.dragged_piece.updateDrag(mouse_pos)

    def stopDrag(self, mouse_pos):
        if self.dragged_piece:
            self.dragged_piece.stopDrag()
            self.dragged_piece = None