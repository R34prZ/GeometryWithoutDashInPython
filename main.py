from typing import Dict, final
import pygame
from pygame.locals import *
import sys
import random
import time
#from time import sleep

pygame.init()
pygame.display.set_caption('GeometryWithoutAnyDash')

clock = pygame.time.Clock()

WIN_SIZE = (600, 400)
WIN = pygame.display.set_mode(WIN_SIZE, 0, 32)
DISPLAY = pygame.Surface((300, 200))

# images
player_image = pygame.image.load('./img/player.png')
floor_img = pygame.image.load('./img/floor.png')
spike_img = pygame.image.load('./img/spike.png').convert()
spike_img.set_colorkey((255, 255, 255))
tile_size = floor_img.get_width()


# game map
game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','2','0','2','0','2','0','0','0','0','0','0'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]
# Movement
## function to check collision
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

## funtion to move and not fall down the world
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    ### horizontal movement
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    ### vertical movement
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False


def main():
    player_y_momentum = 0
    air_timer =0
    player_rect = pygame.Rect(0, 90, player_image.get_width(), player_image.get_height())
    
    start_time = time.time()
# main loop
    while True:
        # delta time
        final_time = time.time()
        delta_time = (final_time - start_time)
        start_time = final_time
        print(f'delta time is: {delta_time}')

        # draw
        DISPLAY.fill((40, 100, 190))

        tile_rects = []
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    DISPLAY.blit(floor_img, (x * tile_size, y * tile_size))
                if tile == '2':
                    # just to see the rect and test collisions
                    spike_rect = pygame.Rect((x * tile_size, y * tile_size), (tile_size, tile_size))
                    pygame.draw.rect(DISPLAY, (0, 0, 255), spike_rect, 5)
                    DISPLAY.blit(spike_img, (x * tile_size, y * tile_size))
                    if player_rect.colliderect(spike_rect):
                        menu()
                        print('Opora bati no espinho ai ai ai')
                if tile != '0':
                    tile_rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
                x += 1
            y += 1

        # movement logic
        moving_right = True
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == KEYDOWN:
                #if ev.key == K_a:
                    #moving_left = True
                #if ev.key == K_d:
                    #moving_right = True
                if ev.key == K_w:
                    if air_timer < 6:
                        player_y_momentum = -4   
            # if ev.type == KEYUP:
            #     if ev.key == K_d:
            #         moving_right = False
            #     if ev.key == K_a:
                    # moving_left = False

        player_movement = [0, 0]
        # player velocity
        if moving_right:
            player_movement[0] += (150 * delta_time)
        if moving_left:
            player_movement[0] -= (150 * delta_time)
        player_movement[1] += player_y_momentum
        # this thing puts the player down acting like gravity just to remember my self
        player_y_momentum += 0.3
        if player_y_momentum > 3:
            player_y_momentum = 3

        player_rect, collisions = move(player_rect, player_movement, tile_rects)
        # just to see the rect and test collisions
        pygame.draw.rect(DISPLAY, (0, 255, 0), (player_rect), 10)
        if collisions['bottom']:
            player_y_momentum = 0
            air_timer = 0
        else:
            air_timer += 1
        if collisions['top']:
            player_y_momentum = 1
        
        # draw player (it's here because of the variables)

        DISPLAY.blit(player_image, (player_rect.x, player_rect.y))

        
        # surface updates?
        surface = pygame.transform.scale(DISPLAY, WIN_SIZE)
        WIN.blit(surface, (0,0))
        pygame.display.update()
        FPS = 60
        clock.tick(FPS)

def menu():
    text = 'Press to Play!'
    font = pygame.font.SysFont('comicsans', 24)
    text_surface = font.render(text, True, (255,255,255))

    def colorpicker():
        color_picker_R = random.randint(0,255)
        color_picker_G = random.randint(0,255)
        color_picker_B = random.randint(0,255)
        pygame.time.delay(500)
        WIN.fill((color_picker_R, color_picker_G, color_picker_B))
    while True:

        colorpicker()
        WIN.blit(text_surface, (WIN_SIZE[0] / 2 - text_surface.get_width() / 2, WIN_SIZE[1] / 2))
        
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == MOUSEBUTTONDOWN:
                main()
        pygame.display.update()   

if __name__ == '__main__':
    menu()