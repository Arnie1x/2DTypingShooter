import random

def generate_words(word_amount: int):
    words = []
    word_list = open(r"assets/word_list.txt", "r").readlines()
    while len(words) != word_amount:
        new_word = word_list[random.randint(0, len(word_list))]
        similar_alphabet = False
        for word in words:
            if word[0] == new_word[0]:
                similar_alphabet = True
        
        if similar_alphabet == False:
            words.append(new_word.rstrip())
    return words