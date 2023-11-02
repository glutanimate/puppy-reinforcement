# -*- coding: utf-8 -*-

# Puppy Reinforcement Add-on for Anki
#
# Copyright (C) 2016-2020  Aristotelis P. <https://glutanimate.com/>
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
Module-level entry point for the add-on
"""

from typing import TYPE_CHECKING

from aqt import mw as main_window

from ._version import __version__  # noqa: F401
from .config import config
from .consts import ADDON
from .libaddon.consts import set_addon_properties
from .reinforcer import PuppyReinforcer
from .views import initialize_views

if TYPE_CHECKING:
    assert main_window is not None

set_addon_properties(ADDON)

puppy_reinforcer = PuppyReinforcer(main_window, config)

main_window._puppy_reinforcer = puppy_reinforcer  # type: ignore[attr-defined]

initialize_views(puppy_reinforcer)
