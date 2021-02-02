# this file is just to test and better understand collisions, probably will be deleted later

import pygame
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
WIN_SIZE = (640, 480)
WIN = pygame.display.set_mode(WIN_SIZE)
SURF = pygame.Surface((320, 240))


def main():
    
    spike_img = pygame.image.load('./img/spike.png').convert()
    spike_img.set_colorkey((255, 255, 255))
    player_image = pygame.image.load('./img/player.png')
    x = 100

    while True:
        spike_Rect = pygame.Rect(200, 100, 16, 16)
        player_Rect = pygame.Rect(x, 100, 16, 16)
        SURF.fill((20, 120, 150))
        SURF.blit(player_image, player_Rect)
        SURF.blit(spike_img, spike_Rect)

        if player_Rect.colliderect(spike_Rect):
            menu()

        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
        key = pygame.key.get_pressed()
        if key[K_d]:
            x += 2
        if key[K_a]:
            x -= 2
        
        screen = pygame.transform.scale(SURF, WIN_SIZE)
        WIN.blit(screen, (0, 0))

        clock.tick(30)
        pygame.display.update()

def menu():
    font = pygame.font.SysFont('Comic Sans', 32)
    text = 'Press to play'
    font_surf = font.render(text, True, (255, 255, 255), (0, 255, 0))

    while True:
        WIN.fill((0, 0, 0))
        WIN.blit(font_surf, (WIN_SIZE[0] / 2 - font_surf.get_width() / 2, WIN_SIZE[1] / 2))
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
            if ev.type == MOUSEBUTTONDOWN:
                main()
        pygame.display.update()
menu()