from madlibs.referee import calculate_score
from tests.conftest import nlp_model

class TestCalculateScore:

    def test_should_return_0_imbalanced_input(self, nlp_model):
        assert calculate_score([], [], nlp_model) == 0

    def test_should_ignore_out_of_vocab_words_if_they_are_not_same(self, nlp_model):
        assert calculate_score(["xttx"], ["cat"], nlp_model) == 0

    def test_should_return_highest_score(self, nlp_model):
        assert calculate_score(["cat","dog"], ["cat","dog"], nlp_model) == 1
        assert calculate_score(["xxtt"], ["xxtt"], nlp_model) == 1


