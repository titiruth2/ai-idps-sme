"""Isolation Forest detector with dual-model hot-swap retraining."""
import threading
import time

import numpy as np
from sklearn.ensemble import IsolationForest

from .features import FEATURES


def _prep(df):
    """log1p on heavy-tailed size and time features so extremes separate cleanly."""
    X = df[FEATURES].astype(float).copy()
    for col in ("orig_bytes", "resp_bytes", "duration"):
        X[col] = np.log1p(X[col])
    return X.to_numpy()


def _fit(X, contamination, seed=42):
    return IsolationForest(n_estimators=200, contamination=contamination,
                           random_state=seed).fit(X)


class Detector:
    """Model A serves predictions. Model B trains in the background, then replaces A atomically."""

    def __init__(self, contamination=0.05):
        self.contamination = contamination
        self._model = None
        self._lock = threading.Lock()
        self.total_swaps = 0
        self.retraining = False
        self.last_duration = None
        self.last_swap_at = None

    def train(self, df):
        self._model = _fit(_prep(df), self.contamination)
        return self

    def scores(self, df):
        """Anomaly scores. Negative means anomalous; more negative is worse."""
        with self._lock:
            model = self._model
        return model.decision_function(_prep(df))

    def retrain_async(self, df):
        """Train a new model in a thread, then swap it in. Detection keeps running meanwhile."""
        def work():
            self.retraining = True
            start = time.perf_counter()
            new_model = _fit(_prep(df), self.contamination, seed=int(time.time()) % 1000)
            with self._lock:
                self._model = new_model          # atomic reference swap
            self.last_duration = time.perf_counter() - start
            self.total_swaps += 1
            self.last_swap_at = time.time()
            self.retraining = False
        t = threading.Thread(target=work, daemon=True)
        t.start()
        return t

    def status(self):
        return {
            "total_swaps": self.total_swaps,
            "retraining": self.retraining,
            "last_retrain_seconds": None if self.last_duration is None else round(self.last_duration, 3),
            "last_swap_at": self.last_swap_at,
        }
