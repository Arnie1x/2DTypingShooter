import pygame
import math

width = 850
height = 700

def draw_player(text_list, selected_word, canvas):
    playerImage = pygame.image.load('assets/jet.png')
    player_X = width/2 - (playerImage.get_width() / 2)
    player_Y = height - playerImage.get_height()
    target_X = 900
    target_Y = -1100
    
    for obj in text_list:
        if obj.text == selected_word:
            target_X = obj.x
            target_Y = obj.y
            
    angle = math.degrees(360-(math.atan2(player_Y - target_Y, player_X - target_X)))
    rotimage = pygame.transform.rotate(playerImage,angle)
    canvas.blit(rotimage, (player_X, player_Y))