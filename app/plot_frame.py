import matplotlib
matplotlib.use("Agg")
from mplsoccer import Pitch
from preprocessing.load_metrica import load_game1_norm


def plot_frame(df, i, path):
    row = df.iloc[i]
    pitch = Pitch(pitch_type="custom", pitch_length=105, pitch_width=68, line_color="#555555")
    fig, ax = pitch.draw(figsize=(10, 6.5))
    for side, color in [("home", "tab:red"), ("away", "tab:blue")]:
        xs = [row[c] for c in df.columns if c.startswith(side + "_") and c.endswith("_x")]
        ys = [row[c] for c in df.columns if c.startswith(side + "_") and c.endswith("_y")]
        ax.scatter(xs, ys, c=color, s=120, edgecolors="white", zorder=3)
    ax.scatter([row["ball_x"]], [row["ball_y"]], c="black", s=50, zorder=4)
    ax.set_title(f"period {int(row['period_id'])} | t = {row['timestamp']}")
    fig.savefig(path, dpi=120, bbox_inches="tight")


if __name__ == "__main__":
    df = load_game1_norm()
    i = int(df["ball_valid"].values.nonzero()[0][3000])
    plot_frame(df, i, "data/frame_test.png")
