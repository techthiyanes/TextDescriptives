"""Calculation of descriptive statistics."""
from typing import Callable, Union

import numpy as np
from spacy.language import Language
from spacy.tokens import Doc, Span

from .utils import filtered_tokens, n_sentences, n_syllables, n_tokens


@Language.factory("descriptive_stats")
def create_descriptive_stats_component(nlp: Language, name: str):
    """Allows DescriptiveStatistics to be added to a spaCy pipe using nlp.add_pipe("descriptive_stats").
    If the pipe does not contain a parser or sentencizer, the sentencizer component is silently added."""
    sentencizers = set(["sentencizer", "parser"])
    if not sentencizers.intersection(set(nlp.pipe_names)):
        nlp.add_pipe("sentencizer")  # add a sentencizer if not one in pipe
    return DescriptiveStatistics(nlp)


class DescriptiveStatistics:
    """spaCy v.3.0 component that adds attributes with desriptive statistics to `Doc` and `Span` objects.
    The attributes relate to token and sentence length, number of syllables, and counts of tokens and sentences.
    """

    def __init__(self, nlp: Language):
        """Initialise components"""

        extensions = [
            "_n_sentences",
            "_n_tokens",
            "_n_syllables",
            "token_length",
            "sentence_length",
            "syllables",
            "counts",
        ]
        ext_funs: list[Callable] = [
            n_sentences,
            n_tokens,
            n_syllables,
            self.token_length,
            self.sentence_length,
            self.syllables,
            self.counts,
        ]
        for ext, fun in zip(extensions, ext_funs):
            if ext not in [
                "_n_sentences",
                "sentence_length",
                "syllables",
            ] and not Span.has_extension(ext):
                Span.set_extension(ext, getter=fun)
            if not Doc.has_extension(ext):
                Doc.set_extension(ext, getter=fun)

        if not Doc.has_extension("_filtered_tokens"):
            Doc.set_extension("_filtered_tokens", default=[])
        if not Span.has_extension("_filtered_tokens"):
            Span.set_extension("_filtered_tokens", getter=filtered_tokens)

    def __call__(self, doc):
        """Run the pipeline component"""
        doc._._filtered_tokens = filtered_tokens(doc)
        return doc

    def token_length(self, doc: Union[Doc, Span]) -> dict:
        """Calculate mean, median and std of token length for a `Doc` or `Span`.

        Returns:
            dict with keys: token_length_mean, token_length_median, token_length_std
        """
        token_lengths = [len(token) for token in doc._._filtered_tokens]
        return {
            "token_length_mean": np.mean(token_lengths),
            "token_length_median": np.median(token_lengths),
            "token_length_std": np.std(token_lengths),
        }

    def sentence_length(self, doc: Doc) -> dict:
        """Calculate mean, median and std of sentence length for a `Doc`.

        Returns:
            dict with keys: sentence_length_mean, sentence_length_median, sentence_length_std"""
        # get length of filtered tokens per sentence
        tokenized_sentences = [
            [
                token.text
                for token in sent
                if not token.is_punct and "'" not in token.text
            ]
            for sent in doc.sents
        ]
        len_sentences = [len(sentence) for sentence in tokenized_sentences]
        return {
            "sentence_length_mean": np.mean(len_sentences),
            "sentence_length_median": np.median(len_sentences),
            "sentence_length_std": np.std(len_sentences),
        }

    def syllables(self, doc: Doc) -> dict:
        """Calculate mean, median and std of syllables per token for a `Doc`.
        Uses `Pyphen` for hyphenation.

        Returns:
            dict with keys: syllables_per_token_mean, syllables_per_token_median, syllables_per_token_std"""
        n_syllables = doc._._n_syllables
        return {
            "syllables_per_token_mean": np.mean(n_syllables),
            "syllables_per_token_median": np.median(n_syllables),
            "syllables_per_token_std": np.std(n_syllables),
        }

    def counts(self, doc: Union[Doc, Span], ignore_whitespace: bool = True) -> dict:
        """Calculate counts of tokens, unique tokens, and characters for a `Doc` or `Span`.
        Adds number of sentences for `Doc` objects.

        Args:
            ignore_whitespace: if True, whitespace is not counted as a character when
                counting number of characters.
        Returns:
            dict with keys: n_tokens, n_unique_tokens, proportion_unique_tokens, n_characters, (n_sentences)
        """
        n_tokens = doc._._n_tokens
        n_types = len(set([tok.lower_ for tok in doc._._filtered_tokens]))
        if ignore_whitespace:
            n_chars = len(doc.text.replace(" ", ""))
        else:
            n_chars = len(doc.text)

        if n_tokens == 0:
            prop_unique_tokens = np.nan
        else:
            prop_unique_tokens = n_types / n_tokens
        out = {
            "n_tokens": n_tokens,
            "n_unique_tokens": n_types,
            "proportion_unique_tokens": prop_unique_tokens,
            "n_characters": n_chars,
        }
        if isinstance(doc, Doc):
            out["n_sentences"] = doc._._n_sentences
        return out
