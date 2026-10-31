import json
from pathlib import Path
import pandas as pd
from preprocessing.load_metrica import load_game1_norm

MAX_SECONDS = 2700         # الشوط الأول كله
FPS = 5                    # الدالة بتطلع 5 فريم/ثانية
OUT = Path("web/data/match1.json")

df = load_game1_norm()
df = df[df["period_id"] == 1].reset_index(drop=True)

cols = [c for c in df.columns
        if (c.startswith("home_") or c.startswith("away_")) and c.endswith("_x")]
pids = [c[:-2] for c in cols]              # مثلا home_1

players = {p: {"team": p.split("_")[0], "jersey": p.split("_")[1]} for p in pids}

def r(v, off):
    return round(float(v) - off, 2)

frames = []
for i, row in df.iterrows():
    t = i / FPS
    if t > MAX_SECONDS:
        break
    pos = {}
    for p in pids:
        x, y = row[p + "_x"], row[p + "_y"]
        if pd.notna(x) and pd.notna(y):
            pos[p] = [r(x, 52.5), r(y, 34)]
    bx, by = row["ball_x"], row["ball_y"]
    ball = [r(bx, 52.5), r(by, 34)] if pd.notna(bx) and pd.notna(by) else None
    frames.append({"t": round(t, 2), "b": ball, "p": pos})

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"players": players, "frames": frames}))
print(len(frames), "frames,", OUT.stat().st_size // 1024, "KB")