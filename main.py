import pygame 
import modules.word_list_generator as word_generator

pygame.init() 

# CREATING CANVAS 
canvas = pygame.display.set_mode((850, 700))

# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 

# Used to maintain the Game Loop
exit = False

# Initialize the Wave System for Words
wave = 1
word_list = word_generator.generate_words(3 + wave)
print("The words are: " + word_list.__str__())

selected_word = None
typed_word = ''
selected_word_index = 0

def show_menu():
    # Load the background image
    bg = pygame.image.load('assets/BackgroundImg.png')
    bg = pygame.transform.scale(bg, (850, 700))

    menu_font = pygame.font.Font(None, 36)
    option1 = menu_font.render("1. Start Game", True, (255, 255, 255))
    option2 = menu_font.render("2. Quit", True, (255, 255, 255))

    # Calculate the positions of the menu options
    option1_pos = option1.get_rect(center=(850 // 2, 700 // 2 - option1.get_height()))
    option2_pos = option2.get_rect(center=(850 // 2, 700 // 2 + option2.get_height()))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "start"
                elif event.key == pygame.K_2:
                    return "quit"

        # Draw the background image
        canvas.blit(bg, (0, 0))

        # Draw the menu options
        canvas.blit(option1, option1_pos)
        canvas.blit(option2, option2_pos)

        pygame.display.flip()

# Main Game Loop
while not exit:
    menu_selection = show_menu()
    if menu_selection == "quit":
        break
    
    # Update the word list if empty
    if (len(word_list) == 0):
        wave += 1
        word_list = word_generator.generate_words(3 + wave)
        print("The words are: " + word_list.__str__())
    
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
            print("\'" + selected_word + "\' successfully typed" )
            word_list.remove(selected_word)
            selected_word_index = 0
            typed_word = ''
            selected_word = None






    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        pygame.display.update()
    
    
