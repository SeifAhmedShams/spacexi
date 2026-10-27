from kloppy import metrica
from kloppy.domain import MetricPitchDimensions, Dimension

PITCH = MetricPitchDimensions(
    x_dim=Dimension(0, 105), y_dim=Dimension(0, 68),
    pitch_length=105, pitch_width=68, standardized=False,
)

def fix_ball(df, fps=5, max_gap_sec=1.0):
    """Interpolate short ball gaps; flag the rest as invalid."""
    m = df['ball_x'].isna()
    run_id = (m != m.shift()).cumsum()
    run_len = m.groupby(run_id).transform('size')
    short = m & (run_len <= int(max_gap_sec * fps))
    for c in ['ball_x', 'ball_y']:
        filled = df[c].interpolate(limit_area='inside')
        df.loc[short, c] = filled[short]
    df['ball_interpolated'] = short
    df['ball_valid'] = df['ball_x'].notna()
    return df

def load_game1(sample_rate=1/5):
    base = 'data/metrica/data/Sample_Game_1/Sample_Game_1_RawTrackingData_'
    d = metrica.load_tracking_csv(
        home_data=base + 'Home_Team.csv',
        away_data=base + 'Away_Team.csv',
        sample_rate=sample_rate,
    )
    d = d.transform(to_pitch_dimensions=PITCH)
    return fix_ball(d.to_df(), fps=25 * sample_rate)

def normalize_direction(df):
    """Flip periods so the home team always attacks toward +x."""
    xs = [c for c in df.columns if c.endswith('_x')]
    ys = [c for c in df.columns if c.endswith('_y')]
    hx = [c for c in xs if c.startswith('home_')]
    ax = [c for c in xs if c.startswith('away_')]
    df = df.copy()
    for p, g in df.groupby('period_id'):
        if g[hx].stack().mean() > g[ax].stack().mean():
            df.loc[g.index, xs] = 105 - g[xs]
            df.loc[g.index, ys] = 68 - g[ys]
    return df

def load_game1_norm(sample_rate=1/5):
    return normalize_direction(load_game1(sample_rate))
