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


game_data = {'Ger': ['Germany','DEU', 'True'], 'Fr': ['France','FRA','False']}
game_data =  pd.DataFrame.from_dict(game_data, orient='index',columns = ['countries','ISO','played'])

st.plotly_chart(show_map_game(game_data), use_container_width=False)