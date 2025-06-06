import pygame as pg
import constants as con
import board

pg.init()
display = pg.display.set_mode(size=(con.WIDTH, con.HEIGTH))
pg.display.set_caption("Ajedrez Suave")
screen = board.Board(display)

dragging = False
clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  
                cell = screen.startDrag(event.pos)
                if cell:
                    dragging = True

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and dragging:  
                screen.stopDrag(event.pos, cell.principal)
                dragging = False

        elif event.type == pg.MOUSEMOTION:
            if dragging:
                screen.updateDrag(event.pos)


    screen.render()
    

    pg.display.flip()
    clock.tick(60)