import streamlit as st
import pandas as pd

# ----------------------------------------------------------------------------------------------------------------------
# To run locally run: 'streamlit run streamlit.py'
# ----------------------------------------------------------------------------------------------------------------------

@st.cache
def load_data(path):
    data = pd.read_csv(path)
    return data

st.sidebar.image("https://media.giphy.com/media/mf8UbIDew7e8g/giphy.gif")