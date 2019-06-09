# -*- coding: utf-8 -*-

# Puppy Reinforcement Add-on for Anki
#
# Copyright (C) 2016-2019  Aristotelis P. <https://glutanimate.com/>
# Copyright (C) 2019  zjosua <https://github.com/zjosua>
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

"""
Initializes add-on components.
"""

import os
import random

from aqt import mw
from aqt.qt import *
from anki.hooks import addHook

from .config import local_conf

mw.dogs = {
    "cnt": 0,
    "last": 0,
    "enc": None,
    "ivl": local_conf["encourage_every"]
}

addon_path = os.path.dirname(__file__)
dogs_dir = os.path.join(addon_path, 'images')
dogs_imgs = [i for i in os.listdir(dogs_dir)
             if i.endswith((".jpg", ".jpeg", ".png"))]

_tooltipTimer = None
_tooltipLabel = None

def dogTooltip(msg, image=":/icons/help-hint.png",
               period=local_conf["duration"], parent=None):
    global _tooltipTimer, _tooltipLabel
    class CustomLabel(QLabel):
        def mousePressEvent(self, evt):
            evt.accept()
            self.hide()
    closeTooltip()
    aw = parent or mw.app.activeWindow() or mw
    lab = CustomLabel("""\
<table cellpadding=10>
<tr>
<td><img height=%d src="%s"></td>
<td valign="middle">
    <center><b>%i cards done so far!</b><br>%s</center>
</td>
</tr>
</table>""" % (local_conf["image_height"], image, mw.dogs["cnt"], msg), aw)
    lab.setFrameStyle(QFrame.Panel)
    lab.setLineWidth(2)
    lab.setWindowFlags(Qt.ToolTip)
    p = QPalette()
    p.setColor(QPalette.Window, QColor(local_conf["tooltip_color"]))
    p.setColor(QPalette.WindowText, QColor("#000000"))
    lab.setPalette(p)
    vdiff = (local_conf["image_height"] - 128) / 2
    lab.move(
        aw.mapToGlobal(QPoint(0, -260-vdiff + aw.height())))
    lab.show()
    _tooltipTimer = mw.progress.timer(
        period, closeTooltip, False)
    _tooltipLabel = lab

def closeTooltip():
    global _tooltipLabel, _tooltipTimer
    if _tooltipLabel:
        try:
            _tooltipLabel.deleteLater()
        except:
            # already deleted as parent window closed
            pass
        _tooltipLabel = None
    if _tooltipTimer:
        _tooltipTimer.stop()
        _tooltipTimer = None

def getEncouragement(cards):
    last = mw.dogs["enc"]
    if cards >= local_conf["limit_max"]:
        lst = list(local_conf["encouragements"]["max"])
    elif cards >= local_conf["limit_high"]:
        lst = list(local_conf["encouragements"]["high"])
    elif cards >= local_conf["limit_middle"]:
        lst = list(local_conf["encouragements"]["middle"])
    else:
        lst = list(local_conf["encouragements"]["low"])
    if last and last in lst:
        # skip identical encouragement
        lst.remove(last)
    idx = random.randrange(len(lst))
    mw.dogs["enc"] = lst[idx]
    return lst[idx]

def showDog():
    mw.dogs["cnt"] += 1
    if mw.dogs["cnt"] != mw.dogs["last"] + mw.dogs["ivl"]:
        return
    image_path = os.path.join(dogs_dir, random.choice(dogs_imgs))
    msg = getEncouragement(mw.dogs["cnt"])
    dogTooltip(msg, image=image_path)
    # intermittent reinforcement:
    mw.dogs["ivl"] = max(1, local_conf["encourage_every"] +
                         random.randint(-local_conf["max_spread"],
                                        local_conf["max_spread"]))
    mw.dogs["last"] = mw.dogs["cnt"]

addHook("showQuestion", showDog)
