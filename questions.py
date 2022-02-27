import pandas as pd
import numpy as np
import random

# ----------------------------------------------------------------------------------------------------------------------
# POPULATION
# ----------------------------------------------------------------------------------------------------------------------


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

# ----------------------------------------------------------------------------------------------------------------------
# CAPITAL CITY
# ----------------------------------------------------------------------------------------------------------------------


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

# ----------------------------------------------------------------------------------------------------------------------
# FLAG
# ----------------------------------------------------------------------------------------------------------------------


def generate_flag_question(country_name, country_list):
    """
    From a country name, generates a multiple answer question with 4 flags and one correct flag to guess

    Function arguments :
    - country_name : str of the name of the country
    - country_list : a list of all country names

    Returns :
    - country_flag_filename_list : list of the country_flag filenames
    - d : dict such that dict[flag_filename] = True if the flag is correct and False in the other cases
    """
    correct_flag_filename = "../country_flags/" + country_name + "_flag.png"

    country_flag_filename_list = [correct_flag_filename]

    for _ in range(3):
        found = False  # In case the random country is already selected
        while not found:
            random_country_name = country_list[np.random.randint(
                0, len(country_list))]
            random_country_flag_filename = "../country_flags/" + \
                random_country_name + "_flag.png"
            found = random_country_flag_filename not in country_flag_filename_list
        country_flag_filename_list.append(random_country_flag_filename)

    random.shuffle(country_flag_filename_list)

    d = {}

    for country_flag_filename in country_flag_filename_list:
        if country_flag_filename == correct_flag_filename:
            d[country_flag_filename] = True
        else:
            d[country_flag_filename] = False

    return country_flag_filename_list, d


def evaluate_country_flag_question(country_flag_filename_list, d, user_input):
    """
    Given a flag question, evaluates the user answer

    Function arguments :
    - country_flag_filename_list : list of the country_flag filenames
    - d : dict such that dict[flag_filename] = True if the flag_filename is correct and False else
    - user_input : the str input that the user made to answer the flag question (here we suppose that it is the index of the flag in the country_flag_filename_list)

    Returns : 
    - evaluation : a bool that is True if the answer is accepted and False else
    """
    user_flag_filename_proposal = country_flag_filename_list[int(user_input)]
    evaluation = d[user_flag_filename_proposal]
    return evaluation

# ----------------------------------------------------------------------------------------------------------------------
# NLP
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# GLOBAL
# ----------------------------------------------------------------------------------------------------------------------

def generate_random_question(allow_FLAG: bool = False):
    """
    Pick a random question 
    Returns : 
    - evaluation : a bool that is True if the answer is accepted and False else
    """
    if allow_FLAG:
        question = ['Population', 'Capital', 'Flag', 'NLP']
    else:
        question = ['Population', 'Capital', 'NLP']
    pick = random.shuffle(question)[0]
    if pick == 'Population':
        pass
    elif pick == 'Capital':
        pass
    elif pick == 'Flag':
        pass
    else:
        pass
    return pick