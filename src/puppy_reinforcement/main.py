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
from aqt.addcards import AddCards
from aqt.reviewer import Reviewer
from anki.hooks import wrap

from .config import config

mw.dogs = {
    "cnt": 0,
    "last": 0,
    "enc": None,
    "ivl": config["local"]["encourage_every"]
}

addon_path = os.path.dirname(__file__)
dogs_dir = os.path.join(addon_path, 'images')
dogs_imgs = [i for i in os.listdir(dogs_dir)
             if i.endswith((".jpg", ".jpeg", ".png"))]

_tooltipTimer = None
_tooltipLabel = None

def dogTooltip(msg, image=":/icons/help-hint.png",
               period=config["local"]["duration"], parent=None):
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
</table>""" % (config["local"]["image_height"], image, mw.dogs["cnt"], msg), aw)
    lab.setFrameStyle(QFrame.Panel)
    lab.setLineWidth(2)
    lab.setWindowFlags(Qt.ToolTip)
    p = QPalette()
    p.setColor(QPalette.Window, QColor(config["local"]["tooltip_color"]))
    p.setColor(QPalette.WindowText, QColor("#000000"))
    lab.setPalette(p)
    vdiff = (config["local"]["image_height"] - 128) / 2
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

def showDog():
    mw.dogs["cnt"] += 1
    if mw.dogs["cnt"] != mw.dogs["last"] + mw.dogs["ivl"]:
        return
    image_path = os.path.join(dogs_dir, random.choice(dogs_imgs))
    msg = getEncouragement(mw.dogs["cnt"])
    dogTooltip(msg, image=image_path)
    # intermittent reinforcement:
    mw.dogs["ivl"] = max(1, config["local"]["encourage_every"] +
                         random.randint(-config["local"]["max_spread"],
                                        config["local"]["max_spread"]))
    mw.dogs["last"] = mw.dogs["cnt"]

def _myAnswerCard(self, ease, _old):
    if self.mw.state != "review":
        # showing resetRequired screen; ignore key
        return
    if self.state != "answer":
        return
    if self.mw.col.sched.answerButtons(self.card) < ease:
        return
    _old(self, ease)
    showDog()

def myAddNote(self, note, _old):
    ret = _old(self, note)
    if ret:
        showDog()
    return ret

Reviewer._answerCard = wrap(Reviewer._answerCard, _myAnswerCard, "around")
if config["local"]["count_adding"]:
    AddCards.addNote = wrap(AddCards.addNote, myAddNote, "around")
