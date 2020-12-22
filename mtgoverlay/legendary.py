#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Docstring"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
from .deck import Deck
from PIL import Image, ImageDraw
import mtgoverlay

log = logging.getLogger(__name__)
art_repo = mtgoverlay.ArtRepo()


class LegendaryFrame(object):
    def __init__(self, width, height):
        # Generate a legendary frame of the correct proportions.
        self.width = width
        self.height = height

        # Legendary frame is a certain width here.
        assert self.width == 355

        im = Image.new('RGBA', (self.width, self.height), (23, 19, 20, 255))

        # Draw sides
        log.debug("Loading sides")
        card_sides = art_repo.get_resource_image("cardsides.png")
        card_sides = card_sides.resize((self.width, self.height))
        im = Image.alpha_composite(im, card_sides)

        # Hide the top portion of the lines.
        hide_top = Image.new('RGBA', (self.width, 30), (23, 19, 20, 255))
        im.paste(hide_top)

        # Draw the frame on top.
        log.debug("Loading legendary top")
        card_top = art_repo.get_resource_image("cardtop.png")
        im.paste(card_top, mask=card_top)

        self.im = im

    def render_deck(self, deck: Deck) -> Image:
        # Render the deck name on top of the frame.
        im = self.im.copy()
        font = art_repo.get_resource_font("belerenbold.ttf", 20)
        draw = ImageDraw.Draw(im)

        # now draw the text over it
        draw.text((19, 20), deck.name, font=font, fill=(0, 0, 0, 255))
        return im
