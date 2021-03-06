# pytest --cov-report term-missing --cov=deepSIP test/

# imports -- standard
import os
import pandas as pd
import pytest

# imports -- custom
from deepSIP import deepSIP
from deepSIP import utils

# globals for testing
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SPECTRA_FILE = os.path.join(os.path.dirname(TEST_DIR), 'example', 'spectra.csv')
DF = pd.read_csv(SPECTRA_FILE)
DF['filename'] = DF['filename'].apply(lambda f: \
                                      os.path.join(os.path.dirname(TEST_DIR),
                                      'example', 'spectra', f))

def test_init():
    dsn = deepSIP()
    assert dsn.seed == 100
    assert dsn.models.shape[0] == 3 # 3 models
    for mod in ['Domain', 'Phase', 'dm15']:
        # testing will happen on a cpu, so will be WrappedModel of DropoutCNN
        assert isinstance(dsn.models.loc[mod, 'net'], utils.WrappedModel)
    assert isinstance(dsn.models.loc['Domain', 'Yscaler'], utils.VoidScaler)
    assert isinstance(dsn.models.loc['Phase', 'Yscaler'], utils.LinearScaler)
    assert isinstance(dsn.models.loc['dm15', 'Yscaler'], utils.LinearScaler)

def test_predict():
    dsn = deepSIP()
    with pytest.raises(TypeError):
        results = dsn.predict(5)
    ## "code is too big" issue
    ## e.g. https://github.com/pytorch/pytorch/issues/32507
    ## just don't do the following tests
    ## tests pass locally as of 4/16/2020
    #results = dsn.predict(DF, mcnum = 1, status = True)
    #assert type(results) == pd.DataFrame
    #assert results['Domain'].max() <= 1.
    #assert results['Domain'].min() >= 0.
    #assert results['Phase'].max() > 1
    #assert results['dm15'].max() > 1
