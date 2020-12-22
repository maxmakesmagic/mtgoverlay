#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Docstring"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
from .deck import Deck
import mtgoverlay
from PIL import Image, ImageDraw
from typing import Tuple, Dict

log = logging.getLogger(__name__)
art_repo = mtgoverlay.ArtRepo()


class CommanderDecklistRenderer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.im = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))

        # Choose appropriate card widths
        self.card_width = 150
        self.cmdr_width = 500

        # Make start draw position
        base_x = 627
        base_y = 188

        self.card_count = 0

        self.positions = {}  # type: Dict[int, Tuple[int, int]]

        count = 0

        # 3 Rows
        for row in range(0, 4):
            # 8 columns
            for column in range(0, 8):
                # 4 cards in each column
                for colcard in range(0, 4):
                    # We should be able to definitively place a card.

                    # Add the column into the X calculation.
                    pos_x = base_x + (column * (self.card_width + 10))

                    # For the Y calculation:
                    # The column card adds on enough to see the card name
                    # The row adds on 300 px
                    pos_y = int(base_y + (colcard * 25) + (row * 300))

                    self.positions[count] = (pos_x, pos_y)
                    log.debug("Position %d: %s", count, self.positions[count])
                    count += 1

        # Commander
        self.positions[99] = (58, 289)

    def get_pos(self) -> Tuple[int, int]:
        return self.positions[self.card_count]

    def advance_pos(self):
        self.card_count += 1

    def render_deck(self, deck: Deck) -> Image:
        # Render "Main Deck" on the image
        im = self.im.copy()

        # Draw the main deck out.
        for cards in deck.main_deck:
            card_im = art_repo.get_full_card_image(cards.card.id)

            # Resize the card image.
            card_w, card_h = card_im.size

            new_card_h = int(self.card_width * card_h / card_w)
            small_card = card_im.resize((self.card_width, new_card_h), Image.LANCZOS)

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

            new_card_h = int(self.cmdr_width * card_h / card_w)
            small_card = card_im.resize((self.cmdr_width, new_card_h), Image.LANCZOS)

            for i in range(cards.quantity):
                pos = self.get_pos()
                log.debug("Pasting card %d: %s at %s", self.card_count, cards.card, pos)
                im.paste(small_card, pos, small_card)
                self.advance_pos()

        return im
