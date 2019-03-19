# -*- coding: utf-8 -*-
#
#   ktug-hanyang-pua: KTUG Hanyang PUA table reader/writer
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
from .fixtures import TABLE


class LineFormatTest(TestCase):

    def make_one(self):
        from ktug_hanyang_pua.formats import LineFormat
        return LineFormat()

    def test_mapping(self):
        from ktug_hanyang_pua.models import Mapping

        lineFormat = self.make_one()
        line = 'U+1107 U+1107 U+110B => U+112C'

        parsed = lineFormat.parse(line)
        self.assertEqual(
            Mapping((0x1107, 0x1107, 0x110B), (0x112C,), None),
            parsed,
        )

        formatted = lineFormat.format(parsed)
        self.assertEqual(
            line,
            formatted,
        )

        line = 'U+F86A =>'

        parsed = lineFormat.parse(line)
        self.assertEqual(
            Mapping((0xF86A, ), (), None),
            parsed,
        )

        formatted = lineFormat.format(parsed)
        self.assertEqual(
            line,
            formatted,
        )

    def test_mapping_with_comment(self):
        from ktug_hanyang_pua.models import Mapping
        from ktug_hanyang_pua.models import Comment

        lineFormat = self.make_one()

        line = 'U+11BC U+11A8 U+11A8 => U+11ED %%% legacy encoding'

        parsed = lineFormat.parse(line)
        self.assertEqual(
            Mapping(
                (0x11BC, 0x11A8, 0x11A8),
                (0x11ED,),
                Comment(' legacy encoding')
            ),
            parsed
        )

        formatted = lineFormat.format(parsed)
        self.assertEqual(
            line,
            formatted,
        )

    def test_empty(self):
        from ktug_hanyang_pua.models import Empty
        lineFormat = self.make_one()

        line = ''

        parsed = lineFormat.parse(line)
        self.assertEqual(
            Empty(),
            parsed,
        )

        formatted = lineFormat.format(parsed)
        self.assertEqual(
            line,
            formatted,
        )

    def test_parse_comment(self):
        from ktug_hanyang_pua.models import Comment
        lineFormat = self.make_one()

        line = '%%%'

        parsed = lineFormat.parse(line)
        self.assertEqual(
            Comment(''),
            parsed,
        )

        formatted = lineFormat.format(parsed)
        self.assertEqual(
            line,
            formatted,
        )

        line = '%%% Trailing Consonants'

        parsed = lineFormat.parse(line)
        self.assertEqual(
            Comment(' Trailing Consonants'),
            parsed,
        )

        formatted = lineFormat.format(parsed)
        self.assertEqual(
            line,
            formatted,
        )

        line = '%%%\t2004/09/17  initial release'
        parsed = lineFormat.parse(line)
        self.assertEqual(
            Comment('\t2004/09/17  initial release'),
            parsed,
        )

        formatted = lineFormat.format(parsed)
        self.assertEqual(
            line,
            formatted,
        )

    def test_format_typeerror(self):
        lineFormat = self.make_one()
        try:
            lineFormat.format(None)
        except TypeError:
            pass
        else:
            assert False, 'TypeError not occurred'

    def test_repr(self):
        lineFormat = self.make_one()
        self.assertEqual('LineFormat()', repr(lineFormat))


class IterableFormatTest(TestCase):

    def make_one(self):
        from ktug_hanyang_pua.formats import IterableFormat

        class IdentityFormat:

            format = parse = lambda self, x: x

            def __repr__(self):
                return 'identity'

        return IterableFormat(IdentityFormat())

    def test_repr(self):
        iterableFormat = self.make_one()
        self.assertEqual(
            'IterableFormat(identity)',
            repr(iterableFormat),
        )

    def test_format(self):
        iterableFormat = self.make_one()
        iterable = [1, 2, 3]
        self.assertEqual(
            (1, 2, 3),
            tuple(iterableFormat.format(iterable)),
        )
        self.assertEqual(
            (1, 2, 3),
            tuple(iterableFormat.parse(iter(iterable))),
        )


class MappingDictFormat(TestCase):

    def make_one(self):
        from ktug_hanyang_pua.formats import MappingDictFormat
        return MappingDictFormat()

    def test_format_and_parse(self):
        from ktug_hanyang_pua.models import Mapping
        dictFormat = self.make_one()

        for index, mapping in enumerate(TABLE.MAPPINGLIST):
            mapping = Mapping(
                source=mapping.source[0],
                target=mapping.target,
                comment=mapping.comment,
            )
            d = dictFormat.format(mapping)
            self.assertEqual(
                TABLE.MAPPINGDICTS[index],
                d,
            )

            parsed = dictFormat.parse(d)
            parsed = Mapping(
                source=tuple([parsed.source]),
                target=tuple(parsed.target),
                comment=parsed.comment,
            )
            self.assertEqual(
                TABLE.MAPPINGLIST[index],
                parsed,
            )

    def test_format_and_parse_without_comment(self):
        from ktug_hanyang_pua.models import Mapping
        from ktug_hanyang_pua.formats import MappingDictFormat
        dictFormat = MappingDictFormat(comment=False)

        for index, mapping in enumerate(TABLE.MAPPINGLIST):
            mapping = Mapping(
                source=mapping.source[0],
                target=mapping.target,
                comment=mapping.comment,
            )
            d = dictFormat.format(mapping)
            self.assertEqual(
                TABLE.MAPPINGDICTS_WITHOUT_COMMENT[index],
                d,
            )

            parsed = dictFormat.parse(d)
            parsed = Mapping(
                source=tuple([parsed.source]),
                target=tuple(parsed.target),
                comment=parsed.comment,
            )
            self.assertEqual(
                TABLE.MAPPINGLIST[index],
                parsed,
            )


class NodeDictFormatTest(TestCase):

    def make_one(self):
        from ktug_hanyang_pua.formats import NodeDictFormat
        return NodeDictFormat()

    def test_format(self):
        nodeFormat = self.make_one()

        for index, node in enumerate(TREE.NODELIST):
            binary = nodeFormat.format(node)
            self.assertEqual(
                TREE.NODEDICTS[index],
                binary
            )

            parsed = nodeFormat.parse(binary)
            self.assertEqual(
                TREE.NODELIST[index],
                parsed,
            )


class NodePackFormatTest(TestCase):

    def make_one(self):
        from ktug_hanyang_pua.formats import NodePackFormat
        return NodePackFormat()

    def test_format(self):
        nodeFormat = self.make_one()

        for index, node in enumerate(TREE.NODELIST):
            binary = nodeFormat.format(node)
            self.assertEqual(
                TREE.NODEPACKS[index],
                binary
            )

            parsed = nodeFormat.parse(binary)
            self.assertEqual(
                TREE.NODELIST[index],
                parsed,
            )
