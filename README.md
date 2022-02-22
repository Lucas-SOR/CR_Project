# CR_Project

This is the project for the "Connaissance et Raisonnement" course @CentraleSupélec

#### Due date
:calendar: **28/02/2021**  

## :books: Subject of the project  

The aim of this project is to program a game in which the player starts in a random country and must go through the maximum countries possible. To move, the player must give the name of a neighboring country (with regards to the contry he is in) and answer a given question (finding the capital, the number of people living there, a trivia question about the local traditions, etc). 

The data that will be used to build this game will be taken from [DBpedia](https://www.dbpedia.org/resources/) and [Wikidata](https://www.wikidata.org/wiki/Q6256).

## :runner: Running the code
``sparql_test.ipynb`` allows to generate the dataframe and country_flags for this project 


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
└── sparql_test.ipynb
```

### TO DO LIST


- [ ] Packaging du code @ArianeDlns
- [ ] Développer les questions (Drapeaux/Capitales/Population) @ArianeDlns @Lucas-SOR
- [ ] Pays adjacents @ArianeDlns
- [ ] MVP du jeu @ArianeDlns @Lucas-SOR
- [ ] Front-end en streamlit @ArianeDlns @Lucas-SOR
- [ ] Développement de Question Answering (NLP) sur les abstract par pays  @Lucas-SOR
- [ ] Score de similarité par drapeau @Lucas-SOR [Pas priori]

## References 