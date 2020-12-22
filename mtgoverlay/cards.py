#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Docstring"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
import xml.etree.ElementTree as ET
from functools import total_ordering
import mtgoverlay
from PIL import Image, ImageDraw


log = logging.getLogger(__name__)
scryfaller = mtgoverlay.scryfall.Scryfaller()
art_repo = mtgoverlay.ArtRepo()


@total_ordering
class Cards(object):
    def __init__(self, cards: ET.Element):
        assert(cards.tag == "Cards")
        self.quantity = int(cards.attrib["Quantity"])
        self.sideboard = (cards.attrib["Sideboard"].lower() == 'true')
        self.card = Card(cards)

    def __repr__(self):
        return "<{self.quantity} * {self.card}>".format(self=self)

    def __eq__(self, other):
        return self.card == other.card

    def __lt__(self, other):
        return self.card < other.card

    def draw(self, im: Image, width: int, height: int, draw_x: int, draw_y: int):
        # Draw the slice.
        self.card.draw(im, width, height, draw_x, draw_y, self.quantity)


@total_ordering
class Card(object):
    def __init__(self, cards: ET.Element):
        self.name = cards.attrib["Name"]

        try:
            self.mtgo_id = int(cards.attrib["CatID"])
            self.json = scryfaller.get_card_by_mtgo_id(self.mtgo_id)
        except Exception:
            # Failed to get card by MTGO ID. Try and get by name.
            log.debug("Failed to get card by MTGO ID; try name: %s", self.name)
            self.mtgo_id = None
            self.json = scryfaller.get_card_by_name(self.name)

        log.debug("Got json %s for mtgo id %s", self.json, self.mtgo_id)

        # Store off useful values.
        self.cmc = self.json["cmc"]  # type: float

        try:
            self.mana_cost = self.json["mana_cost"]  # type: str
        except KeyError:
            self.mana_cost = 3

        self.is_land = ("Land" in self.json["type_line"])  # type: bool
        self.id = self.json["id"]  # type: str

        log.debug("[%s] CMC %f, Mana Cost %s", self, self.cmc, self.mana_cost)

        # Ensure the card has a matching art strip
        # self.art_strip = CardSlice(self.json["id"])
        self.image_slice = art_repo.get_slice_obj(self.id)

    def __str__(self):
        return "{self.name}({self.mtgo_id})".format(self=self)

    def __eq__(self, other):
        return (self.mtgo_id == other.mtgo_id and
                self.name == other.name)

    def __lt__(self, other):
        # Ensure there's a numeric ID to compare against.
        self_mtgo_id = 9999999999 if self.mtgo_id is None else self.mtgo_id
        other_mtgo_id = 9999999999 if other.mtgo_id is None else other.mtgo_id

        try:
            res = (self.is_land, self.cmc, self.name, self_mtgo_id) < (other.is_land, other.cmc, other.name, other_mtgo_id)
        except TypeError:
            log.debug("%s < %s",
                      (self.is_land, self.cmc, self.name, self_mtgo_id),
                      (other.is_land, other.cmc, other.name, other_mtgo_id))
            log.exception("Error while comparing %s and %s", self, other)
            raise

        return res

    def draw(self, im: Image, width: int, height: int, draw_x: int, draw_y: int, quantity: int):
        text = "{quantity} {self.name}".format(quantity=quantity, self=self)
        self.image_slice.draw(im, width, height, draw_x, draw_y, text)
