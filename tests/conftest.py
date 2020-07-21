import spacy
import pytest


@pytest.fixture(scope="session")
def nlp_model():
    yield spacy.load("en_core_web_md")
