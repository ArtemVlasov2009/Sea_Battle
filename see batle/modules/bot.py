import algorithms as al
import pygame as pg
import random

boom = pg.image.load("images/Boom.png")

class Bot:
    def __init__(self, table_player, table_bot, screen):
        self.sc = screen
        self.table_player = table_player
        self.table = table_bot

    def gen_ships(self):
        for it in range(1, 5):
            for _ in range(5-it):
                while True:     
                    x = random.randint(0,9)
                    y = random.randint(0,9)
                    angle = random.choice([0,90,180,360])
                    cell = self.table[y][x]
                    if cell.status_cell not in [3, 4]:
                        if not al.check_next_elements(self.table, (x,y), angle, it):
                            continue

                        al.rotate_ship(self.table, (x, y), angle, al.set_ship(it))
                        break

    @staticmethod
    def random_point(matrix):
        all_pos = [] 
        for y in matrix:
            for x in y:
                if x.status_cell not in [4, 5]:
                    all_pos.append(x.pos_in_array)

        
        if len(all_pos) == 0:
            return None
        
        y, x = random.choice(all_pos)
        return matrix[y][x]


    def next_point(self):
        cell = self.random_point(self.table_player)

        while True:
            if cell is None:
                break

            if cell.status_cell == 1:
                self.sc.blit(boom, cell.POS)
                cell.status_cell = 4
                
                cell = self.random_point(self.table_player)

            else:
                pg.draw.circle(self.sc, (0,0,0), cell.center_pos, 7)
                cell.status_cell = 5
                break

