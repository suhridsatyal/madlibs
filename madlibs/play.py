import random
from collections import defaultdict
from typing import List, Optional, Any

import spacy
from prompt_toolkit import HTML, print_formatted_text, prompt

from madlibs.constants import BLANK_TYPES, MAX_FETCH_ATTEMPTS, MIN_WORDS, STYLE
from madlibs.language import MadLibsToken, mark_blanks, tokenize
from madlibs.sentence import extract_wikipedia_sentence
from madlibs.referee import calculate_score


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


def prepare_question(
    words: List[str],
    madlib_tokens: List[MadLibsToken]
):
    """
    Returns a list of words upto the blank, the blank, and
    a hint based on the part of speech.
    """
    mark = get_first_blank_index(madlib_tokens)
    words_till_blank = words[:mark + 1]
    hint = "<hint>" + BLANK_TYPES.get(madlib_tokens[mark].part_of_speech, "") + "</hint>"
    return " ".join(words_till_blank + [hint])


class Game:
    def __init__(
        self,
        opponent: Optional[Any] = None,
        is_collaborative: bool = False,
        is_multiple_rounds: bool = False
    ):
        self.opponent = opponent
        self.is_collaborative = is_collaborative
        self.is_multiple_rounds = is_multiple_rounds
        self.nlp_model = spacy.load("en_core_web_md")

    def play(self):
        """
        Runs MadLibs game on the terminal.
        """
        if self.is_multiple_rounds:
            in_session = True
            while in_session:
                self._play_single()
                answer = prompt("Keep playing? (Y/N)")
                in_session = False if answer.lower() == "n" else True
        else:
            self._play_single()

    def _play_single(self):
        """
        Helper method for a single game.
        """
        guesses, answers = [], []
        print_formatted_text(HTML(
            "<prompt> Creating a madlib sentence ... </prompt>"), 
            style=STYLE)

        # Prepare madlib sentence
        sentence = extract_wikipedia_sentence(MIN_WORDS, MAX_FETCH_ATTEMPTS)
        madlib_tokens = mark_blanks(*tokenize(sentence, self.nlp_model))
        blank_indices = [i for i, t in enumerate(madlib_tokens) if not t.is_visible] 
        s = tokens_to_string(madlib_tokens) 
        actual = s.copy()

        question = prepare_question(s, madlib_tokens)
        print_formatted_text(HTML(question), style=STYLE)

        for i, blank_index in enumerate(blank_indices):
            # Take input for each blank and display the result
            text = prompt(HTML(
                "<prompt> Enter blank word: </prompt>"), 
                style=STYLE)

            madlib_tokens[blank_index].is_visible = True
            s[blank_index] = f'<answer>{text}</answer>'
            actual[blank_index] = f'<actual>{madlib_tokens[blank_index].text}</actual>'

            guesses.append(text)
            answers.append(madlib_tokens[blank_index].text)

            if i < len(blank_indices) - 1:
                # Don't print question after all blanks have been filled
                print()
                question = prepare_question(s, madlib_tokens)
                # mark = get_first_blank_index(madlib_tokens)
                print_formatted_text(HTML(question), style=STYLE)
                print()

        # Display result
        print()
        print_formatted_text(HTML("<prompt> You said: </prompt>"), style=STYLE)
        print_formatted_text(HTML(" ".join(s)), style=STYLE)
        print()
        print_formatted_text(HTML("<prompt> Actual sentence: </prompt>"), style=STYLE)
        print_formatted_text(HTML(" ".join(actual)), style=STYLE)
        print()
        score = calculate_score(guesses, answers, self.nlp_model) 
        print_formatted_text(HTML(f"<prompt> Score: {score} </prompt>"), style=STYLE)


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
