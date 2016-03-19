# -*- coding: utf-8 -*-

"""Test launcher."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os.path as op

import numpy as np
from numpy.testing import assert_array_equal as ae
from pytest import fixture

from ..launch import detect, cluster
from ..datasets import download_test_data
from ..kwik.creator import create_kwik
from ..kwik.mock import mock_prm
from ..kwik.model import KwikModel


#------------------------------------------------------------------------------
# Fixtures
#------------------------------------------------------------------------------

@fixture
def model(tempdir):
    # Create empty kwik from mock PRM, PRB, and test dat file.
    dat_path = download_test_data('test-32ch-10s.dat')
    kwik_path = op.join(tempdir, 'test-32ch-10s.kwik')
    prm = mock_prm(dat_path)
    create_kwik(prm=prm, kwik_path=kwik_path)

    model = KwikModel(kwik_path)
    return model


#------------------------------------------------------------------------------
# Tests
#------------------------------------------------------------------------------

def test_detect(model):
    out = detect(model, interval=(0., 5.))
    model.describe()
