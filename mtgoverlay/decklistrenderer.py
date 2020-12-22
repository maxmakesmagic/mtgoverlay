#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Docstring"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
from .deck import Deck
import mtgoverlay
from PIL import Image, ImageDraw
from typing import Tuple

log = logging.getLogger(__name__)
art_repo = mtgoverlay.ArtRepo()


class DecklistRenderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.im = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))

        # Make start draw position
        self.draw_x = 50
        self.base_y = 226
        self.draw_y = self.base_y
        self.card_count = 0

    def get_pos(self) -> Tuple[int, int]:
        return self.draw_x, self.draw_y

    def advance_pos(self):
        self.card_count += 1

        if 0 <= self.card_count < 12:
            self.draw_x = 50
        elif 12 <= self.card_count < 24:
            self.draw_x = 340
        elif 24 <= self.card_count < 36:
            self.draw_x = 630
        elif 36 <= self.card_count < 48:
            self.draw_x = 920
        elif 48 <= self.card_count < 60:
            self.draw_x = 1210
        elif 60 <= self.card_count < 75:
            self.draw_x = 1595

        if 0 <= self.card_count < 60:
            self.draw_y = self.base_y + (42 * (self.card_count % 12))
        else:
            self.draw_y = self.base_y + (42 * (self.card_count - 60)) - 126

    def render_deck(self, deck: Deck) -> Image:
        # Render "Main Deck" on the image
        im = self.im.copy()

        # Draw the main deck out.
        for cards in deck.main_deck:
            card_im = art_repo.get_full_card_image(cards.card.id)

            # Resize the card image.
            card_w, card_h = card_im.size

            # Target width is 275
            new_card_h = int(275 * card_h / card_w)
            small_card = card_im.resize((275, new_card_h), Image.LANCZOS)

            for i in range(cards.quantity):
                pos = self.get_pos()
                log.debug("Pasting card %d: %s at %s", self.card_count, cards.card, pos)
                im.paste(small_card, pos, small_card)
                self.advance_pos()

        # Draw the sideboard out.
        for cards in deck.sideboard:
            card_im = art_repo.get_full_card_image(cards.card.id)

            # Resize the card image.
            card_w, card_h = card_im.size

            # Target width is 275
            new_card_h = int(275 * card_h / card_w)
            small_card = card_im.resize((275, new_card_h), Image.LANCZOS)

            for i in range(cards.quantity):
                pos = self.get_pos()
                log.debug("Pasting card %d: %s at %s", self.card_count, cards.card, pos)
                im.paste(small_card, pos, small_card)
                self.advance_pos()

        return im
