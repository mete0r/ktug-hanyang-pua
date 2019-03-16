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
from io import BytesIO
from io import StringIO
from unittest import TestCase
import json
import sys

from .fixtures import TABLE
from .fixtures import TREE


PY3 = sys.version_info.major == 3
if PY3:
    unicode = str


class TextTableFileFormatTest(TestCase):

    maxDiff = None

    def test_load(self):
        from ktug_hanyang_pua.fileformats.table_text import load_mappings_as_text_table  # noqa
        if PY3:
            ioclass = StringIO
        else:
            ioclass = BytesIO
        input_fp = ioclass('\n'.join(TABLE.MAPPINGS))
        mappings = load_mappings_as_text_table(input_fp)
        mappings = list(mappings)
        self.assertEqual(
            TABLE.MAPPINGLIST,
            tuple(mappings),
        )

    def test_dump(self):
        from ktug_hanyang_pua.fileformats.table_text import dump_mappings_as_text_table  # noqa
        if PY3:
            ioclass = StringIO
        else:
            ioclass = BytesIO
        output_fp = ioclass()
        dump_mappings_as_text_table(TABLE.MAPPINGLIST, output_fp)
        output_fp.seek(0)
        self.assertEqual(
            TABLE.MAPPINGS,
            tuple(line.rstrip() for line in output_fp),
        )


class JsonTableFileFormatTest(TestCase):

    maxDiff = None

    def test_load(self):
        from ktug_hanyang_pua.fileformats.table_json import load_mappings_as_json_table  # noqa

        if PY3:
            ioclass = StringIO
        else:
            ioclass = BytesIO
        input_fp = ioclass()
        json.dump(TABLE.MAPPINGDICTS, input_fp)
        input_fp.seek(0)

        mappings = load_mappings_as_json_table(input_fp)
        mappings = list(mappings)

        self.assertEqual(
            TABLE.MAPPINGLIST,
            tuple(mappings),
        )

    def test_dump(self):
        from ktug_hanyang_pua.fileformats.table_json import dump_mappings_as_json_table  # noqa

        if PY3:
            ioclass = StringIO
        else:
            ioclass = BytesIO
        output_fp = ioclass()
        dump_mappings_as_json_table(TABLE.MAPPINGLIST, output_fp)
        output_fp.seek(0)

        mappings = json.load(output_fp)
        self.assertEqual(
            TABLE.MAPPINGDICTS,
            tuple(mappings),
        )


class BinaryTableFileFormatTest(TestCase):

    maxDiff = None

    def test_dump_and_load(self):
        from ktug_hanyang_pua.fileformats.table_binary import dump_mappings_as_binary_table  # noqa
        from ktug_hanyang_pua.fileformats.table_binary import load_mappings_as_binary_table  # noqa

        output_fp = BytesIO()
        dump_mappings_as_binary_table(TABLE.MAPPINGLIST, output_fp)
        output_fp.seek(0)

        mappings = load_mappings_as_binary_table(output_fp)
        self.assertEqual(
            TABLE.MAPPINGLIST,
            tuple(mappings),
        )


class BinaryTreeFileFormatTest(TestCase):

    maxDiff = None

    def test_dump(self):
        from ktug_hanyang_pua.fileformats.tree_binary import dump_tree_as_binary  # noqa

        output_fp = BytesIO()
        dump_tree_as_binary(TREE.NODELIST, output_fp)

        self.assertEqual(
            b''.join(TREE.NODEPACKS),
            output_fp.getvalue(),
        )


class JsonTreeFileFormatTest(TestCase):

    maxDiff = None

    def test_dump(self):
        from ktug_hanyang_pua.fileformats.tree_json import dump_tree_as_json  # noqa

        if PY3:
            ioclass = StringIO
        else:
            ioclass = BytesIO
        output_fp = ioclass()
        dump_tree_as_json(TREE.NODELIST, output_fp)

        output_fp.seek(0)
        nodes = json.load(output_fp)
        self.assertEqual(
            TREE.NODEDICTS,
            tuple(nodes),
        )
