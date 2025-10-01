import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from lr_crispdm_streamlit import model
import numpy as np


def test_generate_and_fit():
    X, y = model.generate_data(a=3.0, b=0.5, n=50, noise=0.1, seed=1)
    res = model.fit_linear_regression(X, y, X_test=X, y_test=y)
    # With very low noise estimated slope should be close to 3.0
    assert abs(res['coef'] - 3.0) < 0.2
