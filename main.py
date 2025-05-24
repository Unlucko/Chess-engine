import pygame as pg
import constants as con
import board

pg.init()
pg.display.init()
display = pg.display.set_mode(size=(con.WIDTH,con.HEIGTH))
screen = board.Board(display)


moving = False
clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()

        elif event.type == pg.MOUSEBUTTONUP:
            moving = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            cell = screen.mouseClickHandler(pg.mouse.get_pos())
            moving = True

        elif event.type == pg.MOUSEMOTION and moving:
            if cell != None:
                screen.mouseMovementHandler(cell, event.pos)
                pg.display.update()

    pg.display.flip()
    clock.tick(60)
    

                  