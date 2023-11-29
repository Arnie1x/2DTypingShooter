import pygame 
import modules.word_list_generator as word_generator
import random

pygame.init() 

# CREATING CANVAS 
width = 850
height = 700
canvas = pygame.display.set_mode((width, height))

# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 

# Used to maintain the Game Loop
exit = False
start_menu = True

# Initialize the Wave System for Words
wave = 0
word_list = []
# word_list = word_generator.generate_words(3 + wave)
# print("The words are: " + word_list.__str__())

selected_word = None
typed_word = ''
selected_word_index = 0

# Constants
white = (255, 255, 255)
font = pygame.font.Font(None, 36)

text_list = []

def show_menu():
    # Load the background image
    bg = pygame.image.load('assets/BackgroundImg.png')
    bg = pygame.transform.scale(bg, (width, height))

    option1 = font.render("Press Space to Start", True, white)
    option2 = font.render("Press Esc to Quit", True, white)

    # Calculate the positions of the menu options
    option1_pos = option1.get_rect(center=(width // 2, height // 2 - option1.get_height()))
    option2_pos = option2.get_rect(center=(width // 2, height // 2 + option2.get_height()))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
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
    def __init__(self, text_object, text_rect_object) -> None:
        self.text_object = text_object
        self.text_rect_object = text_rect_object
        self.x = 0
        self.y = 0
    
    text_object: pygame.Surface
    text_rect_object: any
    x: int
    y: int

# Main Game Loop
while not exit:
    if start_menu:
        menu_selection = show_menu()
        if menu_selection == "start":
            start_menu = False
        if menu_selection == "quit":
            start_menu = False
            break
    
    canvas.fill((0,0,0))
    
    # Update the word list if empty
    if (len(word_list) == 0):
        wave += 1
        word_list = word_generator.generate_words(3 + wave)
        print("The words are: " + word_list.__str__())
        for word in word_list:
            text = font.render(word, True, white)
            text_rect = text.get_rect()
            text_rect.center = (width, height)
            text_list.append(Text(text, text_rect))
        
        index = 0
        for obj in text_list:
            index += 1
            obj.x = random.randint(round(width/len(text_list) * (index - 1)), round(width/len(text_list) * index))
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
            break
        
    if selected_word is not None:
        if keys[pygame.key.key_code(selected_word[selected_word_index])] and len(selected_word) != selected_word_index:
            typed_word += selected_word[selected_word_index]
            selected_word_index += 1
            print("Typed Word: " + typed_word)
            
        if typed_word == selected_word:
            print("\'" + selected_word + "\' successfully typed")
            word_list.remove(selected_word)
            selected_word_index = 0
            typed_word = ''
            selected_word = None
            
    for obj in text_list:
        pygame.time.delay(10)
        obj.y = obj.y + 1;
        canvas.blit(obj.text_object, (obj.x, obj.y))
        if obj.y >= height:
            print("Game Over")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()
    
    
