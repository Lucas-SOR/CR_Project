import plotly.express as px

def show_map_game(game_data):
    fig = px.choropleth(game_data, locations="ISO",
                        color="played", # played is a column of gapminder
                        hover_name="country_name", # column to add to hover information
                        color_continuous_scale=px.colors.sequential.Plasma)
    return fig