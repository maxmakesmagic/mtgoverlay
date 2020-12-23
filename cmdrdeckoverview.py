#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Commander deck generator"""

import logging
import sys
import mtgoverlay
import argparse

log = logging.getLogger(__name__)

def fish():
    # Choose appropriate card widths
    card_width = 150
    cmdr_width = 500

    # Make start draw position
    base_x = 627
    base_y = 188

    positions = []

    # 3 Rows
    for row in range(0, 4):
        # 8 columns
        for column in range(0, 8):
            # 4 cards in each column
            for colcard in range(0, 4):
                # We should be able to definitively place a card.

                # Add the column into the X calculation.
                pos_x = base_x + (column * (card_width + 10))

                # For the Y calculation:
                # The column card adds on enough to see the card name
                # The row adds on 300 px
                pos_y = int(base_y + (colcard * 25) + (row * 300))

                positions.append(mtgoverlay.PositionDimension(pos_x, pos_y, card_width))

    # Commander
    positions[99] = mtgoverlay.PositionDimension(58, 289, cmdr_width)
    return positions


def sheep():
    # Choose appropriate card dimensions
    card_width = 126
    card_height = 120

    three_cell_width = card_width * 3
    cmdr_width = 280
    margin_left = int((three_cell_width - cmdr_width) / 2)

    # Make start draw position
    base_x = 15
    base_y = 170

    positions = []

    # 7 Rows
    for row in range(7):
        # 15 columns
        for column in range(15):
            # Skip the middle 3 cells of the first 2 rows
            if row < 2 and 6 <= column < 9:
                continue

            pos_x = int(base_x + (column * card_width))
            pos_y = int(base_y + (row * card_height))

            positions.append(mtgoverlay.PositionDimension(pos_x, pos_y, card_width))

    # Commander
    positions.append(mtgoverlay.PositionDimension((6 * card_width) + margin_left + base_x, 15, cmdr_width))
    return positions


LAYOUTS = {
    "fish": fish(),
    "sheep": sheep()
}


def deckoverview(args):
    """Help string for deckoverview."""

    # Load deck from the XML file.
    deck = mtgoverlay.Deck.from_dek_file(args.dekfile)
    log.info("Loaded deck %s", deck)

    # Save the deck list
    layout = LAYOUTS[args.layout]
    renderer = mtgoverlay.GenericRenderer(args.width, args.height, layout)
    decklist = renderer.render_deck(deck)

    # Work out where to save the image
    decklist_image = args.output
    if decklist_image is None:
        decklist_image = "{0}.png".format(args.dekfile)

    decklist.save(decklist_image)
    log.info("Saved decklist image as %s", decklist_image)


def main():
    """Main handling function. Wraps deckoverview."""
    logging.basicConfig(format="%(asctime)s %(levelname)-5.5s %(message)s",
                        stream=sys.stdout,
                        level=logging.DEBUG)

    # Parse options
    parser = argparse.ArgumentParser(description='Generate a Commander decklist')
    parser.add_argument("--layout", help="Which layout to use", default="fish")
    parser.add_argument("--width", help="Image width", default=1920)
    parser.add_argument("--height", help="Image height", default=1080)
    parser.add_argument("--output", help="File to output to")
    parser.add_argument("dekfile")
    args = parser.parse_args()

    # Run main script.
    deckoverview(args)

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        log.exception(e)
        sys.exit(1)
