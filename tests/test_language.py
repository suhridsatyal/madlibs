import pytest
import spacy
from madlibs.play import tokenize, mark_blanks 


@pytest.fixture()
def nlp_model():
    yield spacy.load("en_core_web_sm")


class TestTokenize:

    def test_should_return_5_visible_tokens(self, nlp_model):
        tokens, pos_map = tokenize("This is a small sentence", nlp_model)
        assert len(tokens) == 5
        assert len(pos_map) > 0
        for t in tokens:
            assert t.is_visible == True

    def test_should_return_empty_list_and_pos_map(self, nlp_model):
        tokens, pos_map = tokenize("", nlp_model)
        assert len(tokens) == 0
        assert len(pos_map) == 0

    def test_should_return_correct_pos_map(self, nlp_model):
        _, pos_map = tokenize("very good", nlp_model)
        assert pos_map == {"ADV": {0}, "ADJ": {1}}


class TestMarkBlanks:

    def test_should_mark_some_blanks_at_random(self, nlp_model):
        tokens, pos_map = tokenize("This is a small sentence", nlp_model)
        # All visible at first
        visibilities = [m.is_visible for m in tokens]
        assert all(visibilities)
        marked_tokens = mark_blanks(tokens, pos_map)
        # Some should be marked as False now
        visibilities = [m.is_visible for m in marked_tokens]
        assert not all(visibilities)

    def test_should_return_empty_list(self):
        marked_tokens = mark_blanks([], {})
        assert marked_tokens == []
        marked_tokens = mark_blanks([], {'NOUN': 1})
        assert marked_tokens == []

    def test_should_not_mark_blank_on_missing_pos(self, nlp_model):
        tokens, _ = tokenize("This is a small sentence", nlp_model)
        marked_tokens = mark_blanks(tokens, {})
        visibilities = [m.is_visible for m in marked_tokens]
        assert all(visibilities)
        