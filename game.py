import time
from progress.spinner import Spinner
import os
import pandas as pd
import numpy as np
import random

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


def generate_population_question(country_name, error_margin, country_population_dict):
    """
    From a country name, asks the population of the country given an error_margin

    Function arguments :
    - country_name : str of the name of the country
    - error_margin : number between 0 and 1 defining if the answer is "close enough" to the real number
    - country_population_dict : a dict such that dict[country_name] = country_population

    Returns :
    - interval : the acceptation interval (if the input is in the interval, the answer is considered True)
    """

    country_population = country_population_dict[country_name]
    lower = int((1-error_margin) * country_population)
    higher = int((1+error_margin) * country_population)
    interval = [lower, higher]

    return interval


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


def evaluate_population_question(interval, user_input):
    """
    Given a population question, evaluates the user answer

    Function arguments :
    - interval : the acceptation interval (if the input is in the interval, the answer is considered True)
    - user_input : the str input that the user made to answer the population question (here we suppose that it is the guessed population of the country)

    Returns : 
    - evaluation : a bool that is True if the answer is accepted and False else
    """
    lower = interval[0]
    higher = interval[1]
    guessed_population = int(user_input)
    evaluation = (guessed_population >= lower) and (
        guessed_population <= higher)

    return evaluation


def generate_country_capital_question(country_name, country_list, country_capital_dict):
    """
    From a country name, generates a multiple answer question with 4 capital and one correct capital to guess

    Function arguments :
    - country_name : str of the name of the country
    - country_list : a list of all country names
    - country_capital dict : a dict such that dict[country_name] = country_capital

    Returns :
    - list of the country_capital str
    - dict such that dict[country_capital] = True if the capital is correct and False in the other cases
    """

    correct_capital = country_capital_dict[country_name]

    country_capital_list = [correct_capital]

    for _ in range(3):
        found = False  # In case the random country is already selected
        while not found:
            random_country_name = country_list[np.random.randint(
                0, len(country_list))]
            random_capital_name = country_capital_dict[random_country_name]
            found = random_capital_name not in country_capital_list
        country_capital_list.append(random_capital_name)

    random.shuffle(country_capital_list)

    d = {}
    for country_capital in country_capital_list:
        if country_capital == correct_capital:
            d[country_capital] = True
        else:
            d[country_capital] = False

    return country_capital_list, d


def evaluate_country_capital_question(country_capital_list, d, user_input):
    """
    Given a country capital question, evaluates the user answer

    Function arguments :
    - country_capital_list : list of the country_capital
    - d : dict such that dict[country_capital] = True if the country_capital is correct and False else
    - user_input : the str input that the user made to answer the country_capital question (here we suppose that it is the index of the country_capital in the country_capital_list)

    Returns : 
    - evaluation : a bool that is True if the answer is accepted and False else
    """

    user_country_capital_proposal = country_capital_list[int(user_input)]
    evaluation = d[user_country_capital_proposal]
    return evaluation


if __name__ == '__main__':
    playing = True
    start_game()

    df_countries = pd.read_csv('data/countries.csv')

    country_list = get_country_list(df_countries)
    country_name = country_list[np.random.randint(0, len(country_list))]
    country_capital_dict = get_country_capital_dict(df_countries)

    country_capital_list, d = generate_country_capital_question(country_name, country_list, country_capital_dict)
    print("\nWhat is the capital of " + country_name + " ? ")
    user_input = input('The choices are: ' + ', '.join(country_capital_list) + '\n ')
    evaluate_country_capital_question(country_capital_list, d, user_input)
