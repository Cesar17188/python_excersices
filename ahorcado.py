import os
import unicodedata
from random import randint


def clear_window():
    os.system("cls")


def read_words():
    words_play = []

    with open('./archivos/data.txt', 'r', encoding='utf-8') as f:
        for word in f:
            words_play.append(word[:-1])

    assert len(words_play) > 0, 'There is not words in data file'
    return words_play


def select_word(words):
    key_number = randint(0, len(words)-1)
    dict_words = {i: word for i, word in words}
    word_selected = dict_words.get(key_number, '')
    return word_selected


def normalize_str(string):
    assert isinstance(string, str), 'The input should be a string'

    return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode()


def ask_for_letter():
    print('tipe a letter and press enter')
    input_letter = input(': ')

    if len(input_letter) != 1:
        raise ValueError("You must to input almost a letter")
        input('<press enter to conitnue>')
        return None
    return input_letter.lower()


def letter_valid(word, letter):
    valid = False

    special_characters = ['á', 'é', 'í', 'ó', 'ú', 'ü']

    for character in word:
        char = character
        let = letter

        if char in special_characters:
            char = normalize_str(char)

        if let in special_characters:
            let = normalize_str(let)

        if char == let:
            valid = True
    return valid


def render_word(word, tentatives_letters, try_number):
    clear_window()
    template = ''

    for letter in word:
        if letter in list(tentatives_letters):
            template += f' {letter}'
        else:
            template += f' _ '

    if ' _ ' not in template:
        clear_window()
        print('============= YOU WIN ===========')
        print('WORD: ', word)
        print(f'Con {try_number} Intentos restantes')
        input('<press enter to restar the game or ctrl +c to exit>')
        run()

    print('Intentos restantes: ', '=' * 5, try_number, '='*5)
    print('WORD: ', template)


def render_gallow(try_number):
    """Renders the gallow scene based on the strikes.

    Strike description:
    - For 0 it will render just the gallow
    - For 1 it will render the head
    - For 2 it will render the torso
    - For 3 it will render the left arm
    - For 4 it will render the right arm
    - For 5 it will render the left leg
    - For 6 it will render the right leg
    """
    template = """
**  **    ***    **   **  *******   **      **    ***    **   **  
**  **   ** **   ***  **  **        ***    ***   ** **   ***  **  
******   *****   **** **  **  ***   ****  ****   *****   **** **  
**  **  **   **  ** ****  **   **   ** **** **  **   **  ** ****  
**  **  **   **  **  ***  *******   **  **  **  **   **  **  ***  
        ||===================
        ||                            
        ||                            
        ||                            
        ||                            
        ||                            
        ||                            
        ||                            
        ||                            
        ||                            
        ||                            
        ||                            
        ==========@          ======== 
        ||                         || 
        ||                         || 
        ||                         || 
        """

    head = (
        (8, 23, '|',),
        (9, 23, '|',),
        (10, 22, '_',),
        (10, 23, '_',),
        (10, 24, '_',),
        (11, 20, '|',),
        (11, 22, '.',),
        (11, 24, '.',),
        (11, 26, '|',),

        (12, 21, '\\',),
        (12, 23, '_',),
        (12, 25, '/',),
    )

    torso = (
        (13, 23, '|',),
        (13, 24, '|',),
        (14, 23, '|',),
        (14, 24, '|',),
        (15, 23, '|',),
        (15, 24, '|',),
        (16, 23, '|',),
        (16, 24, '|',),
    )

    left_arm = (
        (14, 20, '=',),
        (14, 21, '=',),
        (14, 22, '=',),
    )
    right_arm = (
        (14, 25, '=',),
        (14, 26, '=',),
        (14, 27, '=',),
    )

    left_leg = (
        (17, 22, '/',),
        (17, 23, '/',),
        (18, 21, '/',),
        (18, 22, '/',),
    )
    right_leg = (
        (17, 24, '\\',),
        (17, 25, '\\',),
        (18, 25, '\\',),
        (18, 26, '\\',),
    )
    tramp_closed = (
        (19, 19, '=',),
        (19, 20, '=',),
        (19, 21, '=',),
        (19, 22, '=',),
        (19, 23, '=',),
        (19, 24, '=',),
        (19, 25, '=',),
        (19, 26, '=',),
        (19, 27, '=',),
    )
    tramp_opened = (
        (19, 19, '\\',),
        (19, 20, '\\',),
        (20, 20, '\\',),
        (20, 21, '\\',),
        (21, 21, '\\',),
        (21, 22, '\\',),
        (22, 22, '\\',),
        (22, 23, '\\',),
    )

    scene_descriptors = []

    if try_number <= 6:
        scene_descriptors += head
    if try_number <= 5:
        scene_descriptors += torso
    if try_number <= 4:
        scene_descriptors += left_arm
    if try_number <= 3:
        scene_descriptors += right_arm
    if try_number <= 2:
        scene_descriptors += left_leg
    if try_number <= 1:
        scene_descriptors += right_leg

    if try_number == 0:
        scene_descriptors += tramp_closed
    else:
        scene_descriptors += tramp_opened

    lines = [list(line) for line in template.splitlines()]

    for descriptor in scene_descriptors:
        lines[descriptor[0]][descriptor[1]] = descriptor[2]

    scene = '\n'.join([''.join(l) for l in lines])
    print(scene)


def initial_game(word):
    try_number = 6
    tentatives_letters = []
    while try_number > 0:
        letter = ask_for_letter()
        if letter:
            valid_letter = letter_valid(word, letter)
            if valid_letter:
                tentatives_letters.append(letter)
                render_word(word, tentatives_letters, try_number)
            else:
                try_number = try_number - 1
                render_word(word, tentatives_letters, try_number)

        if try_number == 0:
            print('================ Game Over ==================')
            render_gallow(try_number)
            print(f'WORD: ', word)
            input('<press enter to restart the game or ctrl + c to exit>')
            try_number = 6
            run()
            continue


def run():
    os.system("cls")
    words = list(enumerate(read_words()))
    word = select_word(words)
    initial_game(word)


if __name__ == '__main__':
    run()
