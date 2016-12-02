##
# Copyright (c) 2014-present MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


import collections

from edgedb.lang.common import lexer

from .errors import WKTSyntaxError


__all__ = ('WKTLexer', )

STATE_KEEP = 0
STATE_BASE = 1

Rule = lexer.Rule
Tag = collections.namedtuple('Tag', 'value has_z has_m')


def make_tag(value):
    has_m = has_z = False
    if value[-1] == 'M':
        has_m = True
        value = value[:-1]
    if value[-1] == 'Z':
        has_z = True
        value = value[:-1]
    return Tag(value, has_z=has_z, has_m=has_m)


class WKTLexer(lexer.Lexer):

    start_state = STATE_BASE

    NL = frozenset('NL')

    # Basic keywords
    common_rules = [
        Rule(token='WS', next_state=STATE_KEEP, regexp=r'[^\S\n]+'),
        Rule(token='NL', next_state=STATE_KEEP, regexp=r'\n'),
        Rule(token='LPARENTHESIS', next_state=STATE_KEEP, regexp=r'\('),
        Rule(token='RPARENTHESIS', next_state=STATE_KEEP, regexp=r'\)'),
        Rule(token='COMMA', next_state=STATE_KEEP, regexp=r','),
        Rule(token='SEMICOLON', next_state=STATE_KEEP, regexp=r';'),
        Rule(
            token='FCONST', next_state=STATE_KEEP, regexp=r'''
                -? (?: \d+\.\d*
                       |
                       \.\d+
                   )
             '''),
        Rule(token='FCONST', next_state=STATE_KEEP, regexp=r'-?\d+'),
        Rule(token='EMPTY', next_state=STATE_KEEP, regexp=r'EMPTY'),
        Rule(token='SRID', next_state=STATE_KEEP, regexp=r'SRID=-?[0-9]+'),
        Rule(token='DIM', next_state=STATE_KEEP, regexp=r'''
            (?:
               POINT | LINESTRING | POLYGON | MULTIPOINT | MULTILINESTRING |
               MULTIPOLYGON | GEOMETRYCOLLECTION | CIRCULARSTRING |
               COMPOUNDCURVE | CURVEPOLYGON | MULTICURVE | MULTISURFACE |
               CURVE | SURFACE | POLYHEDRALSURFACE | TIN | TRIANGLE
            )
            Z?M?
        '''),
    ]

    states = {STATE_BASE: common_rules, }

    def token_from_text(self, rule_token, txt):
        tok = super().token_from_text(rule_token, txt)

        if rule_token == 'SRID':
            tok = tok._replace(value=int(txt[5:]))

        elif rule_token == 'FCONST':
            tok = tok._replace(value=float(txt))

        elif rule_token == 'DIM':
            tag = make_tag(txt)
            tok = tok._replace(value=tag, type=tag.value)

        return tok

    def handle_error(self, txt):
        raise WKTSyntaxError(token=txt, context=self.context())
