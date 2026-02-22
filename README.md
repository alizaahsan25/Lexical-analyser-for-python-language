# Lexical-analyser-for-python-language
A lexical analyzer for Python 3, written in Python. It reads a .py file and breaks source code into classified tokens including keywords, identifiers, operators, strings, and numbers.  

## Types of errors it detects:
It detects illegal characters, unmatched strings, and identifiers or numbers exceeding 255 characters, reporting the exact line and column of every token and error.  

## How to run this project:
Download all the files from this project and save them in a specific folder. Open that folder is VS Code. Open terminal in that folder and bash `python analyze.py` and then it will ask the file name that has the source code to be analyzed. Enter `test.py` and laxical analysis will create tokens of the source code written in test.py .

## What it does:
The analyzer reads any Python .py file and breaks every line of code into classified tokens. Each token gets a type, its exact value, and its line and column number.
#### Example:
Input (test.py)
```
name = "Aliza"
age = 25
if age >= 18:
    print("Adult")
```
#### Run:
python analyze.py  
Enter Python filename: test.py

#### Output:  
```
TYPE             VALUE                                       LINE   COL
----------------------------------------------------------------------
ID               'name'                                         1     1
OPERATOR         '='                                            1     6
STR              '"Aliza"'                                      1     8
ID               'age'                                          2     1
OPERATOR         '='                                            2     5
NUM:INT          '25'                                           2     7
KEYWORD          'if'                                           3     1
ID               'age'                                          3     4
OPERATOR         '>='                                           3     8
NUM:INT          '18'                                           3    11
DELIMITER        ':'                                            3    13
BUILTIN          'print'                                        4     5
DELIMITER        '('                                            4    10
STR              '"Adult"'                                      4    11
DELIMITER        ')'                                            4    18
----------------------------------------------------------------------

 TOKEN SUMMARY:
  DELIMITER         : 3
  ID                : 3
  OPERATOR          : 3
  STR               : 2
  NUM:INT           : 2
  KEYWORD           : 1
  BUILTIN           : 1
  TOTAL             : 15

 No lexical errors found.

(ENDMARKER)
```
