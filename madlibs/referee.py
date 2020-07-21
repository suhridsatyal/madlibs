from typing import List, Any 

def calculate_score(
    guesses: List[str], 
    answers: List[str],
    nlp_model: Any
) -> float:
    """
    Calculates mean semantic similarity between
    guesses and answers using Spacy word embeddings.
    High similarity indicates better performance.

    Parameters
    ----------
    guesses
        Player's guesses of blanked words
    
    answers
        Actual value of blanked words
    
    nlp_model
        Spacy NLP model with word embeddings (medium or large)

    Returns
    -------
    float
        Mean semantic similarity score
    """
    if len(guesses) != len(answers):
        return 0
    if len(guesses) == 0:
        return 0
    if guesses == answers:
        return 1
    cumulative_score = 0
    for guess, answer in zip(guesses, answers):
        guess_doc = nlp_model(guess)
        answer_doc = nlp_model(answer)
        is_out_of_vocab = [x.is_oov for x in guess_doc] + [x.is_oov for x in answer_doc]
        if True in is_out_of_vocab:
            continue
        cumulative_score += guess_doc.similarity(answer_doc)
    return round(cumulative_score / len(answers), 2)
