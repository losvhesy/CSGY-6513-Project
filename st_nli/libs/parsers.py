#!/usr/bin/env python

"""parsers.py: parsers used for generating task specs"""

__author__ = "Guande Wu"
__copyright__ = "Copyright 2021, Group8, CSGY-6513 Big Data"
import datefinder
import dateparser
import spacy
from .utils import build_ngrams, get_token_text, reconstruct_text, tokenize_sent
from .filters import TemporalFilter, SpatialFilter, AttrFilter
from .spec import  Spec


class AttrParser:
    def __init__(self, attr_configs):
        self.attrs = attr_configs

    def search_attr(self, text):
        n_grams = build_ngrams(text)
        for n_gram in n_grams:
            for attr in self.attrs:
                if n_gram.lower() in attr['synonyms']:
                    return {
                        "attr": attr['name']
                    }

    def parse(self, node):
        attrs = []

        token_text = get_token_text(node)
        if node.pos_ == "NOUN":
            attr = self.search_attr(token_text)
            if attr != None:
                attrs.append(attr)
        for sub in node.children:
            if sub.dep_ == "conj":
                attr = self.search_attr(sub.orth_)
                if attr != None:
                    attrs.append(attr)
            if sub.dep_ == "nmod":
                pass
        return attrs


class TemporalParser:
    def __init__(self):
        pass
    def check_ent(self, token):
        text = reconstruct_text(token)
        sub_tokens = tokenize_sent(text)
        matches = datefinder.find_dates(text)
        if len(list(matches)) > 0:
           return "TIME"
        else:
           return None
    def _parse(self, node):
        parsed_date = dateparser.parse(node.orth_)
        return {
            "type": "temporal",
            "op": "on",
            "date": parsed_date
        }
    def parse(self, token):
        parsed = self._parse(token)
        filter_instance = TemporalFilter([parsed])
        return filter_instance


class SpatialParser:
    def __init__(self, spatial_commonsense):
        self.spatial_commonsense = spatial_commonsense
        self.spatial_terms_lower = []
        self.spatial_terms = {}
        self.initialize(spatial_commonsense)

    def initialize(self, spatial_commonsense):
        for division in spatial_commonsense["divisions"]:
            self.spatial_terms[division['name'].lower()] = division
        self.spatial_terms_lower = list(map(lambda t: t.lower(), list(self.spatial_terms.keys())))

    def search_spatial_terms(self, text):
        n_grams = build_ngrams(text)
        searched = []
        for n_gram in n_grams:
            if n_gram.lower() in self.spatial_terms_lower:
                searched.append(n_gram.lower())
        return searched

    def check_ent(self, token):
        text = reconstruct_text(token)
        sub_tokens = tokenize_sent(text)
        searched = []
        for sub in sub_tokens:
            _ = self.search_spatial_terms(sub)
            searched.extend(_)
        if len(searched) > 0:
            return "LOC"
        else:
            return None
    
    def parse_region(self, region):
        return self.spatial_terms[region.lower()]['states']
    def _parse(self, node):
        text = reconstruct_text(node)
        if node.pos_ == "NOUN" and node.n_lefts == 0:
            searched = self.search_spatial_terms(node.orth_)
            return {
                "op": "in",
                "regions": searched
            }
        else:
            text = reconstruct_text(node)
            searched = self.search_spatial_terms(text)
            return {
                "type": "spatial",
                "op": "in",
                "regions": searched
            }

    def parse(self, token):
        parsed = self._parse(token)
        referred_states = []
        for region in parsed['regions']:
            states = self.parse_region(region)
            referred_states.extend(states)
        return SpatialFilter(referred_states)


class Parser:
    def __init__(self, attr_configs, spatial_commonsense):
        self.spatial_parser = SpatialParser(spatial_commonsense)
        self.temporal_parser = TemporalParser()
        self.attr_parser = AttrParser(attr_configs)
        self.spatial_words = [
            "areas", "area", "region", "regions", "places", "America", "US", "U.S.", "United States"
        ]
        self.temporal_words = [
            "year", "time", "January", "February", "March", "April"
        ]
        self.nlp = spacy.load("en_core_web_sm")

    def infer_ent(self, token):
        ent = self.infer_ent_by_token(token)
        if ent == None:
            ent = self.infer_ent_by_word(token)

        if ent == None:
            ent = self.infer_ent_by_parser(token)

        return ent

    def infer_ent_by_token(self, token):
        if token.ent_type_ == "LOC":
            return "LOC"
        elif token.ent_type_ == "NUM":
            return "TIME"
        else:
            return None

    def infer_ent_by_word(self, token):
        if token.orth_ in self.spatial_words:
            return "LOC"
        elif token.orth_ in self.temporal_words:
            return "TIME"

    def infer_ent_by_parser(self, token):
        text = reconstruct_text(token)
        matches = datefinder.find_dates(text)

        spatial = self.spatial_parser.check_ent(token)
        temporal = self.temporal_parser.check_ent(token)
        if spatial != None:
            return spatial
        elif temporal != None:
            return temporal
        else:
            return None

    def parse_prep(self, token):
        filters = []
        for child in token.children:
            if child.dep_ == "pobj":
                ent = self.infer_ent(child)
                if ent == "LOC":
                    filter_instance = self.spatial_parser.parse(child)
                    filters.append(filter_instance)
                elif ent == "TIME":
                    filter_instance = self.temporal_parser.parse(child)
                    filters.append(filter_instance)
        return {
            "filters": filters
        }

    def parse(self, token):
        if token.dep_ == "prep":
            return self.parse_prep(token)
        self.infer_ent(token)
        temporal_conds = temporal_parser.parse(token)
        return temporal_conds

    def parse_sent(self, sent):
        doc = self.nlp(sent)

        trees = [sent for sent in doc.sents]
        tree = trees[-1]

        spec = Spec([])
#         print("created: ", spec.filters)
        for node in tree.root.children:
            if node.dep_ == "dobj":
                attrs = self.attr_parser.parse(node)
                spec.extend_selectors(attrs)
            elif node.dep_ == "prep":
                prep = node
                parsed = self.parse(prep)
#                 print('node before', spec.filters)
                spec.integrate_obj_spec(parsed)
#                 print('node after', spec.filters)
            #         for prep_sub in prep.children:
            #             if prep_sub.dep_ == "pobj":
            #                 temporal_conds = parser.parse(prep_sub)
            #                 spatial_regions = spatial_parser.parse(prep_sub)

            for sub in node.children:
                if sub.dep_ == "prep":
                    prep = sub
#                     print('sub before', spec.filters)
                    parsed = self.parse(prep)
                    
                    spec.integrate_obj_spec(parsed)
#                     print('sub after::::', spec.filters)
        return spec
