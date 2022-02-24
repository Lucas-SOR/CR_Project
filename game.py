import time
from progress.spinner import Spinner
import os

global NB_ROUNDS 
global NB_PLAYERS 

def start_game(verbose: bool=True):
    if verbose:
        print("=============================")
        spinner = Spinner('Loading game |||')
        start_time = time.time()
        while time.time() - start_time < 5 :
            time.sleep(0.2)
            spinner.next()
        print("\n=============================")
        time.sleep(0.2)
        os.system('cls' if os.name == 'nt' else 'clear')


    userInput = input("\nHow many rounds do you want to play? ")
    NB_ROUNDS = userInput
    userInput = input("\nHow many player are there? ")
    NB_PLAYERS = userInput

if __name__ == '__main__':
    playing = True 
    start_game()
        