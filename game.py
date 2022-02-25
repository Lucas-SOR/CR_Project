import time
from progress.spinner import Spinner
import os
import pandas as pd
import numpy as np
import random
from questions import *

global NB_ROUNDS
global NB_PLAYERS


def start_game(verbose: bool = True):
    """
    Starting the game
    """
    if verbose:
        print("=============================")
        spinner = Spinner('Loading game |||')
        start_time = time.time()
        while time.time() - start_time < 5:
            time.sleep(0.2)
            spinner.next()
        print("\n=============================")
        time.sleep(0.2)
        os.system('cls' if os.name == 'nt' else 'clear')

        userInput = input("\nHow many rounds do you want to play? ")
        NB_ROUNDS = userInput
        userInput = input("\nHow many player are there? ")
        NB_PLAYERS = userInput

    df_countries = pd.read_csv('data/countries.csv')

    country_list = get_country_list(df_countries)
    # Pick a random first country 
    country_name = country_list[np.random.randint(0, len(country_list))]

    if verbose:
        print("\nLet's starting in ....") 
        spinner = Spinner('')
        start_time = time.time()
        while time.time() - start_time < 2:
            time.sleep(0.2)
            spinner.next()
        print('\n')
        print(country_name)
        time.sleep(1)
    return df_countries, country_name

# ----------------------------------------------------------------------------------------------------------------------
# UTILS
# ----------------------------------------------------------------------------------------------------------------------

def get_country_list(df_countries):
    """
    From the countries df returns the list of countries

    Function arguments : 
    - df_countries : the countries df

    Returns :
    - country_list : a list of all country names
    """
    country_list = df_countries["country_name"].tolist()
    return country_list


def get_country_capital_dict(df_countries):
    """
    From the countries df create a the country to capital dict

    Function arguments : 
    - df_countries : the countries df

    Return :
    - country_capital_dict : a dict such that dict[country_name] = country_capital
    """
    keys = get_country_list(df_countries)
    values = df_countries["capital_name"].tolist()
    country_capital_dict = {}

    for i in range(len(keys)):
        country_capital_dict[keys[i]] = values[i]

    return country_capital_dict


if __name__ == '__main__':
    playing = True

    # Loading the countries and first country
    df_countries, country_name = start_game()

    country_list = get_country_list(df_countries)

    country_capital_dict = get_country_capital_dict(df_countries)

    country_capital_list, d = generate_country_capital_question(country_name, country_list, country_capital_dict)
    print("\nWhat is the capital of " + country_name + " ? ")
    user_input = input('The choices are: ' + ', '.join(country_capital_list) + "\n")
    print(evaluate_country_capital_question(country_capital_list, d, user_input))
