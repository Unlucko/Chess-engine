import pygame as pg
import constants as con
import board

pg.init()
pg.display.init()
display = pg.display.set_mode(size=(con.WIDTH,con.HEIGTH))


while True:
    screen = board.Board(display)
    screen.drawBoard()
    pg.display.update()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    
