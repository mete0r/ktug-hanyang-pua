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
from __future__ import unicode_literals
from argparse import ArgumentParser
import gettext
import io
import json
import logging
import os.path
import struct
import sys

# PYTHON_ARGCOMPLETE_OK
try:
    import argcomplete
except ImportError:
    argcomplete = None

from . import __version__
from .formats import IterableFormat
from .formats import LineFormat
from .formats import MappingDictFormat
from .formats import MappingPackFormat
from .formats import NodePackFormat
from .formats import NodeDictFormat
from .models import Mapping
from .table import split_table
from .tree import build_tree

PY3 = sys.version_info.major == 3
logger = logging.getLogger(__name__)

locale_dir = os.path.join(os.path.dirname(__file__), 'locale')
t = gettext.translation('ktug-hanyang-pua', locale_dir, fallback=True)
if PY3:
    _ = t.gettext
else:
    _ = t.ugettext


def main():
    gettext.gettext = t.gettext
    parser = main_argparse()
    if argcomplete:
        argcomplete.autocomplete(parser)
    args = parser.parse_args()
    configureLogging(args.verbose)
    logger.info('args: %s', args)

    lineFormat = LineFormat()
    inputFormat = IterableFormat(lineFormat)
    mappingPackFormat = MappingPackFormat()
    mappingDictFormat = MappingDictFormat()
    nodePackFormat = NodePackFormat()
    nodeDictFormat = NodeDictFormat()

    if args.FILE is not None:
        input_fp = io.open(args.FILE, 'r', encoding='utf-8')
    else:
        input_fp = sys.stdin
    with input_fp:
        parsed = (
            line for line in inputFormat.parse(input_fp)
        )

        if args.output_file is not None:
            output_fp = io.open(args.output_file, 'w', encoding='utf-8')
        else:
            output_fp = sys.stdout
        with output_fp:
            if args.data_model == 'table':
                if args.output_format == 'binary':
                    if output_fp.isatty():
                        logger.error(
                            _('Rejecting to output binary to a terminal.')
                        )
                        raise SystemExit(1)
                    if PY3:
                        output_fp = output_fp.buffer
                    mappings = (
                        line for line in parsed
                        if isinstance(line, Mapping)
                    )
                    if args.switch:
                        mappings = (
                            Mapping(
                                source=m.target,
                                target=m.source,
                                comment=m.comment
                            )
                            for m in mappings
                        )
                    mappings = (
                        Mapping(
                            source=m.source[0],
                            target=m.target,
                            comment=m.comment,
                        )
                        for m in mappings
                    )
                    mappings = split_table(mappings)
                    if args.output_file is None:
                        logger.error(
                            _('table binary format requires filename.')
                        )
                        raise SystemExit(1)
                    target_filename = args.output_file + '.target'
                    with io.open(target_filename, 'wb') as target_fp:
                        for n, mapping in enumerate(mappings, 1):
                            mapping, target, comment = mapping
                            byteseq = mappingPackFormat.format(mapping)
                            output_fp.write(byteseq)
                            targetfmt = '<{}H'.format(len(target))
                            target = struct.pack(targetfmt, *target)
                            target_fp.write(target)
                    logger.info(
                        _('%s mappings have been written.'), n
                    )
                elif args.output_format == 'json':
                    mappings = (
                        line for line in parsed
                        if isinstance(line, Mapping)
                    )
                    mappings = (
                        Mapping(
                            source=m.source[0],
                            target=m.target,
                            comment=m.comment,
                        )
                        for m in mappings
                    )
                    mappings = [
                        mappingDictFormat.format(mapping)
                        for mapping in mappings
                    ]
                    json.dump(mappings, output_fp, indent=2, sort_keys=True)
                    logger.info(
                        _('%s mappings have been written.'), len(mappings)
                    )
                elif args.output_format == 'text':
                    for n, line in enumerate(parsed, 1):
                        lineFormatted = lineFormat.format(line)
                        output_fp.write(lineFormatted)
                        output_fp.write('\n')
                    logger.info(
                        _('%s lines have been written.'), n
                    )
                else:
                    logger.error(
                        _('Not supported format for data model %s: %s'),
                        args.data_model,
                        args.output_format,
                    )
                    raise SystemExit(1)
            elif args.data_model == 'tree':
                mappings = (
                    line for line in parsed
                    if isinstance(line, Mapping)
                )
                # tree 모형은 사상 방향이 반대
                if not args.switch:
                    mappings = (
                        Mapping(
                            source=m.target,
                            target=m.source,
                            comment=m.comment
                        )
                        for m in mappings
                    )
                mappings = (
                    Mapping(
                        source=m.source,
                        target=m.target[0],
                        comment=m.comment,
                    )
                    for m in mappings
                )
                tree, __ = build_tree(mappings)

                if args.output_format == 'binary':
                    if output_fp.isatty():
                        logger.error(
                            _('Rejecting to output binary to a terminal.')
                        )
                        raise SystemExit(1)
                    if PY3:
                        output_fp = output_fp.buffer
                    for n, node in enumerate(tree, 1):
                        node = nodePackFormat.format(node)
                        output_fp.write(node)
                    logger.info(
                        _('%s nodes have been written.'), n
                    )
                elif args.output_format == 'json':
                    jsonlist = [nodeDictFormat.format(node) for node in tree]
                    json.dump(jsonlist, output_fp, indent=2, sort_keys=True)
                    logger.info(
                        _('%s nodes have been written.'), len(jsonlist)
                    )
                else:
                    logger.error(
                        _('Not supported format for data model %s: %s'),
                        args.data_model,
                        args.output_format,
                    )
                    raise SystemExit(1)


def main_argparse():
    parser = ArgumentParser()
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__),
        help=_('output version information and exit')
    )
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        help=_('increase verbosity')
    )
    parser.add_argument(
        '-o', '--output-file',
        action='store',
        help=_('output file')
    )
    parser.add_argument(
        '-m', '--data-model',
        choices=('table', 'tree'),
        default='table',
        help=_('output data model'),
    )
    parser.add_argument(
        '-F', '--output-format',
        action='store',
        choices=('text', 'binary', 'json'),
        default='text',
        help=_('output data format'),
    )
    parser.add_argument(
        '-S', '--switch',
        action='store_true',
        help=_('Switch source/targets in input mappings'),
    )
    parser.add_argument(
        'FILE',
        action='store',
        nargs='?',
        default=None,
        help=_('input file'),
    )
    return parser


def configureLogging(verbosity):
    verbosity = verbosity or 0
    if verbosity == 1:
        level = logging.INFO
    elif verbosity > 1:
        level = logging.DEBUG
    else:
        level = logging.WARNING
    try:
        import coloredlogs
    except ImportError:
        logging.basicConfig(level=level)
    else:
        coloredlogs.install(level)
