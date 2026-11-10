"""Slim Uber pickups demo for Render Free (512 MB)."""

from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).parent / "data" / "uber_pickups_sample.csv"
DATE_TIME = "date/time"

st.set_page_config(page_title="NYC Uber sample", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    data.rename(str.lower, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data


data = load_data()

row1_1, row1_2 = st.columns((2, 3))
with row1_1:
    st.title("NYC Uber pickups (sample)")
    hour_selected = st.slider("Select hour of pickup", 0, 23)
with row1_2:
    st.write(
        "Examining how Uber pickups vary by hour in a small NYC sample. "
        "This teaching app ships a local 5k-row CSV so it fits Render Free (512 MB)."
    )

filtered = data[data[DATE_TIME].dt.hour == hour_selected]

st.subheader(f"Map of pickups at {hour_selected}:00")
st.map(filtered[["lat", "lon"]])

st.subheader("Pickups by minute")
hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
hist_df = pd.DataFrame({"minute": list(range(60)), "pickups": hist})
chart = (
    alt.Chart(hist_df)
    .mark_area(interpolate="basis")
    .encode(x="minute:Q", y="pickups:Q")
    .properties(height=280)
)
st.altair_chart(chart, use_container_width=True)

st.caption(f"Showing {len(filtered)} of {len(data)} local sample rows.")
