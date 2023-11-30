import pygame
from pygame import mixer

def read_input(typed_word, text_list, word_list, selected_word, selected_word_index, score):
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
            
    return typed_word, selected_word_index, score