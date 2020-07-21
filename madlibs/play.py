import wikipedia
import random
import spacy
from dataclasses import dataclass
from collections import defaultdict
from typing import List, Any
from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text, HTML 
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'prompt': 'blue',
    'blank': '#ff0066',
    'answer': '#44ff00 italic',
    'actual': 'purple',
})

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
    random_page_title = wikipedia.random(1)
    random_page = wikipedia.page(random_page_title)
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

def tokens_to_string(
    tokens: List[MadLibsToken]
):
    s = []
    for t in tokens:
        if t.is_visible:
            s.append(t.text)
        else:
            blank = '_' * len(t.text)
            s.append(f'<blank>{blank}</blank>')
    return s

def get_first_blank_index(tokens):
    for i, t in enumerate(tokens):
        if t.is_visible == False:
            return i

def main():
    nlp_model = spacy.load("en_core_web_sm")

    print_formatted_text(HTML(
        "<prompt> Creating a madlib sentence ... </prompt>"), 
        style=style)
    sentence = extract_wikipedia_sentence(MIN_WORDS, MAX_FETCH_ATTEMPTS)
    madlib_tokens = mark_blanks(*tokenize(sentence, nlp_model))
    blank_indices = [i for i, t in enumerate(madlib_tokens) if not t.is_visible] 

    s = tokens_to_string(madlib_tokens) 
    actual = s.copy()

    mark = get_first_blank_index(madlib_tokens)

    print_formatted_text(HTML(" ".join(s[:mark+1])), style=style)

    for i, blank_index in enumerate(blank_indices):
        text = prompt(HTML(
            "<prompt> Enter blank word: </prompt>"), 
            style=style)

        madlib_tokens[blank_index].is_visible = True
        s[blank_index] = f'<answer>{text}</answer>'
        actual[blank_index] = f'<actual>{madlib_tokens[blank_index].text}</actual>'

        if i < len(blank_indices) - 1:
            print()
            mark = get_first_blank_index(madlib_tokens)
            print_formatted_text(HTML(" ".join(s[:mark + 1])), style=style)
            print()
    print()
    print_formatted_text(HTML("<prompt> You said: </prompt>"), style=style)
    print_formatted_text(HTML(" ".join(s)), style=style)
    print()
    print_formatted_text(HTML("<prompt> Actual sentence: </prompt>"), style=style)
    print_formatted_text(HTML(" ".join(actual)), style=style)


if __name__ == '__main__':
    main()