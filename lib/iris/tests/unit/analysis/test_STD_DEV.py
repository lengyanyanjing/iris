# (C) British Crown Copyright 2014 - 2017, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.
"""Unit tests for the :data:`iris.analysis.STD_DEV` aggregator."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

import numpy as np

from iris._lazy_data import as_concrete_data, as_lazy_data
from iris.analysis import STD_DEV


class Test_lazy_aggregate(tests.IrisTest):
    def test_mdtol(self):
        na = np.nan
        array = np.array([[1., 2., 1., 2.],
                          [1., 2., 3., na],
                          [1., 2., na, na]])
        array = as_lazy_data(array)
        var = STD_DEV.lazy_aggregate(array, axis=1, mdtol=0.3)
        masked_result = as_concrete_data(var, nans_replacement=np.ma.masked)
        masked_expected = np.ma.masked_array([0.57735, 1., 0.707107],
                                             mask=[0, 0, 1])
        self.assertMaskedArrayAlmostEqual(masked_result, masked_expected)

    def test_ddof_one(self):
        array = as_lazy_data(np.arange(8))
        var = STD_DEV.lazy_aggregate(array, axis=0, ddof=1)
        result = as_concrete_data(var)
        self.assertArrayAlmostEqual(result, np.array(2.449489))

    def test_ddof_zero(self):
        array = as_lazy_data(np.arange(8))
        var = STD_DEV.lazy_aggregate(array, axis=0, ddof=0)
        result = as_concrete_data(var)
        self.assertArrayAlmostEqual(result, np.array(2.291287))


class Test_name(tests.IrisTest):
    def test(self):
        self.assertEqual(STD_DEV.name(), 'standard_deviation')


class Test_aggregate_shape(tests.IrisTest):
    def test(self):
        shape = ()
        kwargs = dict()
        self.assertTupleEqual(STD_DEV.aggregate_shape(**kwargs), shape)
        kwargs = dict(forfar=5, fife=4)
        self.assertTupleEqual(STD_DEV.aggregate_shape(**kwargs), shape)


if __name__ == '__main__':
    tests.main()
