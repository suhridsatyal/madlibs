import spacy
from madlibs.play import tokenize, mark_blanks 


def test_tokenize():
    nlp_model = spacy.load("en_core_web_sm")
    sentence = "The meaning of life, universe, and everything is 42"
    result = mark_blanks(*tokenize(sentence, nlp_model))
    for r in result:
        print(r.text, r.is_visible, r.part_of_speech)
