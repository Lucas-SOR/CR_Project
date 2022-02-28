import pandas as pd
import numpy as np
import random
import spacy
from collections import OrderedDict
from spacy.lang.en import English
from sense2vec import Sense2Vec
# ----------------------------------------------------------------------------------------------------------------------
# UTILS FOR QUESTION GENERATIONS
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


def get_country_population_dict(df_countries):
    """
    From the cities df create a the country to capital dict

    Function arguments : 
    - df_countries : the countries df

    Returns :
    - country_population_dict : a dict such that dict[country_name] = country_population
    """
    keys = get_country_list(df_countries)
    values = df_countries["country_population"].tolist()
    country_population_dict = {}

    for i in range(len(keys)):
        country_population_dict[keys[i]] = values[i]

    return country_population_dict

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
    correct_flag_filename = "country_flags/" + country_name + "_flag.png"

    country_flag_filename_list = [correct_flag_filename]

    for _ in range(3):
        found = False  # In case the random country is already selected
        while not found:
            random_country_name = country_list[np.random.randint(
                0, len(country_list))]
            random_country_flag_filename = "country_flags/" + \
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


def get_sentencizer():
    """
    Get the sentencizer
    Returns :
    - sentencizer : the sentencizer model from spacy
    """
    sentencizer = English()
    sentencizer.add_pipe('sentencizer')
    return sentencizer


def get_sentences(text, sentencizer):
    """
    Divide a text into a list of sentences (.split() method is not good because of words with '.' in it)

    Function arguments : 
    - text : the text to summarize
    - sentencizer : the sentencizer model

    Returns:

    - sentences : the list of sentences in the text
    """

    doc = sentencizer(text)

    sentences = [sent.text.strip() for sent in doc.sents]

    return sentences


def get_ner_model():
    """
    Get the ner_model

    Returns:
    - ner_model : the ner_model from spacy
    """
    ner_model = spacy.load("en_core_web_sm")
    return ner_model


def get_s2v():
    s2v = Sense2Vec().from_disk('s2v_model')
    return s2v


def extract_person_gpe(text, ner_model, sentencizer, country_name):
    """
    Extracts the keywords corresponding to places or person in the text

    Function arguments :
    - text : the text from which to extract the keyphrases
    - ner_model : the ner_model from spacy
    - sentencizer : the sentencizer model

    Returns :
    sentence_keyword_dict : a dict such that dict[sentence] = list of keywords 
    """

    sentence_list = get_sentences(text, sentencizer)

    sentence_keyword_dict = {}

    for sentence in sentence_list:
        doc = ner_model(sentence)
        keywords = []
        for ent in doc.ents:
            if ent.label_ in ["GPE", "PERSON"]:
                if ent.text != country_name:
                    keywords.append(ent.text)

        if keywords != []:
            sentence_keyword_dict[sentence] = keywords

    return sentence_keyword_dict


def generate_distractors_from_word(word, s2v):
    """
    Generates a distractor list from a given word

    Function arguments :
    - word : the word to generate distractors from
    - s2v : the sentence to vector model

    Returns :
    - disctractors_list : a list of 3 distractors of the word
    """

    output = []
    word = word.lower()
    word = word.replace(" ", "_")

    sense = s2v.get_best_sense(word)
    most_similar = s2v.most_similar(sense, n=20)

    for each_word in most_similar:
        append_word = each_word[0].split("|")[0].replace("_", " ").lower()
        if append_word.lower() != word:
            output.append(append_word.title())

    disctractors_list = list(OrderedDict.fromkeys(output))

    to_remove = []
    for distractor in disctractors_list:
        if distractor.lower() == word:
            to_remove.append(distractor)

    for distractor in to_remove:
        disctractors_list.remove(distractor)

    return random.choices(disctractors_list, k=3)


def get_abstract_question_from_index(df_countries, index, s2v, sentencizer, ner_model):
    """
    Generates a question from and index of the dataset

    Function arguments : 
    - df_countries : the countries df
    - index : int representing the index of the row to create the question from
    - s2v : the s2v model
    - sentencizer : the sentencizer model
    - ner_model : the ner_model from spacy

    Returns :
    - question : a fill the blank question where the blank is in the form of underscores "_____"
    - answers : a list of 4 possible answers, one true and three disctractors
    - verify_answer : a dict such that verify_answer[answer] == True if and only if the answer is the good one for the question
    """

    try:

        country_name = df_countries["country_name"][index]

        summarized_abstract = df_countries["country_summarized_abstract"][index]

        sentence_keyword_dict = extract_person_gpe(
            summarized_abstract, ner_model, sentencizer, country_name)

        sentence = random.choice(list(sentence_keyword_dict.keys()))

        keyword = random.choice(sentence_keyword_dict[sentence])

        question = sentence.replace(keyword, "_____")

        question = "Fill in the blank : " + question

        answers = generate_distractors_from_word(keyword, s2v)

        answers.append(keyword)

        random.shuffle(answers)

        verify_answer = {}
        for answer in answers:
            if answer == keyword:
                verify_answer[answer] = True
            else:
                verify_answer[answer] = False

        return question, answers, verify_answer

    except:
        BADLY_GENERATED_QUESTION = "Question was badly generated, please validate any answer to validate and move on"
        BADLY_GENERATED_ANSWERS = ["Any answer" for _ in range(4)]
        BADLY_GENERATED_D = {k: True for k in BADLY_GENERATED_ANSWERS}

        return BADLY_GENERATED_QUESTION, BADLY_GENERATED_ANSWERS, BADLY_GENERATED_D


def evaluate_abstract_question(answers, verify_answer, user_input):
    """
    Given an abstract question, evaluates the user answer

    Function arguments :
    - answers : list of possible answers
    - verify_answer : dict such that verify_answer[answer] = True if the answer is correct and False else
    - user_input : the str input that the user made to answer the flag question (here we suppose that it is the index of the answer in answers)

    Returns : 
    - evaluation : a bool that is True if the answer is accepted and False else
    """
    user_answer = answers[int(user_input)]
    evaluation = verify_answer[user_answer]
    return evaluation


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
    random.shuffle(question)
    pick = question[0]
    if pick == 'Population':
        pass
    elif pick == 'Capital':
        pass
    elif pick == 'Flag':
        pass
    else:
        pass
    return pick
