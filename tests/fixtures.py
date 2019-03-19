# -*- coding: utf-8 -*-
#
#   ktug-hanyang-pua: KTUG Hanyang PUA table reader/writer
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


_MAPPINGS = (
    'U+E0BC => U+115F U+1161 U+11AE',
    'U+E0BD => U+115F U+1161 U+D7CD',
    'U+E0C6 => U+115F U+11A3',
    'U+E0C7 => U+115F U+11A3 U+11AE',
    'U+E0C8 => U+115F U+1163 U+11AB',
    'U+F86A =>',
)


class Table:

    MAPPINGS = _MAPPINGS

    @property
    def MAPPINGLIST(self):
        from ktug_hanyang_pua.models import Mapping
        return (
            Mapping(
                source=(0xE0BC, ),
                target=(0x115F, 0x1161, 0x11AE),
                comment=None,
            ),
            Mapping(
                source=(0xE0BD, ),
                target=(0x115F, 0x1161, 0xD7CD),
                comment=None,
            ),
            Mapping(
                source=(0xE0C6, ),
                target=(0x115F, 0x11A3),
                comment=None,
            ),
            Mapping(
                source=(0xE0C7, ),
                target=(0x115F, 0x11A3, 0x11AE),
                comment=None,
            ),
            Mapping(
                source=(0xE0C8, ),
                target=(0x115F, 0x1163, 0x11AB),
                comment=None,
            ),
            Mapping(
                source=(0xF86A, ),
                target=(),
                comment=None,
            ),
        )

    @property
    def MAPPINGLIST_SWITCHED(self):
        from ktug_hanyang_pua.models import Mapping
        return (
            Mapping(
                source=(0x115F, 0x1161, 0x11AE),
                target=(0xE0BC, ),
                comment=None,
            ),
            Mapping(
                source=(0x115F, 0x1161, 0xD7CD),
                target=(0xE0BD, ),
                comment=None,
            ),
            Mapping(
                source=(0x115F, 0x11A3),
                target=(0xE0C6, ),
                comment=None,
            ),
            Mapping(
                source=(0x115F, 0x11A3, 0x11AE),
                target=(0xE0C7, ),
                comment=None,
            ),
            Mapping(
                source=(0x115F, 0x1163, 0x11AB),
                target=(0xE0C8, ),
                comment=None,
            ),
            Mapping(
                source=(),
                target=(0xF86A, ),
                comment=None,
            ),
        )

    MAPPINGPACKS = (
        b'\xbc\xe0\x03\x00',            # 0
        b'\xbd\xe0\x03\x00',            # 1
        b'\xc6\xe0\x02\x00',            # 2
        b'\xc7\xe0\x03\x00',            # 3
        b'\xc8\xe0\x03\x00',            # 4
        b'j\xf8\x00\x00',               # 5
    )

    @property
    def MAPPINGDICTS(self):
        return ({
            'source': u'\ue0bc',
            'target': u'\u115f\u1161\u11ae',
            'comment': None,
        }, {
            'source': u'\ue0bd',
            'target': u'\u115f\u1161\ud7cd',
            'comment': None,
        }, {
            'source': u'\ue0c6',
            'target': u'\u115f\u11a3',
            'comment': None,
        }, {
            'source': u'\ue0c7',
            'target': u'\u115f\u11a3\u11ae',
            'comment': None,
        }, {
            'source': u'\ue0c8',
            'target': u'\u115f\u1163\u11ab',
            'comment': None,
        }, {
            'source': u'\uf86a',
            'target': u'',
            'comment': None,
        })

    @property
    def MAPPINGDICTS_WITHOUT_COMMENT(self):
        return ({
            'source': u'\ue0bc',
            'target': u'\u115f\u1161\u11ae',
        }, {
            'source': u'\ue0bd',
            'target': u'\u115f\u1161\ud7cd',
        }, {
            'source': u'\ue0c6',
            'target': u'\u115f\u11a3',
        }, {
            'source': u'\ue0c7',
            'target': u'\u115f\u11a3\u11ae',
        }, {
            'source': u'\ue0c8',
            'target': u'\u115f\u1163\u11ab',
        }, {
            'source': u'\uf86a',
            'target': u'',
        })


class Tree:

    MAPPINGS = _MAPPINGS

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

    @property
    def NODEDICTS(self):
        return ({
            # 0
            'parent': -1,
            'source': None,
            'target': 0xF86A,
        }, {
            # 1
            'parent': 0,
            'source': 0x115F,
            'target': None,
        }, {
            # 2
            'parent': 1,
            'source': 0x1161,
            'target': None,
        }, {
            # 3
            'parent': 2,
            'source': 0x11AE,
            'target': 0xE0BC,
        }, {
            # 4
            'parent': 2,
            'source': 0xD7CD,
            'target': 0xE0BD,
        }, {
            # 5
            'parent': 1,
            'source': 0x11A3,
            'target': 0xE0C6,
        }, {
            # 6
            'parent': 5,
            'source': 0x11AE,
            'target': 0xE0C7,
        }, {
            # 7
            'parent': 1,
            'source': 0x1163,
            'target': None,
        }, {
            # 8
            'parent': 7,
            'source': 0x11AB,
            'target': 0xE0C8,
        })

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
TABLE = Table()
