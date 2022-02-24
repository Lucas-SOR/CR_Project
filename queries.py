from SPARQLWrapper import SPARQLWrapper, JSON, XML
import ssl
import pandas as pd
import pycountry
import urllib.request
from PIL import Image
import time
import shutil
import requests

ssl._create_default_https_context = ssl._create_unverified_context


def transform_data(results):
    """
    This function transform a SPARQL result into a DataFrame

    Returns : 
    - data : The DataFrame 
    """
    columns = results['head']['vars']
    d = {}
    for col_name in columns:
        d[col_name] = []

    for result in results["results"]["bindings"]:
        for col_name in columns:
            d[col_name].append(result[col_name]["value"])

    data = pd.DataFrame(d)
    return data


def query_sparql(path_to_query: str = 'queries/sparql_query.txt'):
    """
    This function makes the SPARQL request to DBpedia to get the countries df

    Returns : 
    - data : The DataFrame of countries information
    """
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    with open(path_to_query) as f:
        QUERY = f.read()
        sparql.setQuery(QUERY)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = transform_data(results)
    return data


def query_wikidata(path_to_query: str = 'queries/sparql_wikidata_query.txt'):
    """
    This function makes the SPARQL request to WikiData to get the frontiers 

    Returns : 
    - data : The DataFrame of frontiers information
    """
    url = 'https://query.wikidata.org/sparql'

    with open(path_to_query) as f:
        QUERY = f.read()
    r = requests.get(url, params={'format': 'json', 'query': QUERY})
    results = r.json()

    data = transform_data(results)
    return data


def load_fulldata():
    """
    This function loads and merge all the data

    Returns : 
    - countries : The DataFrame of with countries and frontiers informations
    """
    df_countries = query_sparql()
    df_borders = query_wikidata()

    # Adding ISO Code
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3

    codes = [countries.get(country, 'Unknown code')
             for country in df_countries.country_name]
    df_countries['ISO'] = codes

    # Preparing the borders
    df_borders_land = df_borders[df_borders['isLandBorder'] == 'true']
    df_borders_tbm = df_borders_land[['country1Label', 'country2Label']].groupby(
        'country1Label').agg({'country2Label': list}).reset_index()

    # Preparing the borders
    countries = pd.merge(df_countries, df_borders_tbm,
                         right_on='country1Label', left_on='country_name', how='left')
    return countries


if __name__ == '__main__':
    countries = load_fulldata()
    countries.to_csv('data/countries.csv')
