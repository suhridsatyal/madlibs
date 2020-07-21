import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Set, Tuple

import spacy

from madlibs.constants import BLANK_TYPES


@dataclass
class MadLibsToken:
    text: str
    part_of_speech: str
    is_visible: bool


def tokenize(
    sentence: str,
    nlp_model: Any
) -> Tuple[MadLibsToken, Dict[str, Set[int]]]:
    """
    Creates mad libs tokens out of a sentence using spacy nlp model.

    Parameters
    ----------
    sentence
        Gramatically coherent plain text english sentence

    nlp_model
        Instance of a spacy nlp model

    Returns
    -------
    Tuple
        List of MadLibsToken and Dictionary mapping of part-of-speech
        type and indices in the list of tokens
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
    mad_libs_tokens: List[MadLibsToken], 
    pos_map: Dict[str, Set[int]]
) -> List[MadLibsToken]:
    """
    Marks appropriate tokens as blank / invisible at random.
    Upto 25 percent of eligible words can be marked. Eligibility is
    decided in terms of part-of-speech tags defined in constants
    BLANK_TYPES.

    Parameters
    -----------
    mad_libs_tokens
        List of mad libs tokens

    pos_map
        Dictionary where key is the part-of-speech type and values
        are the indices in mad_libs_tokens that are tagged with the type. 
    
    Returns
    -------
    List[MadLibsToken]
        List of tokens with changed visibility
    """
    if len(mad_libs_tokens) == 0 or len(pos_map) == 0:
        return mad_libs_tokens

    # copy pos_map so that it can be mutated internally
    # items from copy of pos_map removed iteratively
    # to avoid double marking 
    pos_map = pos_map.copy()
    min_blanks = 1
    max_blanks = max(min_blanks, len(mad_libs_tokens) // 4)
    invisible_count = random.randint(min_blanks, max_blanks)

    # Track previous blanks so that succesive blank markings
    # can be avoided when found.
    prev_blanks = set()

    while invisible_count > 0 and len(pos_map) > 0:
        k = random.choice(list(pos_map.keys()))
        if k in BLANK_TYPES:
            chosen_val = random.choice(list(pos_map[k])) 
            if chosen_val - 1 not in prev_blanks:
                mad_libs_tokens[chosen_val].is_visible = False
                invisible_count -= 1
                prev_blanks.add(chosen_val)
            pos_map[k].remove(chosen_val)
            if len(pos_map[k]) == 0:
                del pos_map[k]
        else:
            del pos_map[k]
    return mad_libs_tokens
