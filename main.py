import pygame 
import modules.word_list_generator as word_generator
import random
import math
from pygame import mixer

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
font_36 = pygame.font.Font(None, 36)
font_24 = pygame.font.Font(None, 24)

text_list = []

# Background Sound
mixer.music.load('assets/audio/background.mp3')
mixer.music.play(-1)

def show_menu():
    # Load the background image
    bg = pygame.image.load('assets/menu-background.png')
    bg = pygame.transform.scale(bg, (width, height))

    option1 = font_36.render("Press Space to Start", True, white)
    option2 = font_36.render("Press Esc to Quit", True, white)

    # Calculate the positions of the menu options
    option1_pos = option1.get_rect(center=(width // 2, height // 2 - option1.get_height()))
    option2_pos = option2.get_rect(center=(width // 2, height // 2 + option2.get_height()))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                selection_sound = mixer.Sound('assets/audio/selection.wav')
                selection_sound.play()
                if event.key == pygame.K_SPACE:
                    return "start"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"

        # Draw the background image
        canvas.blit(bg, (0, 0))

        # Draw the menu options
        canvas.blit(option1, option1_pos)
        canvas.blit(option2, option2_pos)

        pygame.display.flip()

class Text:
    def __init__(self, text, text_object, text_rect_object) -> None:
        self.text = text
        self.text_object = text_object
        self.text_rect_object = text_rect_object
        self.x = 0
        self.y = 0
    
    text: str
    text_object: pygame.Surface
    text_rect_object: any
    x: int
    y: int
    
def draw_game_over():
    selection_sound = mixer.Sound('assets/audio/game-over.wav')
    selection_sound.play()
                
    bg = pygame.image.load('assets/menu-background.png')
    bg = pygame.transform.scale(bg, (width, height))

    header = font_36.render("Game Over", True, white)
    option1 = font_24.render("Press Space to Restart", True, white)
    option2 = font_24.render("Press Esc to Quit", True, white)
    score_text = font_24.render("Score: " + str(score), True, white)
    wave_text = font_24.render("Wave Reached: " + str(last_wave), True, white)
    
    # Calculate the positions of the menu options
    header_pos = header.get_rect(center=(width // 2, height // 2 - header.get_height() * 2))
    option1_pos = option1.get_rect(center=(width // 2, height // 2 - option1.get_height()))
    option2_pos = option2.get_rect(center=(width // 2, height // 2 + option2.get_height()))
    score_pos = score_text.get_rect(center=(width // 2, height // 2 + score_text.get_height() * 3))
    wave_pos = wave_text.get_rect(center=(width // 2, height // 2 + wave_text.get_height() * 4))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                selection_sound = mixer.Sound('assets/audio/selection.wav')
                selection_sound.play()
                if event.key == pygame.K_SPACE:
                    return "start"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"

        # Draw the background image
        canvas.blit(bg, (0, 0))

        # Draw the menu options
        canvas.blit(header, header_pos)
        canvas.blit(option1, option1_pos)
        canvas.blit(option2, option2_pos)
        canvas.blit(score_text, score_pos)
        canvas.blit(wave_text, wave_pos)
        
        pygame.display.flip()

def draw_player():
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
        menu_selection = show_menu()
        if menu_selection == "start":
            start_menu = False
        if menu_selection == "quit":
            start_menu = False
            break
    
    if game_over:
        game_over_menu = draw_game_over()
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
            text_list.append(Text(word, text, text_rect))
        
        index = 0
        for obj in text_list:
            index += 1
            obj.x = random.randint(round(width/len(text_list) * (index - 1)), round((width - 50)/len(text_list) * index))
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
            game_over = True
            word_list.clear()
            text_list.clear()
            last_wave = wave
            wave = 0
    
    # Render the currently typed word on the screen
    typed_word_text = font_36.render(typed_word, True, white)
    canvas.blit(typed_word_text, (round((width / 2) - typed_word_text.get_width() / 2), height - (typed_word_text.get_height() * 5)))
    
    draw_player()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
    
    
