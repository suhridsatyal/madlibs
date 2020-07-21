import wikipedia
import random
import spacy
from dataclasses import dataclass
from collections import defaultdict
from typing import List, Any

MAX_FETCH_ATTEMPTS = 5
MIN_WORDS = 5
BLANK_TYPES = {'PROPN', 'VERB', 'NOUN', 'ADJ', 'ADV'}

@dataclass
class MadLibsToken:
    text: str
    part_of_speech: str
    is_visible: bool


def extract_wikipedia_sentence(
    min_words:int, 
    max_retries:int
):
    """
    Extracts a sentence from random wikipedia page.

    Parameters:
    -----------
    min_words
        Minimum number of words in a sentence

    max_retries
        Maximum number of retires to be made if sentence of min_words
        is not found
    """
    random_page = wikipedia.page("Special:Random")
    sentences = random_page.content.split(".")
    result = []
    loop_count = 0
    while len(result) < min_words and loop_count < max_retries: 
        result = random.choice(sentences).split()
        loop_count += 1
    selected_sentence = " ".join(result)
    return selected_sentence


def tokenize(
    sentence: str,
    nlp_model: Any
) -> MadLibsToken:
    """
    Creates mad libs tokens out of a sentence using spacy nlp model.

    Parameters
    ----------
    sentence
        Gramatically coherent plain text english sentence

    nlp_model
        Instance of a spacy nlp model
    """
    doc = nlp_model(sentence)
    pos_map = defaultdict(set)
    mad_libs_tokens = []
    for i, token in enumerate(doc):
        mad_libs_token = MadLibsToken(text=token.text, 
                                      part_of_speech=token.pos_,
                                      is_visible=True)
        mad_libs_tokens.append(mad_libs_token)
        pos_map[token.pos_].add(i)
    return mad_libs_tokens, pos_map

def mark_blanks(
    mad_libs_tokens, 
    pos_map
):
    min_blanks = 1
    max_blanks = max(min_blanks, len(mad_libs_tokens) // 4)
    invisible_count = random.randint(min_blanks, max_blanks)

    while invisible_count > 0 and len(pos_map) > 0:
        k = random.choice(list(pos_map.keys()))
        if k in BLANK_TYPES:
            chosen_val = random.choice(list(pos_map[k])) 
            mad_libs_tokens[chosen_val].is_visible = False
            invisible_count -= 1
            pos_map[k].remove(chosen_val)
            if len(pos_map[k]) == 0:
                del pos_map[k]
        else:
            del pos_map[k]
    return mad_libs_tokens