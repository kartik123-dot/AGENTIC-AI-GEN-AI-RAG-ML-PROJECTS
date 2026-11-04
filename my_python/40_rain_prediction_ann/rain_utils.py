"""Shared preprocessing for the rain-prediction ANN.

Used by the training notebook AND the Streamlit app, so training and
prediction always transform data in exactly the same way.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

CAT_COLS = ["Location", "WindGustDir", "WindDir9am", "WindDir3pm", "RainToday"]
NUM_COLS = [
    "MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine",
    "WindGustSpeed", "WindSpeed9am", "WindSpeed3pm", "Humidity9am",
    "Humidity3pm", "Pressure9am", "Pressure3pm", "Cloud9am", "Cloud3pm",
    "Temp9am", "Temp3pm",
]
FEATURE_COLS = [
    "Location", "MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine",
    "WindGustDir", "WindGustSpeed", "WindDir9am", "WindDir3pm",
    "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm",
    "Pressure9am", "Pressure3pm", "Cloud9am", "Cloud3pm", "Temp9am",
    "Temp3pm", "RainToday", "year", "month_sin", "month_cos",
    "day_sin", "day_cos",
]


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """Adds year plus cyclic sine/cosine encodings of month and day."""
    df = df.copy()
    d = pd.to_datetime(df["Date"])
    df["year"] = d.dt.year
    month, day = d.dt.month, d.dt.day
    df["month_sin"] = np.sin(2 * np.pi * month / 12)
    df["month_cos"] = np.cos(2 * np.pi * month / 12)
    df["day_sin"] = np.sin(2 * np.pi * day / 31)
    df["day_cos"] = np.cos(2 * np.pi * day / 31)
    return df


class RainPreprocessor:
    """Fill missing values -> label-encode -> date features -> standardise."""

    def fit(self, df: pd.DataFrame):
        self.medians = {c: float(df[c].median()) for c in NUM_COLS}
        self.modes = {c: df[c].mode()[0] for c in CAT_COLS}
        self.classes = {c: sorted(df[c].dropna().unique().tolist()) for c in CAT_COLS}
        self.num_ranges = {
            c: (float(df[c].quantile(0.001)), float(df[c].quantile(0.999)))
            for c in NUM_COLS
        }
        self.scaler = StandardScaler()
        self.scaler.fit(self._encode(df))
        return self

    def _encode(self, df: pd.DataFrame) -> pd.DataFrame:
        df = add_date_features(df)
        for c in NUM_COLS:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(self.medians[c])
        for c in CAT_COLS:
            col = df[c].astype(object).where(df[c].isin(self.classes[c]), self.modes[c])
            col = col.fillna(self.modes[c])
            df[c] = col.map({v: i for i, v in enumerate(self.classes[c])}).astype(float)
        return df[FEATURE_COLS].astype(float)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        enc = self._encode(df)
        return pd.DataFrame(
            self.scaler.transform(enc), columns=FEATURE_COLS, index=df.index
        )


# Outlier limits (in standardised units) taken from the original notebook.
OUTLIER_RULES = {
    "MinTemp": (-2.3, 2.3), "MaxTemp": (-2.0, 2.3), "Rainfall": (None, 4.5),
    "Evaporation": (None, 2.8), "Sunshine": (None, 2.1),
    "WindGustSpeed": (-4, 4), "WindSpeed9am": (None, 4),
    "WindSpeed3pm": (None, 2.5), "Humidity9am": (-3, None),
    "Humidity3pm": (-2.2, None), "Pressure9am": (-2.7, 2),
    "Pressure3pm": (-2.7, 2), "Cloud9am": (None, 1.8), "Cloud3pm": (None, 2),
    "Temp9am": (-2, 2.3), "Temp3pm": (-2, 2.3),
}


def outlier_mask(features: pd.DataFrame) -> pd.Series:
    keep = pd.Series(True, index=features.index)
    for col, (lo, hi) in OUTLIER_RULES.items():
        if lo is not None:
            keep &= features[col] > lo
        if hi is not None:
            keep &= features[col] < hi
    return keep
