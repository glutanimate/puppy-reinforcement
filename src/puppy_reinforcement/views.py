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

from anki.hooks import wrap
from aqt.addcards import AddCards
from aqt.reviewer import Reviewer

from .config import config
from .reinforcer import PuppyReinforcer

from typing import Any


def initializeViews(puppy_reinforcer: PuppyReinforcer):
    try:
        from aqt.gui_hooks import reviewer_did_answer_card, add_cards_did_add_note

        reviewer_did_answer_card.append(puppy_reinforcer.showDog)
        if config["local"]["count_adding"]:
            add_cards_did_add_note.append(puppy_reinforcer.showDog)

    except (ImportError, ModuleNotFoundError):  # Anki < 2.1.20
        # TODO: Drop monkey-patches in the future
        def _myAnswerCard(self, ease: int, _old: Any):
            if self.mw.state != "review":
                # showing resetRequired screen; ignore key
                return
            if self.state != "answer":
                return
            if self.mw.col.sched.answerButtons(self.card) < ease:
                return
            _old(self, ease)
            puppy_reinforcer.showDog()

        def myAddNote(self, note, _old):
            ret = _old(self, note)
            if ret:
                puppy_reinforcer.showDog()
            return ret

        Reviewer._answerCard = wrap(Reviewer._answerCard, _myAnswerCard, "around")
        if config["local"]["count_adding"]:
            AddCards.addNote = wrap(AddCards.addNote, myAddNote, "around")
