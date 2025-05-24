import pygame as pg
import constants as con
import board

pg.init()
pg.display.init()
display = pg.display.set_mode(size=(640,480))


while True:
    cell = board.Cell(display,0,0)
    cell.drawCell()
    pg.display.update()
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

    
