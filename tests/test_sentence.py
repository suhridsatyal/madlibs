from madlibs.sentence import extract_wikipedia_sentence


class TestExtractWikipediaSentence:

    def test_should_extract_a_sentence(self):
        sentence = extract_wikipedia_sentence(min_words=5, max_retries=3)
        assert len(sentence) > 5
