from prompt_toolkit.styles import Style

MAX_FETCH_ATTEMPTS = 5

MIN_WORDS = 5

BLANK_TYPES = {
    'PROPN': 'Noun',
    'VERB': 'Verb',
    'NOUN': 'Noun',
    'ADJ': 'Adjective',
    'ADV': 'Adverb'
}

STYLE = Style.from_dict({
    'hint': 'gray',
    'prompt': '#2aa198',
    'blank': '#ff0066',
    'answer': '#44ff00 italic',
    'actual': '#ff0066',
})
