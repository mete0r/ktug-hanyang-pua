# -*- coding: utf-8 -*-
#
#   ktug-hanyang-pua: KTUG HanYang PUA conversion table reader
#   Copyright (C) 2015-2019 mete0r <mete0r@sarangbang.or.kr>
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
from unittest import TestCase

from .fixtures import TREE


class TreeTest(TestCase):

    maxDiff = None

    def test_build_tree(self):
        from ktug_hanyang_pua.models import Mapping
        from ktug_hanyang_pua.formats import IterableFormat
        from ktug_hanyang_pua.formats import LineFormat
        from ktug_hanyang_pua.tree import build_tree

        mappingsFormat = IterableFormat(LineFormat())
        mappings = mappingsFormat.parse(TREE.MAPPINGS)
        mappings = (
            Mapping(
                source=m.target,
                target=m.source[0],
                comment=None,
            )
            for m in mappings
        )

        nodelist, node_childrens = build_tree(mappings)

        self.assertEqual(
            TREE.NODELIST,
            nodelist
        )
        self.assertEqual(
            TREE.NODE_CHILDRENS,
            node_childrens
        )

    def test_build_tree_children_list(self):
        from ktug_hanyang_pua.tree import build_tree_children_list

        node_childrens = build_tree_children_list(TREE.NODELIST)

        self.assertEqual(
            TREE.NODE_CHILDRENS,
            node_childrens,
        )
