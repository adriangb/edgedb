##
# Copyright (c) 2008-present MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


import unittest

from edgedb.lang.common.gis.proto import geometry, point, curve, surface


class GisTests(unittest.TestCase):
    def test_common_gis_basic_point(self):
        point.Point('POINT(1.0 2.0)')
        point.Point('POINTZ(1.0 2.0 3.0)')
        point.Point('POINTZM(1.0 2.0 3.0 4.0)')

        with self.assertRaises(geometry.GeometryError):
            point.Point('POINT(1 2 3 4)')

        with self.assertRaises(geometry.GeometryError):
            point.Point('POINTZ(1 2 3 4)')

        with self.assertRaises(geometry.GeometryError):
            point.Point('POINTZM(1 2 3)')

        with self.assertRaises(geometry.GeometryError):
            point.Point('POINT(1)')

        with self.assertRaises(geometry.GeometryError):
            point.Point(x=1)

        pt = point.Point()
        assert pt.is_empty()

    def test_common_gis_basic_linestring(self):
        ls = curve.LineString('LINESTRING(1 1, 2 2)')
        assert len(ls) == 2
        assert isinstance(ls[0], point.Point)
        assert ls[0].x == 1 and ls[0].y == 1 and ls[1].x == 2 and ls[1].y == 2

        ls = curve.LineString([(1, 1), (2, 2)])
        assert len(ls) == 2
        assert isinstance(ls[0], point.Point)
        assert ls[0].x == 1 and ls[0].y == 1 and ls[1].x == 2 and ls[1].y == 2

        # One-point linestrings are invalid
        with self.assertRaises(geometry.GeometryError):
            curve.LineString([(1, 1)])

        with self.assertRaises(geometry.GeometryError):
            ls = curve.LineString('LINESTRING(1 1)')

        # Empty ones are OK
        ls = curve.LineString()
        assert ls.is_empty()

        ls = curve.LineString('LINESTRING EMPTY')
        assert ls.is_empty()

        with self.assertRaises(geometry.GeometryError):
            curve.LineString('LINESTRING(1 1, 2 2 2)')

        with self.assertRaises(geometry.GeometryError):
            curve.LineString(
                [point.Point(x=1, y=1, m=1), point.Point(x=1, y=1, z=1)])

        with self.assertRaises(geometry.GeometryError):
            curve.LineString('LINESTRINGZ(1 1, 2 2)')

        ls = curve.LineString([(1, 1, 1), point.Point(x=1, y=1, m=1)])
        assert 'm' in ls[0].dimensions
        assert 'z' not in ls[0].dimensions

    def test_common_gis_basic_polygon(self):
        poly = surface.Polygon('POLYGON((1 1, 5 1, 5 5, 1 5, 1 1))')

        assert len(poly) == 1
