# -*- coding: utf-8 -*-

"""Tests of misc type utility functions."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os.path as op

import numpy as np
from numpy.testing import assert_array_equal as ae
from pytest import raises, mark

from ..utils import (Bunch, _is_integer, captured_output,
                     _load_arrays, _save_arrays,
                     )


#------------------------------------------------------------------------------
# Tests
#------------------------------------------------------------------------------

def test_bunch():
    obj = Bunch()
    obj['a'] = 1
    assert obj.a == 1
    obj.b = 2
    assert obj['b'] == 2


def test_integer():
    assert _is_integer(3)
    assert _is_integer(np.arange(1)[0])
    assert not _is_integer(3.)


def test_captured_output():
    with captured_output() as (out, err):
        print('Hello world!')
    assert out.getvalue().strip() == 'Hello world!'


@mark.parametrize('n', [20, 0])
def test_load_save_arrays(tempdir, n):
    path = op.join(tempdir, 'test.npy')
    # Random arrays.
    arrays = []
    for i in range(n):
        size = np.random.randint(low=3, high=50)
        assert size > 0
        arr = np.random.rand(size, 3).astype(np.float32)
        arrays.append(arr)
    _save_arrays(path, arrays)

    arrays_loaded = _load_arrays(path)

    assert len(arrays) == len(arrays_loaded)
    for arr, arr_loaded in zip(arrays, arrays_loaded):
        assert arr.shape == arr_loaded.shape
        assert arr.dtype == arr_loaded.dtype
        ae(arr, arr_loaded)
