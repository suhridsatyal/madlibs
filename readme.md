## Madlibs

Mad Libs like game [[1](https://en.wikipedia.org/wiki/Mad_Libs)] in python with wikipedia sentences and spacy NLP.

A sentence is fetched from a random wikipedia page. Some keywords are
replaced with blanks at random. Keywords are chosen based on Part-of-Speech tags
from spacy model.

The player is asked to guess the keywords. At any turn, only the part of sentence upto
the current blank is shown. 

Player's answer is compared with the actual sentence at the end of the game.



### Installation 
```
# Pre-requisite: python 3.7 
cd madlibs/
pip install -r requirements.py
python -m spacy download en_core_web_sm
```

### Usage

```
python -m madlibs.play
```

### Future Plans

- Player vs prediction model (e.g. GPT-3)
- Referee system to automatically decide whether player or the model won
- Model vs Model games
- Genre specific sentences and expansion of data source beyond wikipedia
- Better hints (entity type instead of part-of-speech)

### Links
[1] https://en.wikipedia.org/wiki/Mad_Libs