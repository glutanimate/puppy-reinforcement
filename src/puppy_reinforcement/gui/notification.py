# -*- coding: utf-8 -*-

# Puppy Reinforcement Add-on for Anki
#
# Copyright (C) 2016-2020  Aristotelis P. <https://glutanimate.com/>
# Copyright (C) 2019-2020  zjosua <https://github.com/zjosua>
# Copyright (C) 2016-2020  Ankitects Pty Ltd and contributors
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
Customizable notification pop-up
"""


from typing import Optional

from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QColor, QMouseEvent, QPalette, QResizeEvent
from PyQt5.QtWidgets import QFrame, QLabel, QWidget

from aqt.progress import ProgressManager


class Notification(QLabel):

    _current_timer: Optional[QTimer] = None
    _current_instance: Optional["Notification"] = None

    silentlyClose = True

    def __init__(
        self,
        text: str,
        progress_manager: ProgressManager,
        duration: int = 3000,
        align_horizontal: str = "left",
        align_vertical: str = "bottom",
        space_horizontal: int = 0,
        space_vertical: int = 0,
        fg_color: str = "#000000",
        bg_color: str = "#FFFFFF",
        parent: Optional[QWidget] = None,
        **kwargs,
    ):
        super().__init__(text, parent=parent, **kwargs)
        self._progress_manager = progress_manager
        self._duration = duration
        self._align_horizontal = align_horizontal
        self._align_vertical = align_vertical
        self._space_horizontal = space_horizontal
        self._space_vertical = space_vertical
        self.setFrameStyle(QFrame.Panel)
        self.setLineWidth(2)
        self.setWindowFlags(Qt.ToolTip)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(bg_color))
        palette.setColor(QPalette.WindowText, QColor(fg_color))
        self.setPalette(palette)

    def show(self) -> None:
        # TODO: drop dependency on mw
        Notification._closeSingleton()
        super().show()
        Notification._current_instance = self
        Notification._current_timer = self._progress_manager.timer(
            3000, Notification._closeSingleton, False
        )

    def mousePressEvent(self, evt: QMouseEvent):
        evt.accept()
        self.hide()

    def resizeEvent(self, event: QResizeEvent) -> None:
        # true geometry is only known once resizeEvent fires
        self._setPosition()
        super().resizeEvent(event)

    def _setPosition(self):
        align_horizontal = self._align_horizontal
        align_vertical = self._align_vertical

        if align_horizontal == "left":
            x = 0 + self._space_horizontal
        elif align_horizontal == "right":
            x = self.parent().width() - self.width() - self._space_horizontal
        elif align_horizontal == "center":
            x = (self.parent().width() - self.width()) / 2
        else:
            raise ValueError(f"Alignment value {align_horizontal} is not supported")

        if align_vertical == "top":
            y = 0 + self._space_vertical
        elif align_vertical == "bottom":
            y = self.parent().height() - self.height() - self._space_vertical
        elif align_vertical == "center":
            y = (self.parent().height() - self.height()) / 2
        else:
            raise ValueError(f"Alignment value {align_vertical} is not supported")

        self.move(
            self.parent().mapToGlobal(QPoint(x, y))  # type:ignore
        )

    @classmethod
    def _closeSingleton(cls):
        if cls._current_instance:
            try:
                cls._current_instance.deleteLater()
            except:  # noqa: E722
                # already deleted as parent window closed
                pass
            cls._current_instance = None
        if cls._current_timer:
            cls._current_timer.stop()
            cls._current_timer = None
