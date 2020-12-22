#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Docstring"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
import sys
import mtgoverlay

log = logging.getLogger(__name__)


def deckoverview(deckfile: str,
                 decklist_image: str,
                 width: int=1920,
                 height: int=1080):
    """Help string for deckoverview."""

    # Load deck from the XML file.
    deck = mtgoverlay.Deck.from_dek_file(deckfile)
    log.info("Loaded deck %s", deck)

    # Save the deck list
    decklist = mtgoverlay.render_decklist(deck, width, height)
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
