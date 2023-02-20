import pygame

CAPTION = 'Zombies'

FPS = 60
PX = 5
WIN_X, WIN_Y = 1280, 720
CENTER_X = WIN_X / 2
FONT_PATH = 'Font/Pixel Millennium.ttf'

BTN_COLOR = (255, 255, 255)
BTN_HOVER_COLOR = (200, 200, 200)
BTN_BORDER_RADIUS = 5

sc = pygame.display.set_mode([WIN_X, WIN_Y])
clock = pygame.time.Clock()

pygame.font.init()
MENU_BTN_FONT = pygame.font.Font(FONT_PATH, 60)
UPGRADE_FONT = pygame.font.Font(FONT_PATH, 30)
MENU_FONT = pygame.font.Font(FONT_PATH, 100)

background = pygame.transform.scale(pygame.image.load('assets/background.png').convert(), (WIN_X, WIN_Y))
heart = pygame.image.load('assets/heart.png').convert_alpha()
no_heart = pygame.image.load('assets/no_heart.png').convert_alpha()
gun_img = pygame.transform.scale(pygame.image.load('assets/shotgun.png').convert_alpha(), (12 * PX, 15 * PX))
player_walk_sprite_sheet = pygame.image.load('assets/walk.png').convert_alpha()
player_walk_red_sprite_sheet = pygame.image.load('assets/walk_red.png').convert_alpha()
player_walk_back_sprite_sheet = pygame.image.load('assets/walk_back.png').convert_alpha()
zombie_walk_sprite_sheet = pygame.image.load('assets/zombie_walk.png').convert_alpha()
zombie_walk_red_sprite_sheet = pygame.image.load('assets/zombie_walk_red.png').convert_alpha()
player_walk, player_walk_back, player_walk_red, zombie_walk, zombie_walk_red = [], [], [], [], []
for i in range(6):
    frame = player_walk_sprite_sheet.subsurface((i * 12, 0, 12, 10))
    player_walk.append(pygame.transform.scale(frame, (frame.get_width() * PX, frame.get_height() * PX)))
    frame_r = player_walk_red_sprite_sheet.subsurface((i * 12, 0, 12, 10))
    player_walk_red.append(pygame.transform.scale(frame_r, (frame_r.get_width() * PX, frame_r.get_height() * PX)))
    frame_b = player_walk_back_sprite_sheet.subsurface((i * 12, 0, 12, 10))
    player_walk_back.append(pygame.transform.scale(frame_b, (frame_b.get_width() * PX, frame_b.get_height() * PX)))
    frame_z = zombie_walk_sprite_sheet.subsurface((i * 12, 0, 12, 11))
    zombie_walk.append(pygame.transform.scale(frame_z, (frame_z.get_width() * PX, frame_z.get_height() * PX)))
    frame_zr = zombie_walk_red_sprite_sheet.subsurface((i * 12, 0, 12, 11))
    zombie_walk_red.append(pygame.transform.scale(frame_zr, (frame_zr.get_width() * PX, frame_zr.get_height() * PX)))

WAVE_LENGTH = 30  # s

bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()


def save_highscore(score):
    f = open("highscore.txt", "w")  # opens a file
    f.write(str(score))  # rewrites the file highscore to new one


def get_highscore():
    try:
        f = open("highscore.txt", "r")  # open file
        return int(f.read())  # return the highscore
    except FileNotFoundError:  # if no file exists, highscore is 0
        return 0
