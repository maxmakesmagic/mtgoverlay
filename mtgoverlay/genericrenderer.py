#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generic deck renderer"""

import logging
from .deck import Deck
from collections import namedtuple
import mtgoverlay
from PIL import Image, ImageDraw
from typing import Tuple, List

log = logging.getLogger(__name__)
art_repo = mtgoverlay.ArtRepo()


# Only require width as height is calculated from width.
PositionDimension = namedtuple('PositionDimension', ['x', 'y', 'w'])


class GenericRendererIterator:
    def __init__(self, gr):
        self.n = 0
        self.gr = gr

    def __next__(self) -> PositionDimension:
        try:
            pos = self.gr.positions[self.n]
            self.n += 1
            return pos
        except IndexError:
            raise StopIteration


class GenericRenderer:
    CANVAS_WIDTH = 1920
    CANVAS_HEIGHT = 1080

    def __init__(self, width, height, positions: List[PositionDimension]):
        self.width = width
        self.height = height
        self.im = Image.new('RGBA', (self.CANVAS_WIDTH, self.CANVAS_HEIGHT), (0, 0, 0, 0))

        # Store the list of positions.
        self.positions = positions

    def __iter__(self):
        return GenericRendererIterator(self)

    def __str__(self):
        return ("{self.__class__.__name__}(width={self.width}, height={self.height}, positions={self.positions})"
                .format(self=self))

    def render_deck(self, deck: Deck) -> Image:
        im = self.im.copy()
        posdims = enumerate(self)

        for zone in [deck.main_deck, deck.sideboard]:
            for cards in zone:
                card_im = art_repo.get_full_card_image(cards.card.id)

                for i in range(cards.quantity):
                    (idx, posdim) = next(posdims)

                    # Resize the card image.
                    card_w, card_h = card_im.size

                    # Calculate the target height and resize the card.
                    new_card_h = int(posdim.w * card_h / card_w)
                    small_card = card_im.resize((posdim.w, new_card_h), Image.LANCZOS)

                    log.debug("Pasting card %d: %s at %s", idx, cards.card, posdim)
                    im.paste(small_card, (posdim.x, posdim.y), small_card)

        # Resize to the desired image size and return.
        return im.resize((self.width, self.height), Image.LANCZOS)
