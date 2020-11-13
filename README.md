# Graph-database

[![Build Status](https://travis-ci.org/artemlunev2000/Graph-database.svg?branch=task01)](https://travis-ci.org/artemlunev2000/Graph-database)

## Run localy in interactive mode

```
docker build -t graph-db .
docker run -it graph-db
pytest tests/test_*.py

```
## Assignment 2
Realisation of automata intersection and transitive closure

## Assignment 3
Experiment on algorithms of transitive closure and intersection of automata.

## Assignment 4
Realisation of cyk and Hellings algorithms in class Grammar.

## Assignment 5
Realisation of CFPQ based on matrix multiplication and tensor product added.

## Assignment 7
syntax description

#### Connecting database
```
connect PATH_TO_DB;
    
```

#### Selecting edjes
```
select edges from GRAPH;
    
```

#### Selecting edjes number
```
select count edges from GRAPH;
    
```

#### Graph reseive
```
graph(PATH_TO_GRAPH)

regex(REGEX)

intersect(GRAPH1, GRAPH2)
    
```

#### Regex possible operations
```
REGEX*, REGEX+, REGEX?, (REGEX1|REGEX2), REGEX1 REGEX2
    
```

examples in tests `/tests/test_task7.py`


