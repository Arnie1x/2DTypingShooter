import pygame
import json
from pygame import mixer

pygame.font.init()

white = (255, 255, 255)
font_24 = pygame.font.Font('assets/fonts/Poppins-Regular.ttf', 24)
font_36 = pygame.font.Font('assets/fonts/Poppins-Regular.ttf', 36)
width = 850
height = 700

def draw_game_over(score, last_wave, canvas):
    selection_sound = mixer.Sound('assets/audio/game-over.wav')
    selection_sound.play()
                
    bg = pygame.image.load('assets/menu-background.png')
    bg = pygame.transform.scale(bg, (width, height))
    
    high_score = 0
    highest_wave = 0
    
    f = open('save_file.json')
    in_file = json.load(f)
    
    if in_file['high_score']:
        high_score = in_file['high_score']
        highest_wave = in_file['highest_wave']

    header = font_36.render("Game Over", True, white)
    option1 = font_24.render("Press Space to Restart", True, white)
    option2 = font_24.render("Press Esc to Quit", True, white)
    score_text = font_24.render("Score: " + str(score), True, white)
    high_score_text = font_24.render("High Score: " + str(high_score), True, white)
    wave_text = font_24.render("Wave Reached: " + str(last_wave), True, white)
    highest_wave_text = font_24.render("Highest Wave: " + str(highest_wave), True, white)
    
    # Calculate the positions of the menu options
    header_pos = header.get_rect(center=(width // 2, height // 2 - header.get_height() * 2))
    option1_pos = option1.get_rect(center=(width // 2, height // 2 - option1.get_height()))
    option2_pos = option2.get_rect(center=(width // 2, height // 2 + option2.get_height()))
    score_pos = score_text.get_rect(center=(width // 2, height // 2 + score_text.get_height() * 3))
    high_score_pos = high_score_text.get_rect(center=(width // 2, height // 2 + high_score_text.get_height() * 4))
    wave_pos = wave_text.get_rect(center=(width // 2, height // 2 + wave_text.get_height() * 6))
    highest_wave_pos = highest_wave_text.get_rect(center=(width // 2, height // 2 + highest_wave_text.get_height() * 7))
    
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
        canvas.blit(high_score_text, high_score_pos)
        canvas.blit(highest_wave_text, highest_wave_pos)
        
        pygame.display.flip()
        
def show_menu(canvas):
    # Load the background image
    bg = pygame.image.load('assets/menu-background.png')
    bg = pygame.transform.scale(bg, (width, height))

    title = font_36.render("SpaceType", True, white)
    option1 = font_24.render("Press Space to Start", True, white)
    option2 = font_24.render("Press Esc to Quit", True, white)

    # Calculate the positions of the menu options
    header_pos = title.get_rect(center=(width // 2, height // 2 - option1.get_height() * 3))
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
        canvas.blit(title, header_pos)
        canvas.blit(option1, option1_pos)
        canvas.blit(option2, option2_pos)

        pygame.display.flip()
        
def save_file(score, last_wave):
    high_score = 0
    highest_wave = 0
    
    f = open('save_file.json')
    in_file = json.load(f)
    
    if in_file['high_score']:
        high_score = in_file['high_score']
        highest_wave = in_file['highest_wave']

    if score >= high_score:
        high_score = score
    
    if last_wave >= highest_wave:
        highest_wave = last_wave
        
    data = {
        "high_score": high_score,
        "highest_wave": highest_wave,
	}
    out_file = open('save_file.json', 'w')
    json.dump(data, out_file, indent = 6)
    f.close()
    out_file.close()