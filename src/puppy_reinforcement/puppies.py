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

import os
import random

from aqt import mw

from .config import config
from .tooltip import dogTooltip

mw.dogs = {"cnt": 0, "last": 0, "enc": None, "ivl": config["local"]["encourage_every"]}
addon_path = os.path.dirname(__file__)
dogs_dir = os.path.join(addon_path, "images")
dogs_imgs = [i for i in os.listdir(dogs_dir) if i.endswith((".jpg", ".jpeg", ".png"))]


def getEncouragement(cards: int) -> str:
    last = mw.dogs["enc"]
    if cards >= config["local"]["limit_max"]:
        lst = list(config["local"]["encouragements"]["max"])
    elif cards >= config["local"]["limit_high"]:
        lst = list(config["local"]["encouragements"]["high"])
    elif cards >= config["local"]["limit_middle"]:
        lst = list(config["local"]["encouragements"]["middle"])
    else:
        lst = list(config["local"]["encouragements"]["low"])
    if last and last in lst:
        # skip identical encouragement
        lst.remove(last)
    idx = random.randrange(len(lst))
    mw.dogs["enc"] = lst[idx]
    return lst[idx]


def showDog(*args, **kwargs):
    mw.dogs["cnt"] += 1
    if mw.dogs["cnt"] != mw.dogs["last"] + mw.dogs["ivl"]:
        return
    image_path = os.path.join(dogs_dir, random.choice(dogs_imgs))
    msg = getEncouragement(mw.dogs["cnt"])
    dogTooltip(msg, image=image_path)
    # intermittent reinforcement:
    mw.dogs["ivl"] = max(
        1,
        config["local"]["encourage_every"]
        + random.randint(-config["local"]["max_spread"], config["local"]["max_spread"]),
    )
    mw.dogs["last"] = mw.dogs["cnt"]
