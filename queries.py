from SPARQLWrapper import SPARQLWrapper, JSON, XML
import ssl
import pandas as pd
import urllib.request
from PIL import Image
import time
import shutil
import requests

ssl._create_default_https_context = ssl._create_unverified_context

def query_sparql(path_to_query:str = 'queries/sparql_query.txt'):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    with open(path_to_query) as f:
        QUERY = f.read()
        sparql.setQuery(QUERY)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    columns = results['head']['vars']

    d = {}
    for col_name in columns: 
        d[col_name] = []

    for result in results["results"]["bindings"]:
        for col_name in columns:  
            d[col_name].append(result[col_name]["value"])

    df_cities = pd.DataFrame(d)
    return df_cities 

if __name__ == '__main__':
    query_sparql()