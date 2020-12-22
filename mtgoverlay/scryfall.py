import logging
import mimetypes
import os
import shutil
import tempfile

from PIL import Image
import requests
import requests_cache
from requests_ratelimit_adapter import HTTPRateLimitAdapter

log = logging.getLogger(__name__)
requests_cache.install_cache("scryfall_cache")
rate_limiter = HTTPRateLimitAdapter(calls=1, period=0.5)


class Scryfaller(object):
    def __init__(self):
        self.session = requests.Session()
        self.session.mount("https://", rate_limiter)
        self.session.mount("http://", rate_limiter)

    def get_card_by_mtgo_id(self, mtgo_id: int) -> dict:
        url = "https://api.scryfall.com/cards/mtgo/{mtgo_id}".format(mtgo_id=mtgo_id)
        r = self.session.get(url)
        r.raise_for_status()
        return r.json()

    def get_card_by_name(self, name: str) -> dict:
        r = self.session.get("https://api.scryfall.com/cards/named", params={"exact": name})
        r.raise_for_status()
        return r.json()

    def get_card_image_by_id(self, scryfall_id: str, version: str) -> Image:
        params = {
            "format": "image",
            "version": version,
        }

        r = self.session.get("https://api.scryfall.com/cards/{id}".format(id=scryfall_id), params=params, stream=True)
        r.raise_for_status()

        content_type = r.headers["Content-Type"]
        extension = mimetypes.guess_extension(content_type)

        log.debug("For returned content type %r, guessed extension %r", content_type, extension)

        full_path = os.path.join(tempfile.gettempdir(),
                                 "{name}_{version}{ext}".format(name=scryfall_id,
                                                                version=version,
                                                                ext=extension))
        with open(full_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
            log.debug("Saved image %r to %r", scryfall_id, full_path)

        return Image.open(full_path)


if __name__ == "__main__":
    import sys
    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG,
                        format="[%(asctime)s][%(levelname)s]: %(message)s")
    x = Scryfaller()
    x.save_card_image("Loxodon Warhammer", "./")
