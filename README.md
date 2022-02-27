# CR_Project

This is the project for the "Connaissance et Raisonnement" course @CentraleSupélec

#### Due date
:calendar: **28/02/2021**  

## :books: Subject of the project  

The aim of this project is to program a game in which the player starts in a random country and must go through the maximum countries possible. To move, the player must give the name of a neighboring country (with regards to the contry he is in) and answer a given question (finding the capital, the number of people living there, a trivia question about the local traditions, etc). 

The data that will be used to build this game will be taken from [DBpedia](https://www.dbpedia.org/resources/) and [Wikidata](https://www.wikidata.org/wiki/Q6256).

## :runner: Running the code
``sparql_test.ipynb`` allows to generate the dataframe and country_flags for this project 

First install the required dependancies: 
```bash
pip install -r requirements.txt
```

To run the game, you can either: 

0. Running the SPARQL queries to gather the data 
```bash
python3 queries.py
```

1. Run the command line interface of the game 
```bash
python3 game.py
```

2. Use the front-end with streamlit
```bash
streamlit run streamlit.py
```

## :package: Organisation of the project

### Structure

```bash 
.
├── README.md
├── country_flags
│   ├── Afghanistan_flag.png
│   ├── Albania_flag.png
│   ├── .... 
│   └── Zimbabwe_flag.png
├── data
│   └── countries.csv 
├── game.py #Mechanisms and CLI for the game 
├── notebooks
│   ├── sparql_test.ipynb 
│   └── tests.ipynb
├── queries
│   ├── sparql_query.txt #Querying DBPedia
│   └── sparql_wikidata_query.txt #Querying WikiData
├── queries.py #Querying DBPedia & Wikidata for data
├── questions.py #Creatin questions
├── requirements.txt 
├── streamlit.py #Front-end for the game
├── test_pytest.py
└── utils
    ├── helpers.py
    └── map.py
```
### :warning: Technical choice

We chose to compute two full SPARQL request and then use a structured dabase for three reasons:
1. the latency of the SPARQL requests 
2. the need of a network connection to use the game
3. the need of full data to train our NLP model

### TO DO LIST

- [x] Packaging du code @ArianeDlns -> `main.py`
- [x] Développer les questions (Drapeaux/Capitales/Population) @ArianeDlns @Lucas-SOR -> `game.py`
- [x] Pays adjacents @ArianeDlns  -> `queries/sparql_wikidata_query.txt`
- [x] MVP du jeu @ArianeDlns @Lucas-SOR
- [ ] Front-end en streamlit @ArianeDlns @Lucas-SOR
- [x] Développement de Question Answering (NLP) sur les abstract par pays  @Lucas-SOR
- [ ] Score de similarité par drapeau @Lucas-SOR [Pas priori]
- [ ] Rapport sur Overleaf @ArianeDlns @Lucas-SOR
- [ ] Fix missing countries @Lucas-SOR
- [x] Adding summarization steps in queries.py to generate countries.csv @Lucas-SOR

## References 