# -*- coding: utf-8 -*-

# Puppy Reinforcement Add-on for Anki
#
# Copyright (C) 2016-2023  Aristotelis P. <https://glutanimate.com/>
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

from typing import TYPE_CHECKING

import random
import re
from pathlib import Path
from typing import List, Optional

if TYPE_CHECKING:
    from aqt.main import AnkiQt

from .libaddon.anki.configmanager import ConfigManager
from .libaddon.platform import PATH_THIS_ADDON, pathUserFiles
from .gui.notification import Notification


class PuppyReinforcer:
    _extensions = re.compile(r"\.(jpg|jpeg|png|bmp|gif)$")

    def __init__(self, mw: "AnkiQt", config: ConfigManager):
        self._mw = mw
        self._config = config
        self._images: List[str] = []
        self._playlist: List[int] = []  # self._images indexes

        self._state = {
            "cnt": 0,
            "last": 0,
            "enc": None,
            "ivl": self._config["local"]["encourage_every"],
            "cutoff": False,
        }

        self._read_images()
        self._rebuild_playlist()
        self._shuffle_playlist()

    def show_dog(self, *args, **kwargs):
        local_config = self._config["local"]

        if local_config["reset_counter_on_new_day"]:
            self._maybe_reset_count()

        self._state["cnt"] += 1
        if self._state["cnt"] != self._state["last"] + self._state["ivl"]:
            return
        image_path = self._get_next_image()
        encouragement = self._get_encouragement(self._state["cnt"])
        self._show_tooltip(encouragement, image_path)
        # intermittent reinforcement:
        self._state["ivl"] = max(
            1,
            local_config["encourage_every"]
            + random.randint(-local_config["max_spread"], local_config["max_spread"]),
        )
        self._state["last"] = self._state["cnt"]

    def _show_tooltip(self, encouragement: str, media_path: str):
        local_config = self._config["local"]
        count = self._state["cnt"]

        text = f"<b>{count} {'cards' if count > 1 else 'card'} done so far!</b><br>{encouragement}"

        notification = Notification(
            text,
            media_path,
            local_config["image_height"],
            self._mw.progress,
            duration=local_config["duration"],
            parent=self._mw.app.activeWindow() or self._mw,
            align_horizontal=local_config["tooltip_align_horizontal"],
            align_vertical=local_config["tooltip_align_vertical"],
            space_horizontal=local_config["tooltip_space_horizontal"],
            space_vertical=local_config["tooltip_space_vertical"],
            bg_color=local_config["tooltip_color"],
        )

        notification.show()

    def _read_images(self):
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

        return images

    def _maybe_reset_count(self):
        """
        Reset on day cutoff traversal
        """
        cutoff = self._get_day_cutoff()

        if self._state["cutoff"] is False:
            # initial value, only available after profile load
            self._state["cutoff"] = cutoff
        elif self._state["cutoff"] == cutoff:
            return

        self._state["cnt"] = 0
        self._state["cutoff"] = cutoff

    def _get_day_cutoff(self) -> Optional[int]:
        if (collection := self._mw.col) is None:
            return None
        scheduler = collection.sched
        if hasattr(scheduler, "day_cutoff"):
            return scheduler.day_cutoff  # 2.1.54+
        try:
            return scheduler.dayCutoff  # type: ignore[union-attr]
        except AttributeError:
            return None

    def _rebuild_playlist(self):
        self._playlist = list(range(len(self._images)))

    def _shuffle_playlist(self):
        random.shuffle(self._playlist)

    def _get_next_image(self) -> str:
        try:
            index = self._playlist.pop()
        except IndexError:
            self._rebuild_playlist()
            self._shuffle_playlist()
            index = self._playlist.pop()
        return self._images[index]

    def _get_encouragement(self, cards: int) -> str:
        local_config = self._config["local"]
        last = self._state["enc"]
        if cards >= local_config["limit_max"]:
            lst = list(local_config["encouragements"]["max"])
        elif cards >= local_config["limit_high"]:
            lst = list(local_config["encouragements"]["high"])
        elif cards >= local_config["limit_middle"]:
            lst = list(local_config["encouragements"]["middle"])
        else:
            lst = list(local_config["encouragements"]["low"])
        if last and last in lst:
            # skip identical encouragement
            lst.remove(last)
        idx = random.randrange(len(lst))
        self._state["enc"] = lst[idx]
        return lst[idx]
