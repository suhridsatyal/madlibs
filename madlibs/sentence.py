import random

import wikipedia


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
    try:
        random_page_title = wikipedia.random(1)
        random_page = wikipedia.page(random_page_title)
    except wikipedia.exceptions.PageError:
        # page title from wikipedia.random does not always
        # return a valid page. Try again if this is the case.
        return extract_wikipedia_sentence(min_words, max_retries)
    sentences = random_page.content.split(".")
    result = []
    loop_count = 0
    while len(result) < min_words and loop_count < max_retries: 
        sentence = random.choice(sentences) 
        if "=" not in sentence:
            # Some content includes unsual markup with = characters,
            # giving out incoherent sentence. Skip those.
            result = sentence.split()
        loop_count += 1
    selected_sentence = " ".join(result)
    return selected_sentence
