# -*- coding: utf-8 -*-
#
#   ktug-hanyang-pua: KTUG HanYang PUA conversion table reader
#   Copyright (C) 2015-2017 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
import logging


logger = logging.getLogger(__name__)


class Tree:

    MAPPINGS = (
        'U+E0BC => U+115F U+1161 U+11AE',
        'U+E0BD => U+115F U+1161 U+D7CD',
        'U+E0C6 => U+115F U+11A3',
        'U+E0C7 => U+115F U+11A3 U+11AE',
        'U+E0C8 => U+115F U+1163 U+11AB',
        'U+F86A =>',
    )

    @property
    def NODELIST(self):
        from ktug_hanyang_pua.models import Node
        return (
            Node(parent=-1, source=None, target=0xF86A),
            Node(parent=0, source=0x115F, target=None),
            Node(parent=1, source=0x1161, target=None),
            Node(parent=2, source=0x11AE, target=0xE0BC),
            Node(parent=2, source=0xD7CD, target=0xE0BD),
            Node(parent=1, source=0x11A3, target=0xE0C6),
            Node(parent=5, source=0x11AE, target=0xE0C7),
            Node(parent=1, source=0x1163, target=None),
            Node(parent=7, source=0x11AB, target=0xE0C8),
        )

    NODEPACKS = (
        b'\xff\xff\x00\x00j\xf8',       # 0
        b'\x00\x00_\x11\x00\x00',       # 1
        b'\x01\x00a\x11\x00\x00',       # 2
        b'\x02\x00\xae\x11\xbc\xe0',    # 3
        b'\x02\x00\xcd\xd7\xbd\xe0',    # 4
        b'\x01\x00\xa3\x11\xc6\xe0',    # 5
        b'\x05\x00\xae\x11\xc7\xe0',    # 6
        b'\x01\x00c\x11\x00\x00',       # 7
        b'\x07\x00\xab\x11\xc8\xe0',    # 8
    )

    NODE_CHILDRENS = ((
        # 0
        (0x115F, 1),
    ), (
        # 1
        (0x1161, 2),
        (0x1163, 7),
        (0x11A3, 5),
    ), (
        # 2
        (0x11AE, 3),
        (0xD7CD, 4),
    ), (
        # 3
    ), (
        # 4
    ), (
        # 5
        (0x11AE, 6),
    ), (
        # 6
    ), (
        # 7
        (0x11AB, 8),
    ), (
        # 8
    ))


TREE = Tree()
