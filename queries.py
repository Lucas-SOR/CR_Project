from SPARQLWrapper import SPARQLWrapper, JSON, XML
import ssl
import pandas as pd
import pycountry
import urllib.request
from PIL import Image
import time
import shutil
import requests
from transformers import pipeline
from spacy.lang.en import English


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

def get_summarizer():
    """
    Get the summarizer
    Returns :
    - summarizer : the summarizer model from transformers
    """
    summarizer = pipeline("summarization")
    return summarizer

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

def summarize(text,summarizer, sentencizer):
    """
    Summarizes the given text.

    Function arguments :   
    - text : the text to summarize
    - summarizer : the summarizer model
    - sentencizer : the sentencizer model

    Returns :
    -summarized_text : the summarized text computed with the given model

    """

    print(text) #See where we are at in the apply method for get_summarized_column
    
    max_chunk = 500 #Because of input size limits for transformers

    #Separating sentences
    
    sentences = get_sentences(text, sentencizer)

    #Creating chunks of sentences of limited size (with regard to max_chunk)
    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])

    #summarizing the chunks one by one
    summarized_text_list = summarizer(chunks, max_length=300, min_length=150, do_sample=False)

    summarized_text = ' '.join([summ['summary_text'] for summ in summarized_text_list])

    summarized_text.replace(" . ", ". ")

    return summarized_text


def get_summarized_column(df_countries):
    """
    This function adds the summarized column to the dataframe

    Function arguments :
    df_countries : the coutries df

    Returns
    df_countries_with_sum : the countries df with the summarized abstract as the last column
    """

    sentencizer = get_sentencizer()
    summarizer = get_summarizer()

    df_countries["country_summarized_abstract"] = df_countries["country_abstract"].apply(lambda x : summarize(x,summarizer,sentencizer))

    return df_countries


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

    countries = get_summarized_column(countries)

    return countries


if __name__ == '__main__':
    countries = load_fulldata()
    countries.to_csv('data/countries.csv')
