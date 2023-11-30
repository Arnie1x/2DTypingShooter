import pygame 
import modules.word_list_generator as word_generator
import random
import math
from pygame import mixer
import json
import modules.models as models
import modules.functions as functions
import modules.player as player
import modules.input as input

pygame.init() 
# clock = pygame.time.Clock()
# clock.tick(60)

# CREATING CANVAS 
width = 850
height = 700
canvas = pygame.display.set_mode((width, height))

# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 

# Used to maintain the Game Loop
exit = False
start_menu = True
game_over = False

# Initialize the Wave System for Words
wave = 0
last_wave = 0
score = 0
word_list = []
# word_list = word_generator.generate_words(3 + wave)
# print("The words are: " + word_list.__str__())

selected_word = None
typed_word = ''
selected_word_index = 0

# Constants
white = (255, 255, 255)
black = (0, 0, 0)
font_24 = pygame.font.Font('assets/fonts/Poppins-Regular.ttf', 24)
font_36 = pygame.font.Font('assets/fonts/Poppins-Regular.ttf', 36)

text_list = []

# Background Sound
mixer.music.load('assets/audio/background.mp3')
mixer.music.play(-1)


def shoot_bullet():
    global lerp
    def lerp(A, B, C):
        return (C * A) + ((1-C) * B)
        
    
    bullet = pygame.image.load('assets/bullet-small.png')
    bullet_X = width/2 - (bullet.get_width() / 2)
    bullet_Y = height - bullet.get_height()
    target_X = 0
    target_Y = 0

    for obj in text_list:
        if obj.text == selected_word:
            target_X = obj.x
            target_Y = obj.y
            
    # angle = math.degrees(360-(math.atan2(bullet_X - target_Y, bullet_Y - target_X)))
    lerp_value = 0
    while lerp_value < 1:
        pygame.time.delay(20)
        lerp_value += 0.1
    pos_X = lerp(target_X, bullet_X, lerp_value)
    pos_Y = lerp(target_Y, bullet_Y, lerp_value)
    canvas.blit(bullet, (pos_X, pos_Y))

# Main Game Loop
while not exit:
    if start_menu:
        menu_selection = functions.show_menu(canvas)
        if menu_selection == "start":
            start_menu = False
        if menu_selection == "quit":
            start_menu = False
            break
    
    if game_over:
        game_over_menu = functions.draw_game_over(score, last_wave, canvas)
        if game_over_menu == "start":
            game_over = False
        if game_over_menu == "quit":
            game_over = False
            break
    
    bg = pygame.image.load('assets/game-background.jpg')
    bg = pygame.transform.scale(bg, (width, height))
    
    canvas.blit(bg, (0, 0))

    
    # Update the word list if empty
    if (len(word_list) == 0):
        wave += 1
        word_list = word_generator.generate_words(3 + wave)
        print("The words are: " + word_list.__str__())
        
        for word in word_list:
            text = font_24.render(word, True, white)
            text_rect = text.get_rect()
            text_rect.center = (width, height)
            text_list.append(models.Text(word, text, text_rect))
        
        index = 0
        for obj in text_list:
            index += 1
            obj.x = random.randint(round(width/len(text_list) * (index - 1)), round((width - 100)/len(text_list) * index))
            obj.y = random.randint(-100, 0)
            canvas.blit(obj.text_object, (obj.x, obj.y))
    
    # Read Keyboard input for Key Presses
    keys = pygame.key.get_pressed()
    for word in word_list:
        if selected_word is None and keys[pygame.key.key_code(word[selected_word_index])]:
            selected_word = word
            typed_word += word[selected_word_index]
            selected_word_index += 1
            print("Selected Word: " + selected_word)
            print("Typed Word: " + typed_word)
            score += 1
            selection_sound = mixer.Sound('assets/audio/click.ogg')
            selection_sound.play()
            break
        
    if selected_word is not None:
        # bullet = shoot_bullet()
        if keys[pygame.key.key_code(selected_word[selected_word_index])] and len(selected_word) != selected_word_index:
            typed_word += selected_word[selected_word_index]
            selected_word_index += 1
            score += 1
            print("Typed Word: " + typed_word)
            selection_sound = mixer.Sound('assets/audio/click.ogg')
            selection_sound.play()
            
        if typed_word == selected_word:
            selection_sound = mixer.Sound('assets/audio/explosion.wav')
            selection_sound.play()
            
            pygame.time.delay(20)
            # Delete the word from the screen
            for text in text_list:
                if text.text == typed_word:
                    text_list.remove(text)

            print("\'" + selected_word + "\' successfully typed")
            word_list.remove(selected_word)
            selected_word_index = 0
            typed_word = ''
            selected_word = None
            
    pygame.time.delay(50 - (wave * 4))
    for obj in text_list:
        obj.y = obj.y + 1;
        canvas.blit(obj.text_object, (obj.x, obj.y))
        if obj.y >= height:
            print("Game Over")
            word_list.clear()
            text_list.clear()
            last_wave = wave
            functions.save_file(score, last_wave)
            game_over = True
            wave = 0
    
    # Render the currently typed word on the screen
    typed_word_text = font_36.render(typed_word, True, white)
    canvas.blit(typed_word_text, (round((width / 2) - typed_word_text.get_width() / 2), height - (typed_word_text.get_height() * 4)))
    
    current_score = font_24.render("Score: " + str(score), True, white, black)
    current_wave = font_24.render("Wave: " + str(wave), True, white, black)
    
    canvas.blit(current_score, (20, 20))
    canvas.blit(current_wave, (width - 20 - current_wave.get_width(), 20))
    
    player.draw_player(text_list, selected_word, canvas)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
    
    
