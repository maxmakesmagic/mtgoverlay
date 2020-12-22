#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Docstring"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
import sys
import mtgoverlay

log = logging.getLogger(__name__)


def mtgoverlay_main(deckfile: str,
                    frame_image: str,
                    decklist_image: str,
                    width: int=355,
                    height: int=1080):
    """Help string for mtgoverlay_main."""

    # Load deck from the XML file.
    deck = mtgoverlay.Deck.from_dek_file(deckfile)
    log.info("Loaded deck %s", deck)

    # Save the rendered frame
    frame = mtgoverlay.render_frame(deck, width, height)
    frame.save(frame_image)
    log.info("Saved frame image as %s", frame_image)

    # Save the card list
    cardlist = mtgoverlay.render_deck(deck, width, height)
    cardlist.save(decklist_image)
    log.info("Saved decklist image as %s", decklist_image)


def main():
    """Main handling function. Wraps mtgoverlay()."""
    logging.basicConfig(format="%(asctime)s %(levelname)-5.5s %(message)s",
                        stream=sys.stdout,
                        level=logging.DEBUG)

    # Run main script.
    mtgoverlay_main(sys.argv[1],
                    "{0}_frame.png".format(sys.argv[1]),
                    "{0}_decklist.png".format(sys.argv[1]))

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        log.exception(e)
        sys.exit(1)
