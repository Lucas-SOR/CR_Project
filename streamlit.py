from turtle import onclick
import streamlit as st
import pandas as pd
from utils.map import *
from questions import *
import random
from PIL import Image

# ----------------------------------------------------------------------------------------------------------------------
# To run locally run: 'streamlit run streamlit.py'
# ----------------------------------------------------------------------------------------------------------------------

if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

if 'show_question' not in st.session_state:
    st.session_state.show_question = False

if 'question_type' not in st.session_state:
    st.session_state.question_type = 1

if 'current_question' not in st.session_state:
    st.session_state.current_question = "this is question"

if 'current_proposals' not in st.session_state:
    st.session_state.current_proposals = [None for _ in range(4)]

if 'current_answer' not in st.session_state:
    st.session_state.current_answer = "this is answer"

if 'country_name' not in st.session_state:
    st.session_state.country_name = None

if 'user_input' not in st.session_state:
    st.session_state.user_input = 0

if 'd' not in st.session_state:
    st.session_state.d = {}


@st.cache()
def load_data(path):
    data = pd.read_csv(path)
    return data


def load_ner_model():
    return get_ner_model()


if 'ner_model' not in st.session_state:
    st.session_state.ner_model = load_ner_model()


def load_sentencizer():
    return get_sentencizer()


if 'sentencizer' not in st.session_state:
    st.session_state.sentencizer = load_sentencizer()


def get_s2v_model():
    return get_s2v()


if 's2v_model' not in st.session_state:
    st.session_state.s2v_model = get_s2v_model()


game_data = load_data('data/countries.csv')


def show_answer():
    st.session_state.show_answer = True


def get_question():
    st.session_state.question_type = random.randint(0, 3)
    st.session_state.show_question = True
    st.session_state.show_answer = False

    if st.session_state.question_type == 0 and st.session_state.show_question:  # population

        st.session_state.country_name = game_data["country_name"][idx]
        st.session_state.current_question = "What is the population of the country ? (error margin of 10%)"
        error_margin = 0.1
        country_population_dict = get_country_population_dict(game_data)

        st.session_state.current_proposals = generate_population_question(
            st.session_state.country_name, error_margin, country_population_dict)

    if st.session_state.question_type == 1 and st.session_state.show_question:  # capital
        st.session_state.country_name = game_data["country_name"][idx]

        st.session_state.current_question = "What is the capital of country ?"

        country_list = get_country_list(game_data)

        country_capital_dict = get_country_capital_dict(game_data)

        st.session_state.current_proposals, st.session_state.d = generate_country_capital_question(
            st.session_state.country_name, country_list, country_capital_dict)

    if st.session_state.question_type == 2 and st.session_state.show_question:  # flag
        st.session_state.country_name = game_data["country_name"][idx]
        st.session_state.current_question = "What is the flag of country ?"

        country_list = get_country_list(game_data)

        st.session_state.current_proposals, st.session_state.d = generate_flag_question(
            st.session_state.country_name, country_list)

    if st.session_state.question_type == 3 and st.session_state.show_question:  # QG
        st.session_state.country_name = game_data["country_name"][idx]

        country_list = get_country_list(game_data)

        st.session_state.current_question, st.session_state.current_proposals, st.session_state.d = get_abstract_question_from_index(
            game_data, idx, st.session_state.s2v_model, st.session_state.sentencizer, st.session_state.ner_model)


st.sidebar.image("https://media.giphy.com/media/mf8UbIDew7e8g/giphy.gif")
NB_PLAYERS = st.sidebar.selectbox(
    "Nombre de joueurs:", [1, 2, 3, 4, 5])
NB_ROUNDS = st.sidebar.selectbox(
    "Nombre de rounds:", [1, 2, 3, 4, 5])

# game_data['played'] = game_data.apply(lambda x: False, axis=1) # A changer pour pas changer la valeur de game_data (immutable), faut faire une copie en fait
# st.plotly_chart(show_map_game(game_data), use_container_width=False)

idx = st.number_input("index dans le CSV", min_value=0,
                      max_value=len(game_data)-1)

st.button("Generate_question !", on_click=get_question)


if st.session_state.show_question:

    st.write(f"You are in {st.session_state.country_name} !")

    #st.write(st.session_state.question_type, st.session_state.show_question)  # For debug

    st.session_state.current_question

    if st.session_state.question_type == 0:  # Population
        st.session_state.user_input = st.number_input("Answer", min_value=0)

    if st.session_state.question_type == 1:  # Capitals
        c1, c2 = st.columns(2)

        for i in range(2):
            c1.write(str(2*i) + ". " + st.session_state.current_proposals[2*i])
            c2.write(str(2*i+1) + ". " +
                     st.session_state.current_proposals[2*i+1])

        st.session_state.user_input = st.number_input(
            "Answer (index of solution)", min_value=0)

    if st.session_state.question_type == 2:  # Flags
        c1, c2 = st.columns(2)

        for i in range(2):
            c1.write(str(2*i) + ".")
            c1.image(Image.open(st.session_state.current_proposals[2*i]))
            c2.write(str(2*i+1) + ".")
            c2.image(Image.open(st.session_state.current_proposals[2*i+1]))

        st.session_state.user_input = st.number_input(
            "Answer (index of solution)", min_value=0)

    if st.session_state.question_type == 3:  # QG
        c1, c2 = st.columns(2)

        for i in range(2):
            c1.write(str(2*i) + ". " + st.session_state.current_proposals[2*i])
            c2.write(str(2*i+1) + ". " +
                     st.session_state.current_proposals[2*i+1])

        st.session_state.user_input = st.number_input(
            "Answer (index of solution)", min_value=0)

    st.button("Validate answer", on_click=show_answer)
    
if st.session_state.show_answer:

    if st.session_state.question_type == 0:  # Population
        st.session_state.current_answer = game_data["country_population"][idx]
        st.write(evaluate_population_question(st.session_state.current_proposals,
                 st.session_state.user_input), f"Correct population was : {st.session_state.current_answer} !")

    if st.session_state.question_type == 1:  # Capitals
        st.session_state.current_answer = game_data["capital_name"][idx]
        st.write(evaluate_country_capital_question(st.session_state.current_proposals, st.session_state.d,
                 st.session_state.user_input), f"Correct capital was : {st.session_state.current_answer} !")

    if st.session_state.question_type == 2:  # Flags
        st.write(evaluate_country_flag_question(st.session_state.current_proposals,
                 st.session_state.d, st.session_state.user_input), f"Correct flag was : ")
        st.image(Image.open("country_flags/" +
                 st.session_state.country_name + "_flag.png"))

    if st.session_state.question_type == 3:  # QG
        for key in st.session_state.current_proposals:
            if st.session_state.d[key]:
                st.session_state.current_answer = key
        st.write(evaluate_abstract_question(st.session_state.current_proposals, st.session_state.d,
                 st.session_state.user_input), f"Correct answer was : {st.session_state.current_answer} !")
