import algorithms as al
import pygame as pg
import sys
import bot

import os

pg.init()

# musik settings
pg.mixer.init()
pg.mixer.music.load('music/audio.mp3')
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.3)

size_screen = (1300, 700)
screen = pg.display.set_mode(size_screen)

background = pg.image.load("images/background.png")
boom  = pg.image.load("images/Boom.png")
screen.blit(background, (0,0))

BLACK = (0,0,0)

ships = {
    1: 4,
    2: 3,
    3: 2,
    4: 1
}

it = 1
count = 1


image = None
lockdrawn = False
lockdrawn_2 = False
rotate_status = 0




n1 = pg.font.Font(None, 60)


#буквы в начальном окне  
text1  = n1.render('А', True,(0, 0, 0))
text2  = n1.render("B", False,(0, 0, 0))
text3  = n1.render('C', True,(0, 0, 0))
text4  = n1.render("D", False,(0, 0, 0))
text5  = n1.render('E', True,(0, 0, 0))
text6  = n1.render("F", False,(0, 0, 0))
text7  = n1.render('J', True,(0, 0, 0))
text8  = n1.render("H", False,(0, 0, 0))
text9  = n1.render('I', True,(0, 0, 0))
text10 = n1.render("L", False,(0, 0, 0))

# цифры в начальном окне
number1  = n1.render('1', True,(0, 0, 0))
number2  = n1.render("2", False,(0, 0, 0))
number3  = n1.render('3', True,(0, 0, 0))
number4  = n1.render("4", False,(0, 0, 0))
number5  = n1.render('5', True,(0, 0, 0))
number6  = n1.render("6", False,(0, 0, 0))
number7  = n1.render('7', True,(0, 0, 0))
number8  = n1.render("8", False,(0, 0, 0))
number9  = n1.render('9', True,(0, 0, 0))
number10 = n1.render("10", False,(0, 0, 0))

# Вертикаль
for y in range(11):
    pg.draw.line(screen, BLACK, (y*50 + 120, 80), (y*50 + 120, 635), 5)
#  Горизонталь
for x in range(11):
    pg.draw.line(screen, BLACK, (80, x*50 + 135), (620, x*50 + 135), 5)

#Задаємо координати тексту
screen.blit(text1,   (130, 90))
screen.blit(text2,   (180, 90))
screen.blit(text3,   (230, 90))
screen.blit(text4,   (280, 90))
screen.blit(text5,   (330, 90))
screen.blit(text6,   (380, 90))
screen.blit(text7,   (430, 90))
screen.blit(text8,   (480, 90))
screen.blit(text9,   (540, 90))
screen.blit(text10,  (580, 90))
#Задаємо координати цифор
screen.blit(number1,  (90, 140))
screen.blit(number2,  (90, 190))
screen.blit(number3,  (90, 240))
screen.blit(number4,  (90, 290))
screen.blit(number5,  (90, 340))
screen.blit(number6,  (90, 390))
screen.blit(number7,  (90, 440))
screen.blit(number8,  (90, 490))
screen.blit(number9,  (90, 540))
screen.blit(number10, (70, 590))

pg.display.update()
    
pg.display.set_caption("Морський бій")



text_print_image = pg.image.load("images/text.png")
screen.blit(text_print_image, (700, 200))

def new_screen():
    background2 = pg.image.load("images/123.png")
    screen.blit(background2, (0, 0))


