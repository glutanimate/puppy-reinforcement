# -*- coding: utf-8 -*-

# Puppy Reinforcement Add-on for Anki
#
# Copyright (C) 2016-2020  Aristotelis P. <https://glutanimate.com/>
# Copyright (C) 2019-2020  zjosua <https://github.com/zjosua>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

import random
import re
from pathlib import Path
import pickle
import os

from aqt.main import AnkiQt

from .tooltip import dogTooltip

from .libaddon.platform import PATH_THIS_ADDON, pathUserFiles
from .libaddon.anki.configmanager import ConfigManager

from typing import List


class PuppyReinforcer:

    _extensions = re.compile(r"\.(jpg|jpeg|png|bmp|gif)$")

    def __init__(self, mw: AnkiQt, config: ConfigManager):
        self._mw = mw
        self._config = config
        self._images: List[str] = []
        self._playlist_path = Path(PATH_THIS_ADDON) / "playlist.pkl"

        self._state = {
            "cnt": 0,
            "last": 0,
            "enc": None,
            "ivl": self._config["local"]["encourage_every"],
        }

    def showDog(self, *args, **kwargs):
        config = self._config["local"]
        self._state["cnt"] += 1
        if self._state["cnt"] != self._state["last"] + self._state["ivl"]:
            return
        image_path = self._getNextImage()
        encouragement = self._getEncouragement(self._state["cnt"])
        self._showTooltip(encouragement, image_path)
        # intermittent reinforcement:
        self._state["ivl"] = max(
            1,
            config["encourage_every"]
            + random.randint(-config["max_spread"], config["max_spread"]),
        )
        self._state["last"] = self._state["cnt"]

    def _showTooltip(self, encouragement: str, image_path: str):
        config = self._config["local"]
        dogTooltip(
            encouragement,
            image_path,
            self._state["cnt"],
            config["image_height"],
            config["tooltip_color"],
            config["duration"],
        )

    def _readImages(self):
        default_path = Path(PATH_THIS_ADDON) / "images"
        user_path = Path(pathUserFiles())

        images = []

        for path in (user_path, default_path):
            if not path.is_dir():
                continue
            for p in path.iterdir():
                if not self._extensions.match(p.suffix.lower()):
                    continue
                images.append(str(p.resolve()))

            if images and self._config["local"]["disable_default_images"]:
                break

        self._images = images

    def _readPlaylist(self):
        images = []
        try:
            with open(self._playlist_path, "rb") as handle:
                images = pickle.load(handle)
        except Exception:
            pass

        self._images = images

    def _savePlaylist(self):
        with open(self._playlist_path, "wb") as handle:
            pickle.dump(self._images, handle)

    def _rebuildPlaylist(self):
        self._readImages()
        random.shuffle(self._images)

    def _getNextImage(self) -> str:
        if not self._images:
            self._readPlaylist()
        if not self._images:
            self._rebuildPlaylist()
        img = ""
        while self._images:
            img = self._images.pop()
            if os.path.isfile(img):
                break
        self._savePlaylist()
        return img

    def _getEncouragement(self, cards: int) -> str:
        config = self._config["local"]
        last = self._state["enc"]
        if cards >= config["limit_max"]:
            lst = list(config["encouragements"]["max"])
        elif cards >= config["limit_high"]:
            lst = list(config["encouragements"]["high"])
        elif cards >= config["limit_middle"]:
            lst = list(config["encouragements"]["middle"])
        else:
            lst = list(config["encouragements"]["low"])
        if last and last in lst:
            # skip identical encouragement
            lst.remove(last)
        idx = random.randrange(len(lst))
        self._state["enc"] = lst[idx]
        return lst[idx]
