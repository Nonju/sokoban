# -*- coding: utf-8 -*-

import os

def clear():
    os.system('clear')

def cmd(command):
    os.system(command)

def menu():
    while True:
        clear()

        print('-' * 30)
        print('|', ' ' * 8, 'Sokoban!', ' ' * 8, '|')
        print('-' * 30)

        print('Shell (1)')
        print('PyGame (2)')
        print('Avsluta (Q)')
        choice = input('Choose game >> ')

        if choice.lower() == 'q':
            break

        try: choice = int(choice)
        except: continue

        if choice == 1:
            cmd('make start-sh')
        elif choice == 2:
            cmd('make start-pygame')

if __name__ == '__main__':
    menu()

