from prompt_toolkit.styles import Style

MAX_FETCH_ATTEMPTS = 5

MIN_WORDS = 5

BLANK_TYPES = {'PROPN', 'VERB', 'NOUN', 'ADJ', 'ADV'}

STYLE = Style.from_dict({
    'prompt': '#2aa198',
    'blank': '#ff0066',
    'answer': '#44ff00 italic',
    'actual': '#ff0066',
})
