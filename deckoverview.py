#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Docstring"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
import sys
import math

import mtgoverlay
import typing

log = logging.getLogger(__name__)


def layout1() -> typing.List[mtgoverlay.PositionDimension]:
    # Generate the standard 60 card + 15 card layout
    card_width = 275
    base_x = 50
    base_y = 226
    positions = []

    for ii in range(75):
        if 0 <= ii < 60:
            draw_x = base_x + ((card_width + 15) * math.floor(ii / 12))
            draw_y = base_y + (42 * (ii % 12))
        else:
            draw_x = 1595
            draw_y = base_y + (42 * (ii - 60)) - 126

        positions.append(mtgoverlay.PositionDimension(draw_x, draw_y, card_width))
    return positions


def deckoverview(deckfile: str,
                 decklist_image: str,
                 width: int=1920,
                 height: int=1080):
    """Help string for deckoverview."""

    # Load deck from the XML file.
    deck = mtgoverlay.Deck.from_dek_file(deckfile)
    log.info("Loaded deck %s", deck)

    # Save the deck list
    layout = layout1()
    renderer = mtgoverlay.GenericRenderer(width, height, layout)
    decklist = renderer.render_deck(deck)
    decklist.save(decklist_image)
    log.info("Saved decklist image as %s", decklist_image)


def main():
    """Main handling function. Wraps deckoverview."""
    logging.basicConfig(format="%(asctime)s %(levelname)-5.5s %(message)s",
                        stream=sys.stdout,
                        level=logging.DEBUG)

    # Run main script.
    deckoverview(sys.argv[1],
                 "{0}.png".format(sys.argv[1]))


if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        log.exception(e)
        sys.exit(1)
