import random
from collections import defaultdict
from typing import List

import spacy
from prompt_toolkit import HTML, print_formatted_text, prompt

from madlibs.constants import MAX_FETCH_ATTEMPTS, MIN_WORDS, STYLE
from madlibs.language import MadLibsToken, mark_blanks, tokenize
from madlibs.sentence import extract_wikipedia_sentence


def tokens_to_string(
    tokens: List[MadLibsToken]
) -> List[str]:
    """
    Converts madlibs token into a list of string such with invisible
    tokens marked as blanks ( _ character).
    """
    s = []
    for t in tokens:
        if t.is_visible:
            s.append(t.text)
        else:
            blank = '_' * len(t.text)
            s.append(f'<blank>{blank}</blank>')
    return s


def get_first_blank_index(
    tokens: List[MadLibsToken]
) -> int:
    """
    Returns the index of first token in list that is blank or invisible.
    """
    for i, t in enumerate(tokens):
        if t.is_visible == False:
            return i


def main():
    """
    Runs MadLibs game on the terminal.
    """
    nlp_model = spacy.load("en_core_web_sm")

    print_formatted_text(HTML(
        "<prompt> Creating a madlib sentence ... </prompt>"), 
        style=STYLE)

    # Prepare madlib sentence
    sentence = extract_wikipedia_sentence(MIN_WORDS, MAX_FETCH_ATTEMPTS)
    madlib_tokens = mark_blanks(*tokenize(sentence, nlp_model))
    blank_indices = [i for i, t in enumerate(madlib_tokens) if not t.is_visible] 

    s = tokens_to_string(madlib_tokens) 
    actual = s.copy()

    mark = get_first_blank_index(madlib_tokens)

    print_formatted_text(HTML(" ".join(s[:mark+1])), style=STYLE)

    for i, blank_index in enumerate(blank_indices):
        # Take input for each blank and display the result
        text = prompt(HTML(
            "<prompt> Enter blank word: </prompt>"), 
            style=STYLE)

        madlib_tokens[blank_index].is_visible = True
        s[blank_index] = f'<answer>{text}</answer>'
        actual[blank_index] = f'<actual>{madlib_tokens[blank_index].text}</actual>'

        if i < len(blank_indices) - 1:
            # Don't print after all blanks have been filled
            print()
            mark = get_first_blank_index(madlib_tokens)
            print_formatted_text(HTML(" ".join(s[:mark + 1])), style=STYLE)
            print()

    # Display result
    print()
    print_formatted_text(HTML("<prompt> You said: </prompt>"), style=STYLE)
    print_formatted_text(HTML(" ".join(s)), style=STYLE)
    print()
    print_formatted_text(HTML("<prompt> Actual sentence: </prompt>"), style=STYLE)
    print_formatted_text(HTML(" ".join(actual)), style=STYLE)


if __name__ == '__main__':
    main()
