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

#### Selecting edjes or number with filter
```
select filter (v, e, u) (BOOL_EXP) edges from GRAPH;
    
```

#### BOOL_EXP
```
STRING has STRING
is_start STRING
is_final STRING
(BOOL_EXP and BOOL_EXP)
(BOOL_EXP or BOOL_EXP)
not BOOL_EXP
    
```

#### Graph reseive
```
graph(PATH_TO_GRAPH)

regex(REGEX)

intersect(GRAPH1, GRAPH2)

graph_with_start_final(VERTICES, VERTICES, GRAPH)
    
```

#### VERTICES
```
set (1, 2, ... )
range (1, 10)
none
    
```

#### Regex possible operations
```
term(name)
nonterm(name)
REGEX*, REGEX+, REGEX?, (REGEX1 or REGEX2), (REGEX1 . REGEX2 . REGEX3)
    
```

examples in tests `/tests/test_task7.py`


