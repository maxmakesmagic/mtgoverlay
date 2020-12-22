#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Docstring"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
import os
import xml.etree.ElementTree as ET
from typing import List
from mtgoverlay.cards import Cards

log = logging.getLogger(__name__)


class Deck(object):
    def __init__(self, name: str, main_deck: List['Cards'], sideboard: List['Cards']):
        self.name = name
        self.main_deck = main_deck
        self.sideboard = sideboard

    def __repr__(self):
        return "{self.__class__.__name__}({self.name!r}, {self.main_deck!r}, {self.sideboard!r})".format(self=self)

    @classmethod
    def from_dek_file(cls, filename: str) -> 'Deck':
        tree = ET.parse(filename)
        xml_deck = tree.getroot()

        all_cards = [Cards(element) for element in xml_deck.findall("Cards")]
        main_deck = sorted([cards for cards in all_cards if not cards.sideboard])
        sideboard = sorted([cards for cards in all_cards if cards.sideboard])

        main_deck = munge_cards(main_deck)
        sideboard = munge_cards(sideboard)

        # Make the deck name
        basename = os.path.basename(filename)
        basenoext = os.path.splitext(basename)[0]

        return cls(basenoext, main_deck, sideboard)


def munge_cards(cardses: List[Cards]) -> List[Cards]:
    new_cardses = []

    while len(cardses) > 0:
        cards = cardses.pop(0)

        while len(cardses) > 0 and cards.card.name == cardses[0].card.name:
            temp_cards = cardses.pop(0)
            cards.quantity += temp_cards.quantity

        new_cardses.append(cards)

    return new_cardses
