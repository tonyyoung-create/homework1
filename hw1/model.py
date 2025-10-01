import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def generate_data(a=2.0, b=1.0, n=100, noise=1.0, seed=42):
    rng = np.random.RandomState(int(seed))
    X = rng.uniform(-10, 10, size=(n, 1))
    y = a * X + b + rng.normal(scale=noise, size=(n, 1))
    return X, y


def fit_linear_regression(X_train, y_train, X_test=None, y_test=None, fit_intercept=True):
    model = LinearRegression(fit_intercept=fit_intercept)
    model.fit(X_train, y_train.ravel())
    coef = float(model.coef_[0])
    intercept = float(model.intercept_)
    train_pred = model.predict(X_train)
    train_mse = float(mean_squared_error(y_train, train_pred))
    test_mse = None
    test_r2 = None
    if X_test is not None and y_test is not None and len(X_test) > 0:
        pred = model.predict(X_test)
        test_mse = float(mean_squared_error(y_test, pred))
        test_r2 = float(r2_score(y_test, pred))

    return {
        'model': model,
        'coef': coef,
        'intercept': intercept,
        'train_mse': train_mse,
        'test_mse': test_mse if test_mse is not None else float('nan'),
        'test_r2': test_r2 if test_r2 is not None else float('nan'),
    }
