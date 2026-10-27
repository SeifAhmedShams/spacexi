import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mplsoccer import Pitch
from preprocessing.load_metrica import load_game1_norm
from spatial_models.voronoi import voronoi_control

st.set_page_config(page_title="SpaceXI", layout="wide")
st.title("SpaceXI - Match Replay")


@st.cache_data
def get_data():
    return load_game1_norm()


df = get_data()
period = st.radio("Period", sorted(df["period_id"].unique()), horizontal=True)
show_vor = st.checkbox("Show Voronoi", value=True)
g = df[df["period_id"] == period].reset_index(drop=True)
i = st.slider("Frame", 0, len(g) - 1, 0)
row = g.iloc[i]

pitch = Pitch(pitch_type="custom", pitch_length=105, pitch_width=68, line_color="#555555")
fig, ax = pitch.draw(figsize=(10, 6.5))
title_extra = ""
if show_vor:
    grid = voronoi_control(row).astype(int)
    ax.imshow(grid, extent=(0, 105, 0, 68), origin="lower", aspect="auto",
              cmap=ListedColormap(["tab:blue", "tab:red"]), alpha=0.2, zorder=1)
    title_extra = f" | Home space: {grid.mean():.0%}"
for side, color in [("home", "tab:red"), ("away", "tab:blue")]:
    xs = [row[c] for c in g.columns if c.startswith(side + "_") and c.endswith("_x")]
    ys = [row[c] for c in g.columns if c.startswith(side + "_") and c.endswith("_y")]
    ax.scatter(xs, ys, c=color, s=120, edgecolors="white", zorder=3)
ax.scatter([row["ball_x"]], [row["ball_y"]], c="black", s=50, zorder=4)
sec = row["timestamp"].total_seconds()
ax.set_title(f"Period {int(period)} | {int(sec // 60):02d}:{int(sec % 60):02d}{title_extra}")
st.pyplot(fig)
plt.close(fig)
