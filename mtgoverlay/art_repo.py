#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Docstring"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import logging
import os
import pkg_resources
import tempfile
from .scryfall import Scryfaller
from PIL import Image, ImageDraw, ImageFont

log = logging.getLogger(__name__)
scryfaller = Scryfaller()


class ArtRepo(object):
    def __init__(self):
        self.art_cache = os.path.join(tempfile.gettempdir(), "art_cache")
        os.makedirs(self.art_cache, exist_ok=True)

    def get_art_crop_image(self, scryfall_id: str) -> Image:
        return self.get_cached_image(scryfall_id, "art_crop")

    def get_full_card_image(self, scryfall_id: str) -> Image:
        return self.get_cached_image(scryfall_id, "png")

    def get_cached_image(self, scryfall_id: str, version: str) -> Image:
        cached_path = os.path.join(self.art_cache, "{0}_{1}.png".format(scryfall_id, version))
        if os.path.exists(cached_path):
            log.debug("[%s] Using cache", scryfall_id)
            im = Image.open(cached_path).convert("RGBA")
        else:
            log.debug("[%s] Downloading from scryfall", scryfall_id)
            im = scryfaller.get_card_image_by_id(scryfall_id, version).convert('RGBA')
            im.save(cached_path)
        return im

    def get_slice_obj(self, scryfall_id: str) -> 'ArtSlice':
        return ArtSlice(self, scryfall_id)

    def get_resource_image(self, name: str) -> Image:
        stream = pkg_resources.resource_stream("mtgoverlay.resources", name)
        return Image.open(stream).convert('RGBA')

    def get_resource_font(self, name: str, size: int):
        stream = pkg_resources.resource_stream("mtgoverlay.resources", name)
        return ImageFont.truetype(stream, size)

    def get_small_text_font(self, size: int):
        return self.get_resource_font("belerenbold.ttf", size)


class ArtSlice(object):
    def __init__(self, art_repo: ArtRepo, scryfall_id: str):
        self.art_repo = art_repo
        self.scryfall_id = scryfall_id

    def draw(self, image: Image, width: int, height: int, draw_x: int, draw_y: int, text: str):
        slice_path = os.path.join(self.art_repo.art_cache,
                                  "{0}_slice{1}x{2}.png".format(self.scryfall_id, width, height))
        if os.path.exists(slice_path):
            log.debug("[%s] Using cache", slice_path)
            slice_im = Image.open(slice_path)
        else:
            log.debug("[%s] Generating slice", slice_path)
            slice_im = self.generate_slice(width, height)
            slice_im.save(slice_path)

        # Now make some text
        x = 3
        y = 3
        shadowcolor = (0, 0, 0, 255)
        fillcolor = (255, 255, 255, 255)

        log.debug("Drawing text %s", text)

        draw = ImageDraw.Draw(slice_im)
        font = self.art_repo.get_small_text_font(height-(y * 2)-2)

        for i in range(-1, 2):
            for j in range(-1, 2):
                draw.text((x + i, y + j), text, font=font, fill=shadowcolor)

        # now draw the text over it
        draw.text((x, y), text, font=font, fill=fillcolor)

        log.debug("Drawing slice at %s x %s", draw_x, draw_y)
        image.paste(slice_im, (draw_x, draw_y))

    def generate_slice(self, width: int, height: int):
        # First get the main image.
        im = self.art_repo.get_art_crop_image(self.scryfall_id)

        im_width, im_height = im.size
        log.debug("[%s] Slicing main image (%d x %d)", self.scryfall_id, im_width, im_height)

        # Slice some pixels at the 20% point of the image
        start_height = im_height // 5
        half_slice = height // 2
        slice_coords = (0,
                        start_height - half_slice,
                        width,
                        start_height - half_slice + height)
        slice = im.crop(slice_coords)
        gradient_slice = self.apply_black_gradient(slice)
        return gradient_slice

    def apply_black_gradient(self, input_im: Image, gradient=1., initial_opacity=1.):
        """
        Applies a black gradient to the image, going from left to right.

        Arguments:
        ---------
            path_in: string
                path to image to apply gradient to
            path_out: string (default 'out.png')
                path to save result to
            gradient: float (default 1.)
                gradient of the gradient; should be non-negative;
                if gradient = 0., the image is black;
                if gradient = 1., the gradient smoothly varies over the full width;
                if gradient > 1., the gradient terminates before the end of the width;
            initial_opacity: float (default 1.)
                scales the initial opacity of the gradient (i.e. on the far left of the image);
                should be between 0. and 1.; values between 0.9-1. give good results
        """

        # get image to operate on
        width, height = input_im.size

        # create a gradient that
        # starts at full opacity * initial_value
        # decrements opacity by gradient * x / width
        alpha_gradient = Image.new('L', (width, 1), color=0xFF)
        for x in range(width):
            a = int((initial_opacity * 255.) * (1. - gradient * float(x) / width))
            if a > 0:
                alpha_gradient.putpixel((x, 0), a)
            else:
                alpha_gradient.putpixel((x, 0), 0)
            # print '{}, {:.2f}, {}'.format(x, float(x) / width, a)
        alpha = alpha_gradient.resize(input_im.size)

        # create black image, apply gradient
        black_im = Image.new('RGBA', (width, height), color=0)  # i.e. black
        black_im.putalpha(alpha)

        # make composite with original image
        output_im = Image.alpha_composite(input_im, black_im)
        return output_im
