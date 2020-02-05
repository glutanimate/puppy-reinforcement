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

"""
Puppy tooltip
"""


from PyQt5.QtCore import QPoint, QTimer, Qt
from PyQt5.QtGui import QColor, QMouseEvent, QPalette
from PyQt5.QtWidgets import QFrame, QLabel, QWidget

from aqt import mw

from typing import Optional


class CustomLabel(QLabel):
    def mousePressEvent(self, evt: QMouseEvent):
        evt.accept()
        self.hide()


_tooltipTimer: Optional[QTimer] = None
_tooltipLabel: Optional[CustomLabel] = None


def dogTooltip(
    encouragement: str,
    image_path: str,
    count: int,
    image_height: int,
    color: str,
    duration: int,
    parent: QWidget = None,
):
    global _tooltipTimer, _tooltipLabel

    closeTooltip()
    aw = parent or mw.app.activeWindow() or mw
    lab = CustomLabel(
        f"""\
<table cellpadding=10>
<tr>
<td><img height={image_height} src="{image_path}"></td>
<td valign="middle">
    <center><b>{count} {'cards' if count > 1 else 'card'} done so far!</b><br>
    {encouragement}</center>
</td>
</tr>
</table>""",
        aw,
    )
    lab.setFrameStyle(QFrame.Panel)
    lab.setLineWidth(2)
    lab.setWindowFlags(Qt.ToolTip)
    p = QPalette()
    p.setColor(QPalette.Window, QColor(color))
    p.setColor(QPalette.WindowText, QColor("#000000"))
    lab.setPalette(p)
    vdiff = (image_height - 128) / 2
    lab.move(aw.mapToGlobal(QPoint(0, -260 - vdiff + aw.height())))  # type:ignore
    lab.show()
    _tooltipTimer = mw.progress.timer(duration, closeTooltip, False)
    _tooltipLabel = lab


def closeTooltip():
    global _tooltipLabel, _tooltipTimer
    if _tooltipLabel:
        try:
            _tooltipLabel.deleteLater()
        except:  # noqa: E722
            # already deleted as parent window closed
            pass
        _tooltipLabel = None
    if _tooltipTimer:
        _tooltipTimer.stop()
        _tooltipTimer = None
