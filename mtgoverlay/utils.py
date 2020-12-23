#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Docstring"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
from PIL import Image
import mtgoverlay

log = logging.getLogger(__name__)
art_repo = mtgoverlay.ArtRepo()


def render_frame(deck: mtgoverlay.Deck, width: int, height: int) -> Image:
    frame = mtgoverlay.LegendaryFrame(width, height)
    return frame.render_deck(deck)


def render_deck(deck: mtgoverlay.Deck, width: int, height: int) -> Image:
    frame = mtgoverlay.CardRenderer(width, height)
    return frame.render_deck(deck)
