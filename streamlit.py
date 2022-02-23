import streamlit as st
import pandas as pd
from utils.map import *

# ----------------------------------------------------------------------------------------------------------------------
# To run locally run: 'streamlit run streamlit.py'
# ----------------------------------------------------------------------------------------------------------------------


@st.cache
def load_data(path):
    data = pd.read_csv(path)
    return data


st.sidebar.image("https://media.giphy.com/media/mf8UbIDew7e8g/giphy.gif")
NB_PLAYERS = st.sidebar.selectbox(
    "Nombre de joueurs:", [1, 2, 3, 4, 5])
NB_ROUNDS = st.sidebar.selectbox(
    "Nombre de rounds:", [1, 2, 3, 4, 5])

game_data = load_data('data/countries.csv')
game_data['played'] = game_data.apply(lambda x: False, axis=1)

st.plotly_chart(show_map_game(game_data), use_container_width=False)
