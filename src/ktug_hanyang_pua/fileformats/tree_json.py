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
import json

from ..formats import NodeDictFormat


def dump_tree_as_json(tree, output_fp):
    nodeDictFormat = NodeDictFormat()
    jsonlist = [nodeDictFormat.format(node) for node in tree]
    json.dump(jsonlist, output_fp, indent=2, sort_keys=True)
    return len(jsonlist)
