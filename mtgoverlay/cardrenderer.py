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


class CardRenderer(object):
    def __init__(self, width, height):
        # Generate a legendary frame of the correct proportions.
        self.width = width
        self.height = height

        # Make slice width and height
        self.slice_width = 315
        self.slice_height = 25
        self.draw_x = 21
        self.draw_y = 48
        self.draw_y_mod = 0

        # Legendary frame is a certain width here.
        assert self.width == 355

        self.im = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        self.row_count = 0

    def get_pos(self) -> Tuple[int, int]:
        return self.draw_x, self.draw_y + self.draw_y_mod + self.row_count * self.slice_height

    def render_deck(self, deck: Deck) -> Image:
        # Render "Main Deck" on the image
        im = self.im.copy()

        # Make Main Deck
        im.paste(self.make_text_slice("Main Deck"), self.get_pos())
        self.row_count += 1

        # Draw the main deck out.
        for cards in deck.main_deck:
            pos = self.get_pos()
            cards.draw(im, self.slice_width, self.slice_height, pos[0], pos[1])
            self.row_count += 1

        # Blank line
        self.render_blank_slice(im)

        # Make Sideboard
        im.paste(self.make_text_slice("Sideboard"), self.get_pos())
        self.row_count += 1

        # Draw the sideboard out.
        for cards in deck.sideboard:
            pos = self.get_pos()
            cards.draw(im, self.slice_width, self.slice_height, pos[0], pos[1])
            self.row_count += 1

        # Blank line
        self.render_blank_slice(im)

        return im

    def make_text_slice(self, text: str):
        x = 4
        y = 3

        im = Image.new('RGBA', (self.slice_width, self.slice_height), (23, 19, 20, 255))
        font = art_repo.get_small_text_font(self.slice_height - (y * 2) - 2)
        draw = ImageDraw.Draw(im)
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        return im

    def render_blank_slice(self, parent_im):
        half_slice_height = self.slice_height // 2
        im = Image.new('RGBA', (self.slice_width, half_slice_height), (23, 19, 20, 255))
        parent_im.paste(im, self.get_pos())
        self.draw_y_mod += half_slice_height
