# -*- coding: utf-8 -*-

# Puppy Reinforcement Add-on for Anki
#
# Copyright (C) 2016-2023  Aristotelis P. <https://glutanimate.com/>
# Copyright (C) 2019-2020  zjosua <https://github.com/zjosua>
# Copyright (C) 2016-2023  Ankitects Pty Ltd and contributors
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


from typing import Optional, cast

from aqt.progress import ProgressManager
from aqt.qt import (
    QColor,
    QFrame,
    QLabel,
    QMouseEvent,
    QPalette,
    QPoint,
    QResizeEvent,
    Qt,
    QTimer,
    QWidget,
)

from ..libaddon.platform import is_anki_version_in_range


class Notification(QLabel):
    _current_timer: Optional[QTimer] = None
    _current_instance: Optional["Notification"] = None

    silentlyClose = True

    def __init__(
        self,
        text: str,
        progress_manager: ProgressManager,
        parent: QWidget,
        duration: int = 3000,
        align_horizontal: str = "left",
        align_vertical: str = "bottom",
        space_horizontal: int = 0,
        space_vertical: int = 0,
        fg_color: str = "#000000",
        bg_color: str = "#FFFFFF",
        **kwargs,
    ):
        super().__init__(text, parent=parent, **kwargs)
        self._progress_manager = progress_manager
        self._duration = duration
        self._align_horizontal = align_horizontal
        self._align_vertical = align_vertical
        self._space_horizontal = space_horizontal
        self._space_vertical = space_vertical
        self.setFrameStyle(QFrame.Shape.Panel)
        self.setLineWidth(2)
        self.setWindowFlags(Qt.WindowType.ToolTip)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(bg_color))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(fg_color))
        self.setPalette(palette)

    def show(self) -> None:
        # TODO: drop dependency on mw
        Notification._close_singleton()
        super().show()
        Notification._current_instance = self
        if is_anki_version_in_range("2.1.54"):
            Notification._current_timer = self._progress_manager.timer(
                3000, Notification._close_singleton, False, parent=self.parent()
            )
        else:
            Notification._current_timer = self._progress_manager.timer(
                3000, Notification._close_singleton, False
            )

    def mousePressEvent(self, evt: QMouseEvent):
        evt.accept()
        self.hide()

    def resizeEvent(self, event: QResizeEvent) -> None:
        # true geometry is only known once resizeEvent fires
        self._set_position()
        super().resizeEvent(event)

    def _set_position(self):
        align_horizontal = self._align_horizontal
        align_vertical = self._align_vertical

        parent = self._parent()

        if align_horizontal == "left":
            x: float = 0 + self._space_horizontal
        elif align_horizontal == "right":
            x = parent.width() - self.width() - self._space_horizontal
        elif align_horizontal == "center":
            x = (parent.width() - self.width()) / 2
        else:
            raise ValueError(f"Alignment value {align_horizontal} is not supported")

        if align_vertical == "top":
            y: float = 0 + self._space_vertical
        elif align_vertical == "bottom":
            y = parent.height() - self.height() - self._space_vertical
        elif align_vertical == "center":
            y = (parent.height() - self.height()) / 2
        else:
            raise ValueError(f"Alignment value {align_vertical} is not supported")

        self.move(parent.mapToGlobal(QPoint(int(x), int(y))))
        # Workaround for tooltips appearing squashed on Qt 6.6:
        self.setMinimumWidth(self.width())
        self.setMinimumHeight(self.height())
        self.update()

    def _parent(self) -> QWidget:  # pyqt stubs workaround
        return cast(QWidget, self.parent())

    @classmethod
    def _close_singleton(cls):
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