class Cell:
    def __init__(self, position, size, pos_in_array):
        self.center_pos = (position[0] + size[0] // 2, position[1] + size[1]  // 2)
        self.POS = position
        self.SIZE = size
        self.POINTS = al.zone(position, size)
        self.pos_in_array = pos_in_array

        self.status_cell = 0

        self.rotate_Texure = 0
        self.Texture = None
        self.last_cell = None

    def render(self):
        if self.Texture is not None:
            image = pg.image.load(self.Texture)
            image = pg.transform.rotate(image, self.rotate_Texure)
            screen.blit(image, self.POS)
        
        # if self.status_cell == 3:
        #     pg.draw.circle(screen, (255,0,0), self.center_pos, 6)

    def set_texture(self, path):
        if os.path.isfile(path):
            self.Texture = path

    def rotate_texture(self, angle):
        self.rotate_Texure = angle
    
    def check(self, mouse):
        return al.is_point_in_square(mouse, self.POINTS)

class Cell_bot(Cell):
    def __init__(self, position, size, pos_in_array):
        super().__init__(position, size, pos_in_array)
    def render(self):
        pass

#Генерация поля
table_for_ships= [
    [ Cell( (123 + 50* x , 137 + 50* y), (50, 50), (y,x) ) for x in range(10) ] for y in range(10)]

table_for_ships_bot = [
    [Cell_bot( (749 + 50* x , 137 + 50* y), (50, 50), (y,x) ) for x in range(10) ] for y in range(10)]


# Налаштування кнопки
button = pg.Rect(800, 600, 100, 50)
font = pg.font.Font(None, 70)
text = font.render("ПОЧАТИ", True, (0, 0, 0))
text_rect = text.get_rect(center=button.center)

# создоём бота
BOT = bot.Bot(table_for_ships, table_for_ships_bot, screen)
BOT.gen_ships()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                rotate_status += 90
                if rotate_status == 360:
                    rotate_status = 0

        
        if event.type == pg.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos) and not lockdrawn and it == 5:
                text_rect.move_ip(1000, 1000) 
                # перекидання на новий екран
                new_screen()
                lockdrawn = True
                
                for i in range(11):
                    pg.draw.line(screen, BLACK, (i*50 + 120, 80),   (i*50 + 120, 635), 5)
                    pg.draw.line(screen, BLACK, (80, i*50 + 135),   (620, i*50 + 135), 5)
                    pg.draw.line(screen, BLACK, (i*50 + 750, 80),   (i*50 + 750, 635), 5)
                    pg.draw.line(screen, BLACK, (1250, i*50 + 135), (700, i*50 + 135), 5)

                #координаты букв в 1 окне
                screen.blit(text1,   (130, 90))
                screen.blit(text2,   (180, 90))
                screen.blit(text3,   (230, 90))
                screen.blit(text4,   (280, 90))
                screen.blit(text5,   (330, 90))
                screen.blit(text6,   (380, 90))
                screen.blit(text7,   (430, 90))
                screen.blit(text8,   (480, 90))
                screen.blit(text9,   (540, 90))
                screen.blit(text10,  (580, 90))

                #координаты цифор в 1 окне
                screen.blit(number1,  (90, 140))
                screen.blit(number2,  (90, 190))
                screen.blit(number3,  (90, 240))
                screen.blit(number4,  (90, 290))
                screen.blit(number5,  (90, 340))
                screen.blit(number6,  (90, 390))
                screen.blit(number7,  (90, 440))
                screen.blit(number8,  (90, 490))
                screen.blit(number9,  (90, 540))
                screen.blit(number10, (70, 590))

                #координаты букв в 2 окне
                screen.blit(text1,    (760, 90))
                screen.blit(text2,    (810, 90))
                screen.blit(text3,    (860, 90))
                screen.blit(text4,    (910, 90))
                screen.blit(text5,    (960, 90))
                screen.blit(text6,    (1010, 90))
                screen.blit(text7,    (1060, 90))
                screen.blit(text8,    (1110, 90))
                screen.blit(text9,    (1170, 90))
                screen.blit(text10,   (1210, 90))
                
                #координаты цифор в 2 окне
                screen.blit(number1,  (710, 140))
                screen.blit(number2,  (710, 190))
                screen.blit(number3,  (710, 240))
                screen.blit(number4,  (710, 290))
                screen.blit(number5,  (710, 340))
                screen.blit(number6,  (710, 390))
                screen.blit(number7,  (710, 440))           
                screen.blit(number8,  (710, 490))
                screen.blit(number9,  (710, 540))
                screen.blit(number10, (700, 590))

                for y in table_for_ships:
                    for cell in y:
                        cell.render()
                continue

                

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            # Получаем координаты мыши
            mouse_x, mouse_y = pg.mouse.get_pos()
            
            if not lockdrawn:
                if it <= len(ships):

                    # Отображаем картинку на экране с учетом координат мыши
                    for dy, y in enumerate(table_for_ships):
                        for dx, cell in enumerate(y):
                            if cell.check((mouse_x, mouse_y)) and cell.status_cell == 0:
                                if not al.check_next_elements(table_for_ships, (dx, dy), rotate_status, it):
                                    continue

                                al.rotate_ship(table_for_ships, (dx, dy), rotate_status, al.set_ship(it))

                                if ships[it] > count:
                                    count += 1
                                else:
                                    it += 1
                                    count = 1
            elif not lockdrawn_2:
                for dy, y in enumerate(table_for_ships_bot):
                    for dx, cell in enumerate(y):
                        if cell.check((mouse_x, mouse_y)):
                            if cell.status_cell in [4, 5]:
                                break 

                            if cell.status_cell == 1:
                                screen.blit(boom, cell.POS)
                                cell.status_cell = 4
                                break
                            
                            pg.draw.circle(screen, (0,0,0), cell.center_pos, 6)
                            cell.status_cell = 5

                            BOT.next_point()
                

                # проверяем на победу  
                points_dead_ships = {
                    "player": 0,
                    "bot":    0
                }
                for y in range(10):
                    for x in range(10):
                        if table_for_ships_bot[y][x].status_cell == 4:
                            points_dead_ships["player"]+=1
                        if table_for_ships[y][x].status_cell == 4:
                            points_dead_ships["bot"]+=1

                for user in points_dead_ships:
                    if points_dead_ships[user] == 20:
                    
                        win_player = "player" if user == "player" else 'bot'
                        lockdrawn_2 = True
                        size_screen2 = (1300, 700)
                        screen2 = pg.display.set_mode(size_screen2)
                        if win_player == "player":
                            background2 = pg.image.load("images/fon.png")
                            screen.blit(background2, (0,0))
                            you_win = pg.image.load("images/You.png")
                            screen.blit(you_win, (500,500))
                    
                        if win_player == "bot":
                            background2 = pg.image.load("images/fon.png")
                            screen.blit(background2, (0,0))
                            bot_win = pg.image.load("images/Bot.png")
                            screen.blit(bot_win, (500,500))
    # Відображення кнопки та тексту на екрані 
    screen.blit(text, text_rect)
    pg.display.update()
  

