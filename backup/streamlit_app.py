import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime
import os

st.set_page_config(
    page_title="Azure Forecast — Capacity Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@500;600;700;800&display=swap');

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes borderGlow {
        0%,100% { border-color: rgba(59,130,246,0.4); box-shadow: 0 0 12px rgba(59,130,246,0.08); }
        25% { border-color: rgba(139,92,246,0.5); box-shadow: 0 0 18px rgba(139,92,246,0.12); }
        50% { border-color: rgba(6,182,212,0.5); box-shadow: 0 0 18px rgba(6,182,212,0.12); }
        75% { border-color: rgba(236,72,153,0.4); box-shadow: 0 0 12px rgba(236,72,153,0.08); }
    }
    @keyframes pulseGlow {
        0%,100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    @keyframes sparkle {
        0%,100% { opacity: 0; transform: scale(0); }
        50% { opacity: 1; transform: scale(1); }
    }

    :root {
        --bg-primary: #050506;
        --bg-card: #0c0c10;
        --bg-elevated: #111116;
        --border: #1a1a24;
        --border-hover: #3b82f6;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --blue: #3b82f6;
        --purple: #8b5cf6;
        --cyan: #06b6d4;
        --green: #10b981;
        --amber: #f59e0b;
        --pink: #ec4899;
        --red: #ef4444;
        --glow-gradient: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4, #ec4899, #f59e0b, #3b82f6);
    }

    .stApp {
        background: linear-gradient(165deg, var(--bg-primary) 0%, #07071a 45%, #060612 100%);
        color: var(--text-primary);
    }

    h1 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em;
        color: #ffffff !important;
        text-shadow: 0 0 30px rgba(59,130,246,0.3), 0 0 60px rgba(139,92,246,0.15) !important;
    }
    h2,h3,h4 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
        color: #ffffff !important;
        text-shadow: 0 0 20px rgba(59,130,246,0.2), 0 0 40px rgba(139,92,246,0.08) !important;
    }
    p, span, div, label { font-family: 'Inter', sans-serif; }

    #MainMenu, footer { visibility: hidden; }
    header { background-color: transparent !important; }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #04040a 0%, #08081a 40%, #060614 100%) !important;
        border-right: 1.5px solid rgba(59,130,246,0.18);
        box-shadow: 4px 0 30px rgba(0,0,0,0.6), 1px 0 8px rgba(59,130,246,0.04);
    }
    section[data-testid="stSidebar"] h3 {
        font-size: 0.88rem !important;
        color: #e2e8f0 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        text-shadow: 0 0 15px rgba(59,130,246,0.2) !important;
    }
    section[data-testid="stSidebar"] label {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        text-shadow: 0 0 6px rgba(148,163,184,0.1);
    }
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] .stDateInput > div > div,
    section[data-testid="stSidebar"] [data-baseweb="input"] {
        background: #0a0a14 !important;
        border-color: rgba(59,130,246,0.15) !important;
        color: #e2e8f0 !important;
        border-radius: 10px !important;
    }
    section[data-testid="stSidebar"] input:focus {
        border-color: rgba(59,130,246,0.5) !important;
        box-shadow: 0 0 10px rgba(59,130,246,0.12) !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background: rgba(59,130,246,0.12) !important;
        border: 1px solid rgba(59,130,246,0.3) !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: #0a0a14 !important;
        border-color: rgba(59,130,246,0.15) !important;
        border-radius: 10px !important;
    }
    section[data-testid="stSidebar"] .stCheckbox label span {
        color: #94a3b8 !important;
    }
    section[data-testid="stSidebar"] ::-webkit-scrollbar {
        width: 4px;
    }
    section[data-testid="stSidebar"] ::-webkit-scrollbar-track {
        background: transparent;
    }
    section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
        background: rgba(59,130,246,0.2);
        border-radius: 4px;
    }
    .sidebar-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(59,130,246,0.2), rgba(139,92,246,0.15), transparent);
        margin: 1.2rem 0;
        border: none;
    }
    .sidebar-card {
        background: linear-gradient(145deg, rgba(14,14,22,0.9), rgba(8,8,18,0.95));
        border: 1px solid rgba(59,130,246,0.12);
        border-radius: 12px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.8rem;
    }
    .sidebar-card-title {
        font-size: 0.7rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .sidebar-card-value {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #f1f5f9;
        text-shadow: 0 0 14px rgba(59,130,246,0.25);
    }
    .sidebar-badge {
        display: inline-block;
        background: rgba(16,185,129,0.12);
        border: 1px solid rgba(16,185,129,0.3);
        color: #10b981;
        font-size: 0.68rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, var(--bg-elevated) 0%, var(--bg-card) 100%);
        border: 1.5px solid rgba(59,130,246,0.3);
        border-radius: 16px;
        padding: 1.3rem 1.4rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5), 0 0 15px rgba(59,130,246,0.06), inset 0 1px 0 rgba(255,255,255,0.03);
        transition: all .3s cubic-bezier(.4,0,.2,1);
        overflow: hidden;
        position: relative;
        animation: borderGlow 6s ease-in-out infinite;
    }
    div[data-testid="metric-container"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent 0%, #3b82f6 20%, #8b5cf6 40%, #06b6d4 60%, #ec4899 80%, transparent 100%);
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
    }
    div[data-testid="metric-container"]::after {
        content: "✦";
        position: absolute;
        top: 8px; right: 12px;
        font-size: 10px;
        color: rgba(139,92,246,0.4);
        animation: sparkle 2s ease-in-out infinite;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: var(--cyan);
        box-shadow: 0 20px 60px rgba(59,130,246,0.2), 0 0 30px rgba(139,92,246,0.15), inset 0 1px 0 rgba(255,255,255,0.06);
    }

    div[data-testid="stMetricValue"] {
        font-family: 'Poppins', sans-serif !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        line-height: 1.2 !important;
        text-shadow: 0 0 18px rgba(6,182,212,0.35), 0 0 40px rgba(59,130,246,0.15);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        text-shadow: 0 0 10px rgba(59,130,246,0.12);
    }
    div[data-testid="stMetricDelta"] svg { display: none; }

    .section-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: var(--text-primary);
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 0.6rem;
        border-bottom: 2px solid transparent;
        border-image: var(--glow-gradient) 1;
        border-image-slice: 1;
        text-shadow: 0 0 20px rgba(59,130,246,0.3);
    }
    .section-header::after {
        content: ""; flex: 1; height: 2px;
        background: linear-gradient(90deg, rgba(139,92,246,0.4), rgba(6,182,212,0.2), transparent 80%);
        animation: pulseGlow 3s ease-in-out infinite;
    }

    .chart-card {
        background: linear-gradient(145deg, rgba(14,14,20,0.9), rgba(10,10,16,0.95));
        border: 1.5px solid rgba(139,92,246,0.25);
        border-radius: 14px;
        padding: 1.2rem 1.2rem 0.5rem;
        margin-bottom: 0.6rem;
        backdrop-filter: blur(8px);
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0,0,0,0.4), 0 0 8px rgba(139,92,246,0.05);
        transition: all .35s ease;
    }
    .chart-card::before {
        content: "";
        position: absolute;
        top: 0; left: -100%; right: 0;
        height: 100%; width: 50%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.03), transparent);
        animation: shimmer 4s ease-in-out infinite;
        pointer-events: none;
    }
    .chart-card:hover {
        border-color: rgba(6,182,212,0.4);
        box-shadow: 0 8px 32px rgba(6,182,212,0.12), 0 0 20px rgba(139,92,246,0.08);
    }
    .chart-title {
        font-family: 'Poppins', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.15rem;
        text-shadow: 0 0 12px rgba(139,92,246,0.2), 0 0 25px rgba(59,130,246,0.08);
    }
    .chart-subtitle {
        font-size: 0.78rem;
        color: var(--text-muted);
        margin-bottom: 0.6rem;
        text-shadow: 0 0 8px rgba(100,116,139,0.15);
    }

    .neon-alert {
        background: linear-gradient(135deg, rgba(239,68,68,0.08), rgba(239,68,68,0.02));
        border: 1.5px solid rgba(239,68,68,0.5);
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        color: var(--red);
        display: flex;
        align-items: center;
        gap: 1.2rem;
        box-shadow: 0 0 30px rgba(239,68,68,0.12), 0 0 60px rgba(239,68,68,0.05);
        animation: borderGlow 4s ease-in-out infinite;
    }
    .neon-success {
        background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(16,185,129,0.02));
        border: 1.5px solid rgba(16,185,129,0.5);
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        color: var(--green);
        display: flex;
        align-items: center;
        gap: 1.2rem;
        box-shadow: 0 0 30px rgba(16,185,129,0.12), 0 0 60px rgba(16,185,129,0.05);
    }

    .insight-banner {
        background: linear-gradient(135deg, rgba(59,130,246,0.08), rgba(139,92,246,0.05));
        border: 1.5px solid rgba(59,130,246,0.35);
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        color: var(--text-secondary);
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        font-size: 0.88rem;
        line-height: 1.55;
        box-shadow: 0 0 20px rgba(59,130,246,0.08), 0 0 40px rgba(139,92,246,0.04);
        position: relative;
        overflow: hidden;
    }
    .insight-banner::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4, #ec4899, #3b82f6);
        background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
    }

    .stat-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(59,130,246,0.2);
        border-radius: 8px;
        padding: 0.35rem 0.7rem;
        font-size: 0.78rem;
        color: var(--text-secondary);
        transition: all .3s ease;
    }
    .stat-pill:hover {
        border-color: rgba(6,182,212,0.5);
        box-shadow: 0 0 12px rgba(6,182,212,0.15);
        color: var(--text-primary);
    }
    .stat-pill .val { font-weight: 700; }

    .styled-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.82rem;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(59,130,246,0.15);
    }
    .styled-table th {
        background: rgba(59,130,246,0.1);
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.72rem;
        padding: 0.7rem 0.9rem;
        text-align: left;
        border-bottom: 1px solid rgba(59,130,246,0.2);
    }
    .styled-table td {
        padding: 0.6rem 0.9rem;
        border-bottom: 1px solid rgba(26,26,36,0.6);
        color: var(--text-primary);
    }
    .styled-table tr:hover td { background: rgba(59,130,246,0.06); }
    .styled-table .good { color: var(--green); font-weight: 600; }
    .styled-table .warn { color: var(--amber); font-weight: 600; }
    .styled-table .bad { color: var(--red); font-weight: 600; }

    .app-footer {
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 2px solid transparent;
        border-image: linear-gradient(90deg, transparent, #3b82f6, #8b5cf6, #06b6d4, transparent) 1;
        text-align: center;
        color: var(--text-muted);
        font-size: 0.78rem;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
    }

    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

BRAND = ['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ec4899']
px.defaults.template = "plotly_dark"
px.defaults.color_discrete_sequence = BRAND

def style(fig, height=None):
    kw = dict(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', color='#94a3b8', size=11),
        margin=dict(l=12, r=12, t=36, b=12),
        xaxis=dict(gridcolor='#14141e', zeroline=False, showline=False),
        yaxis=dict(gridcolor='#14141e', zeroline=False, showline=False),
        hoverlabel=dict(bgcolor='#111118', font_size=12, font_family='Inter', bordercolor='#3b82f6'),
        legend=dict(orientation='h', yanchor='bottom', y=1.04, xanchor='center', x=0.5, font=dict(size=10)),
        hovermode='x unified',
    )
    if height:
        kw['height'] = height
    fig.update_layout(**kw)
    return fig

@st.cache_data
def load_and_engineer():
    path = os.path.join("outputs", "forecast_output.csv")
    if not os.path.exists(path):
        return pd.DataFrame(), pd.DataFrame()

    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
    df['day_name'] = df['date'].dt.day_name()
    df['week'] = df['date'].dt.isocalendar().week.astype(int)

    daily = df.groupby('date')[['actual', 'forecast']].sum().reset_index().sort_values('date')
    daily['rolling_actual_7'] = daily['actual'].rolling(7, min_periods=1).mean()
    daily['rolling_forecast_7'] = daily['forecast'].rolling(7, min_periods=1).mean()

    mu, sigma = daily['actual'].mean(), daily['actual'].std()
    daily['is_anomaly'] = (daily['actual'] > mu + 2 * sigma) | (daily['actual'] < mu - 2 * sigma)

    rmse_g = np.sqrt(mean_squared_error(daily['actual'], daily['forecast']))
    margin = rmse_g * 1.96
    daily['ci_upper'] = daily['forecast'] + margin
    daily['ci_lower'] = np.maximum(0, daily['forecast'] - margin)
    daily['abs_error'] = np.abs(daily['actual'] - daily['forecast'])
    daily['rolling_error_7'] = daily['abs_error'].rolling(7, min_periods=1).mean()
    daily['growth_pct'] = daily['forecast'].pct_change().mul(100).fillna(0).replace([np.inf, -np.inf], 0)
    daily['gap'] = daily['forecast'] - daily['actual']
    daily['accuracy_pct'] = np.where(daily['actual'] != 0,
                                      (1 - daily['abs_error'] / daily['actual']) * 100, 100)

    return df, daily

df_raw, daily_raw = load_and_engineer()
if df_raw.empty:
    st.error("❌ Dataset `outputs/forecast_output.csv` not found. Run the batch pipeline first.")
    st.stop()

_RMSE_g, _MAE_g, _acc_g = 0.0, 0.0, 100.0
if not daily_raw.empty and len(daily_raw) > 1:
    _RMSE_g = np.sqrt(mean_squared_error(daily_raw['actual'], daily_raw['forecast']))
    _MAE_g = mean_absolute_error(daily_raw['actual'], daily_raw['forecast'])
    _nz = daily_raw[daily_raw['actual'] != 0]
    if not _nz.empty:
        _acc_g = max(0, 100 - (_nz['abs_error'] / _nz['actual']).mean() * 100)

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:0.5rem 0 0.3rem'>
        <div style='font-size:2rem; margin-bottom:0.2rem'>⚡</div>
        <div style='font-family:Poppins,sans-serif; font-size:1rem; font-weight:700; color:#fff; letter-spacing:-0.02em'>Azure Forecast</div>
        <div style='font-size:0.68rem; color:#64748b; margin-top:0.1rem'>Capacity Intelligence v1.0</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='sidebar-card'>
        <div class='sidebar-card-title'>System Status</div>
        <div style='display:flex; align-items:center; justify-content:space-between'>
            <span style='color:#10b981; font-weight:600; font-size:0.85rem'>● Online</span>
            <span class='sidebar-badge'>Live</span>
        </div>
        <div style='font-size:0.72rem; color:#64748b; margin-top:0.4rem'>Last sync: {datetime.now().strftime('%H:%M:%S')}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='sidebar-card'>
        <div class='sidebar-card-title'>ML Engine</div>
        <div class='sidebar-card-value'>XGBoost</div>
        <div style='display:flex; gap:8px; margin-top:0.4rem; flex-wrap:wrap'>
            <span style='font-size:0.68rem; color:#3b82f6; background:rgba(59,130,246,0.08); padding:2px 7px; border-radius:5px; border:1px solid rgba(59,130,246,0.15)'>RMSE: {_RMSE_g:.1f}</span>
            <span style='font-size:0.68rem; color:#06b6d4; background:rgba(6,182,212,0.08); padding:2px 7px; border-radius:5px; border:1px solid rgba(6,182,212,0.15)'>MAE: {_MAE_g:.1f}</span>
            <span style='font-size:0.68rem; color:#10b981; background:rgba(16,185,129,0.08); padding:2px 7px; border-radius:5px; border:1px solid rgba(16,185,129,0.15)'>Acc: {_acc_g:.1f}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    st.markdown("### 🎛️ Filters")
    min_d, max_d = df_raw['date'].min(), df_raw['date'].max()
    date_range = st.date_input("Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d)

    all_regions = sorted(df_raw['region'].unique())
    sel_regions = st.multiselect("Region", all_regions, default=all_regions)

    all_services = sorted(df_raw['service_type'].unique()) if 'service_type' in df_raw.columns else []
    sel_services = st.multiselect("Service Type", all_services, default=all_services) if all_services else []

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    st.markdown("### 📐 Display")
    show_ci = st.checkbox("Confidence Band", value=True)
    show_rolling = st.checkbox("Rolling Average", value=True)

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='text-align:center; padding:0.5rem 0; margin-top:auto'>
        <div style='font-size:0.65rem; color:#475569'>Powered by</div>
        <div style='font-size:0.75rem; color:#94a3b8; font-weight:600; margin-top:0.1rem'>Streamlit + Plotly + XGBoost</div>
        <div style='font-size:0.62rem; color:#334155; margin-top:0.3rem'>{len(df_raw):,} records · {datetime.now().strftime('%Y')}</div>
    </div>
    """, unsafe_allow_html=True)

if len(date_range) == 2:
    s, e = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df = df_raw[(df_raw['date'] >= s) & (df_raw['date'] <= e)].copy()
    daily = daily_raw[(daily_raw['date'] >= s) & (daily_raw['date'] <= e)].copy()
else:
    df, daily = df_raw.copy(), daily_raw.copy()

if sel_regions:
    df = df[df['region'].isin(sel_regions)]
if sel_services and 'service_type' in df.columns:
    df = df[df['service_type'].isin(sel_services)]

total_demand = df['forecast'].sum()
total_actual = df['actual'].sum()

peak_day_str = "N/A"
if not daily.empty:
    peak_day_str = daily.loc[daily['forecast'].idxmax(), 'date'].strftime('%b %d, %Y')

RMSE, MAE = 0.0, 0.0
if not daily.empty and len(daily) > 1:
    RMSE = np.sqrt(mean_squared_error(daily['actual'], daily['forecast']))
    MAE = mean_absolute_error(daily['actual'], daily['forecast'])

df_temp = df.copy()
df_temp['month_yr'] = df_temp['date'].dt.to_period('M')
mo = df_temp.groupby('month_yr')['forecast'].sum().reset_index()
growth_pct = 0.0
if len(mo) >= 2:
    growth_pct = ((mo.iloc[-1]['forecast'] - mo.iloc[-2]['forecast']) / mo.iloc[-2]['forecast']) * 100

anomaly_count = int(daily['is_anomaly'].sum()) if not daily.empty else 0
risk_score = min(100, max(0, (RMSE / 200) * 60 + min(abs(growth_pct), 40)))

mape = 0.0
if not daily.empty:
    nz = daily[daily['actual'] != 0]
    if not nz.empty:
        mape = (nz['abs_error'] / nz['actual']).mean() * 100
accuracy = max(0, 100 - mape)

with st.container():
    st.markdown("""
        <div style='margin-bottom:0.3rem'>
            <h1 style='margin-bottom:0; font-size:2.4rem'>⚡ Azure Capacity Intelligence</h1>
            <p style='color:#64748b; font-size:1rem; margin-top:0.4rem; margin-bottom:0.5rem'>
                Enterprise ML prediction engine &nbsp;·&nbsp; Real-time demand forecasting &nbsp;·&nbsp; XGBoost pipeline
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='display:flex; gap:10px; flex-wrap:wrap; margin-bottom:2rem'>
            <div class='stat-pill'>📅 <span class='val'>{min_d.strftime('%b %Y')} — {max_d.strftime('%b %Y')}</span></div>
            <div class='stat-pill'>🌍 <span class='val'>{len(sel_regions)} Regions</span></div>
            <div class='stat-pill'>⚙️ <span class='val'>{len(sel_services)} Services</span></div>
            <div class='stat-pill'>📊 <span class='val'>{len(df):,} Records</span></div>
            <div class='stat-pill'>🧠 <span class='val'>XGBoost v1.0</span></div>
        </div>
    """, unsafe_allow_html=True)

with st.container():
    k1, k2, k3, k4, k5, k6 = st.columns(6)

    def kpi(col, icon, label, value, color):
        with col:
            st.markdown(f"""
                <div data-testid="metric-container">
                    <div data-testid="stMetricLabel">{icon} {label}</div>
                    <div data-testid="stMetricValue" style="color:{color} !important">{value}</div>
                </div>
            """, unsafe_allow_html=True)

    kpi(k1, "📊", "Total Demand", f"{int(total_demand):,}", "#3b82f6")
    kpi(k2, "🔥", "Peak Day", peak_day_str, "#f59e0b")
    g_c = "#10b981" if growth_pct >= 0 else "#ef4444"
    kpi(k3, "🚀" if growth_pct >= 0 else "📉", "Growth (MoM)", f"{growth_pct:+.1f}%", g_c)
    kpi(k4, "⚠️" if RMSE > 150 else "🎯", "RMSE", f"{RMSE:.1f}", "#ef4444" if RMSE > 150 else "#8b5cf6")
    kpi(k5, "📏", "MAE", f"{MAE:.1f}", "#06b6d4")
    kpi(k6, "🔴", "Anomalies", str(anomaly_count), "#ef4444" if anomaly_count > 0 else "#10b981")

with st.container():
    best_region = df.groupby('region')['forecast'].sum().idxmax()
    top_service = df.groupby('service_type')['forecast'].sum().idxmax() if 'service_type' in df.columns else "N/A"
    avg_acc = daily['accuracy_pct'].mean() if not daily.empty else 0
    r_sq_top = np.corrcoef(daily['actual'], daily['forecast'])[0, 1] ** 2 if len(daily) > 1 else 0

    st.markdown(f"""
    <div class='insight-banner' style='margin-top:1.5rem'>
        <div style='font-size:1.4rem'>💡</div>
        <div>
            <strong style='color:#f1f5f9'>Key Insights:</strong>
            <strong style='color:#3b82f6'>{best_region}</strong> leads demand at
            <strong style='color:#f59e0b'>{df.groupby("region")["forecast"].sum().max():,.0f}</strong> units.
            Top service: <strong style='color:#8b5cf6'>{top_service}</strong>.
            Model R² = <strong style='color:#06b6d4'>{r_sq_top:.3f}</strong>.
            Accuracy averages <strong style='color:#10b981'>{avg_acc:.1f}%</strong>.
            {f"<span style='color:#ef4444'>⚠ {anomaly_count} anomalous day(s) detected.</span>" if anomaly_count > 0 else "<span style='color:#10b981'>No anomalies — stable.</span>"}
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='section-header'>🧪 Model Diagnostics</div>", unsafe_allow_html=True)

    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        r_squared = np.corrcoef(daily['actual'], daily['forecast'])[0, 1] ** 2 if len(daily) > 1 else 0
        st.markdown(f"""<div class='chart-card'>
            <div class='chart-title'>Prediction Correlation (R² = {r_squared:.3f})</div>
            <div class='chart-subtitle'>Actual vs Forecast scatter — perfect model = diagonal line</div>
        </div>""", unsafe_allow_html=True)
        fig_scatter = go.Figure()
        min_v = min(daily['actual'].min(), daily['forecast'].min())
        max_v = max(daily['actual'].max(), daily['forecast'].max())
        fig_scatter.add_trace(go.Scatter(x=[min_v, max_v], y=[min_v, max_v], mode='lines',
                                          name='Perfect Fit', line=dict(color='#333', width=1.5, dash='dash')))
        fig_scatter.add_trace(go.Scatter(x=daily['actual'], y=daily['forecast'], mode='markers',
                                          name='Daily Points',
                                          marker=dict(color='#3b82f6', size=6, opacity=0.7,
                                                      line=dict(width=0.5, color='#fff')),
                                          text=[f"Date: {d.strftime('%b %d')}<br>Actual: {a:,.0f}<br>Forecast: {f:,.0f}"
                                                for d, a, f in zip(daily['date'], daily['actual'], daily['forecast'])],
                                          hoverinfo='text'))
        style(fig_scatter, height=320)
        fig_scatter.update_layout(xaxis_title='Actual', yaxis_title='Forecast')
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_d2:
        residuals = daily['actual'] - daily['forecast']
        st.markdown(f"""<div class='chart-card'>
            <div class='chart-title'>Residual Distribution</div>
            <div class='chart-subtitle'>Prediction errors — centered = unbiased model (μ={residuals.mean():.0f})</div>
        </div>""", unsafe_allow_html=True)
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=residuals, nbinsx=30, name='Residuals',
                                         marker=dict(color='#8b5cf6', line=dict(color='#0c0c10', width=1)),
                                         opacity=0.85))
        fig_hist.add_vline(x=0, line_dash='dash', line_color='#f59e0b', line_width=2,
                           annotation_text='Zero Error', annotation_font=dict(color='#f59e0b', size=10))
        fig_hist.add_vline(x=residuals.mean(), line_dash='dot', line_color='#ef4444', line_width=1.5,
                           annotation_text=f'Mean: {residuals.mean():.0f}',
                           annotation_font=dict(color='#ef4444', size=10),
                           annotation_position='top left')
        style(fig_hist, height=320)
        fig_hist.update_layout(xaxis_title='Residual (Actual − Forecast)', yaxis_title='Frequency', bargap=0.05)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_d3:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Monthly Demand Waterfall</div>
            <div class='chart-subtitle'>Month-over-month demand change — incremental buildup</div>
        </div>""", unsafe_allow_html=True)
        monthly_demand = df.groupby(df['date'].dt.to_period('M'))['forecast'].sum().reset_index()
        monthly_demand['date'] = monthly_demand['date'].astype(str)
        monthly_demand['delta'] = monthly_demand['forecast'].diff().fillna(monthly_demand['forecast'].iloc[0])
        fig_wf = go.Figure(go.Waterfall(
            x=monthly_demand['date'], y=monthly_demand['delta'],
            textposition='outside',
            text=[f"{v:+,.0f}" if i > 0 else f"{v:,.0f}" for i, v in enumerate(monthly_demand['delta'])],
            connector=dict(line=dict(color='#333', width=1)),
            increasing=dict(marker=dict(color='#10b981')),
            decreasing=dict(marker=dict(color='#ef4444')),
            totals=dict(marker=dict(color='#3b82f6')),
        ))
        style(fig_wf, height=320)
        fig_wf.update_layout(xaxis_title='Month', waterfallgap=0.3)
        st.plotly_chart(fig_wf, use_container_width=True)

with st.container():
    st.markdown("<div class='section-header'>🔬 Advanced Analytics</div>", unsafe_allow_html=True)

    st.markdown("""<div class='chart-card'>
        <div class='chart-title'>Predictive Trajectory & Confidence Bounds</div>
        <div class='chart-subtitle'>Actual vs Forecast with 95% CI, 7-day rolling mean, anomaly markers, and peak annotation</div>
    </div>""", unsafe_allow_html=True)

    fig_main = go.Figure()
    if show_ci:
        fig_main.add_trace(go.Scatter(x=daily['date'], y=daily['ci_upper'], mode='lines',
                                       line=dict(width=0), showlegend=False, hoverinfo='skip'))
        fig_main.add_trace(go.Scatter(x=daily['date'], y=daily['ci_lower'], mode='lines',
                                       line=dict(width=0), fill='tonexty',
                                       fillcolor='rgba(139,92,246,0.1)', name='95% CI', hoverinfo='skip'))

    fig_main.add_trace(go.Scatter(x=daily['date'], y=daily['actual'], mode='lines+markers',
                                   name='Actual', line=dict(color='#3b82f6', width=2.5, shape='spline'),
                                   marker=dict(size=3)))
    if show_rolling:
        fig_main.add_trace(go.Scatter(x=daily['date'], y=daily['rolling_actual_7'], mode='lines',
                                       name='7d Moving Avg', line=dict(color='#06b6d4', width=3, shape='spline')))

    fig_main.add_trace(go.Scatter(x=daily['date'], y=daily['forecast'], mode='lines',
                                   name='Forecast (XGB)', line=dict(color='#8b5cf6', width=2.5, dash='dash', shape='spline')))

    anom = daily[daily['is_anomaly']]
    if not anom.empty:
        fig_main.add_trace(go.Scatter(x=anom['date'], y=anom['actual'], mode='markers',
                                       name=f'Anomaly ({len(anom)})',
                                       marker=dict(color='#ef4444', size=13, symbol='diamond',
                                                   line=dict(width=2, color='#fff')),
                                       text=[f"⚠ {v:,.0f}" for v in anom['actual']], hoverinfo='text'))

    if not daily.empty:
        pk = daily.loc[daily['forecast'].idxmax()]
        fig_main.add_annotation(x=pk['date'], y=pk['forecast'],
                                text=f"Peak: {pk['forecast']:,.0f}",
                                showarrow=True, arrowhead=2, arrowcolor='#f59e0b',
                                font=dict(color='#f59e0b', size=11),
                                bgcolor='rgba(0,0,0,0.7)', bordercolor='#f59e0b', borderpad=4)

    style(fig_main, height=400)
    st.plotly_chart(fig_main, use_container_width=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Growth Velocity</div>
            <div class='chart-subtitle'>Daily forecast % change — momentum tracker</div>
        </div>""", unsafe_allow_html=True)
        fig_vel = go.Figure()
        fig_vel.add_trace(go.Scatter(x=daily['date'], y=daily['growth_pct'], mode='lines',
                                      name='Daily Δ%', line=dict(color='#06b6d4', width=2.5, shape='spline'),
                                      fill='tozeroy', fillcolor='rgba(6,182,212,0.1)'))
        fig_vel.add_hline(y=0, line_dash='dash', line_color='#222')
        style(fig_vel, height=260)
        st.plotly_chart(fig_vel, use_container_width=True)

    with col_g2:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Forecast Gap Analysis</div>
            <div class='chart-subtitle'>Forecast − Actual variance (positive = over-predict)</div>
        </div>""", unsafe_allow_html=True)
        fig_gap = go.Figure()
        fig_gap.add_trace(go.Scatter(x=daily['date'], y=daily['gap'], mode='lines',
                                      name='Gap', line=dict(color='#ec4899', width=2.5, shape='spline'),
                                      fill='tozeroy', fillcolor='rgba(236,72,153,0.12)'))
        fig_gap.add_hline(y=0, line_dash='dash', line_color='#222')
        style(fig_gap, height=260)
        st.plotly_chart(fig_gap, use_container_width=True)

with st.container():
    st.markdown("<div class='section-header'>💡 Strategic Insights</div>", unsafe_allow_html=True)

    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Service Contribution</div>
            <div class='chart-subtitle'>Proportional demand by service tier</div>
        </div>""", unsafe_allow_html=True)
        if 'service_type' in df.columns:
            svc = df.groupby('service_type')['forecast'].sum().reset_index()
            fig_donut = go.Figure(go.Pie(labels=svc['service_type'], values=svc['forecast'], hole=0.62,
                                          marker=dict(colors=BRAND, line=dict(color='#0c0c10', width=3)),
                                          textinfo='percent', hoverinfo='label+percent+value',
                                          textfont=dict(size=11, color='#e2e8f0')))
            fig_donut.add_annotation(text="Services", x=0.5, y=0.5, showarrow=False,
                                      font=dict(size=14, color='#fff', family='Poppins'))
            style(fig_donut, height=310)
            fig_donut.update_layout(showlegend=True,
                                    legend=dict(orientation='h', xanchor='center', x=0.5, y=-0.15, font=dict(size=9)))
            st.plotly_chart(fig_donut, use_container_width=True)

    with col_s2:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Demand Heatmap</div>
            <div class='chart-subtitle'>Average demand by day-of-week × month</div>
        </div>""", unsafe_allow_html=True)
        hdf = df.groupby(['month', 'day_name'])['forecast'].mean().reset_index()
        hdf['month_str'] = hdf['month'].dt.strftime('%b')
        name_map = {'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed',
                    'Thursday': 'Thu', 'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'}
        hdf['day_short'] = hdf['day_name'].map(name_map)
        hdf['day_short'] = pd.Categorical(hdf['day_short'],
                                           categories=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], ordered=True)
        pivot = hdf.pivot_table(index='day_short', columns='month_str', values='forecast')
        fig_heat = px.imshow(pivot, aspect='auto',
                             color_continuous_scale=['#08080e','#1e3a5f','#3b82f6','#8b5cf6','#ec4899'])
        style(fig_heat, height=310)
        fig_heat.update_xaxes(side='top')
        fig_heat.update_layout(coloraxis_colorbar=dict(title='Avg', thickness=10, len=0.55, tickfont=dict(size=9)))
        st.plotly_chart(fig_heat, use_container_width=True)

    with col_s3:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Demand Treemap</div>
            <div class='chart-subtitle'>Hierarchical: Region → Service breakdown</div>
        </div>""", unsafe_allow_html=True)
        if 'service_type' in df.columns:
            tree_df = df.groupby(['region', 'service_type'])['forecast'].sum().reset_index()
            fig_tree = px.treemap(tree_df, path=['region', 'service_type'], values='forecast',
                                  color='forecast', color_continuous_scale=['#0c0c10','#3b82f6','#8b5cf6','#ec4899'])
            style(fig_tree, height=310)
            fig_tree.update_traces(textinfo='label+percent parent',
                                    marker=dict(line=dict(color='#0c0c10', width=2)))
            fig_tree.update_layout(coloraxis_showscale=False, margin=dict(l=5, r=5, t=30, b=5))
            st.plotly_chart(fig_tree, use_container_width=True)

with st.container():
    st.markdown("<div class='section-header'>🔍 Deep Dive</div>", unsafe_allow_html=True)

    col_r1, col_r2, col_r3 = st.columns(3)

    with col_r1:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Region Performance Radar</div>
            <div class='chart-subtitle'>Multi-metric comparison across regions</div>
        </div>""", unsafe_allow_html=True)

        reg_metrics = df.groupby('region').agg(
            demand=('forecast', 'sum'),
            volume=('actual', 'sum'),
            avg_error=('abs_error', 'mean'),
        ).reset_index()
        for c in ['demand', 'volume', 'avg_error']:
            cmax = reg_metrics[c].max()
            if cmax > 0:
                reg_metrics[c + '_norm'] = (reg_metrics[c] / cmax * 100)
            else:
                reg_metrics[c + '_norm'] = 0
        reg_metrics['accuracy_norm'] = 100 - reg_metrics['avg_error_norm']  # invert: lower error = better

        categories = ['Demand', 'Volume', 'Low Error', 'Consistency']
        fig_radar = go.Figure()
        radar_colors = ['#3b82f6', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b']
        for i, (_, row) in enumerate(reg_metrics.iterrows()):
            vals = [row['demand_norm'], row['volume_norm'], row['accuracy_norm'],
                    max(0, 100 - abs(row['demand_norm'] - row['volume_norm']))]
            vals.append(vals[0])
            fig_radar.add_trace(go.Scatterpolar(
                r=vals, theta=categories + [categories[0]],
                name=row['region'], fill='toself',
                fillcolor=f'rgba({int(radar_colors[i % len(radar_colors)][1:3], 16)},{int(radar_colors[i % len(radar_colors)][3:5], 16)},{int(radar_colors[i % len(radar_colors)][5:7], 16)},0.12)',
                line=dict(color=radar_colors[i % len(radar_colors)], width=2)))
        style(fig_radar, height=320)
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#1a1a24', tickfont=dict(size=8)),
                angularaxis=dict(gridcolor='#1a1a24')),
            legend=dict(font=dict(size=9)))
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_r2:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Monthly Demand Volatility</div>
            <div class='chart-subtitle'>Distribution spread per month — box = IQR, whiskers = range</div>
        </div>""", unsafe_allow_html=True)

        df_box = df.copy()
        df_box['month_str'] = df_box['date'].dt.strftime('%b')
        month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        present_months = [m for m in month_order if m in df_box['month_str'].unique()]

        fig_box = px.box(df_box, x='month_str', y='actual', color='month_str',
                         category_orders={'month_str': present_months},
                         color_discrete_sequence=['#3b82f6','#8b5cf6','#06b6d4','#10b981',
                                                  '#f59e0b','#ec4899','#3b82f6','#8b5cf6','#06b6d4'])
        fig_box.update_traces(marker=dict(opacity=0.6, size=3), line=dict(width=1.5))
        style(fig_box, height=320)
        fig_box.update_layout(showlegend=False, xaxis_title='Month', yaxis_title='Actual Demand')
        st.plotly_chart(fig_box, use_container_width=True)

    with col_r3:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Cumulative Demand</div>
            <div class='chart-subtitle'>Running total — Actual vs Forecast divergence over time</div>
        </div>""", unsafe_allow_html=True)

        daily['cum_actual'] = daily['actual'].cumsum()
        daily['cum_forecast'] = daily['forecast'].cumsum()

        fig_cum = go.Figure()
        fig_cum.add_trace(go.Scatter(x=daily['date'], y=daily['cum_actual'], mode='lines',
                                      name='Cumulative Actual',
                                      line=dict(color='#3b82f6', width=2.5, shape='spline'),
                                      fill='tozeroy', fillcolor='rgba(59,130,246,0.06)'))
        fig_cum.add_trace(go.Scatter(x=daily['date'], y=daily['cum_forecast'], mode='lines',
                                      name='Cumulative Forecast',
                                      line=dict(color='#8b5cf6', width=2.5, dash='dash', shape='spline')))
        style(fig_cum, height=320)
        st.plotly_chart(fig_cum, use_container_width=True)

    col_dd1, col_dd2 = st.columns(2)

    with col_dd1:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Forecast Accuracy Trend</div>
            <div class='chart-subtitle'>Daily accuracy % with 7-day smoothed overlay — target ≥ 90%</div>
        </div>""", unsafe_allow_html=True)
        daily['accuracy_smooth'] = daily['accuracy_pct'].rolling(7, min_periods=1).mean()
        fig_acc = go.Figure()
        fig_acc.add_trace(go.Scatter(x=daily['date'], y=daily['accuracy_pct'], mode='lines',
                                      name='Daily Accuracy', line=dict(color='rgba(16,185,129,0.3)', width=1.2)))
        fig_acc.add_trace(go.Scatter(x=daily['date'], y=daily['accuracy_smooth'], mode='lines',
                                      name='7d Smoothed', line=dict(color='#10b981', width=3, shape='spline'),
                                      fill='tozeroy', fillcolor='rgba(16,185,129,0.08)'))
        fig_acc.add_hline(y=90, line_dash='dash', line_color='#f59e0b',
                          annotation_text='Target: 90%', annotation_font=dict(color='#f59e0b', size=10))
        style(fig_acc, height=300)
        fig_acc.update_yaxes(range=[0, 105])
        st.plotly_chart(fig_acc, use_container_width=True)

    with col_dd2:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Region Drill-Down: Actual vs Forecast</div>
            <div class='chart-subtitle'>Grouped comparison per Azure region</div>
        </div>""", unsafe_allow_html=True)
        reg_comp = df.groupby('region')[['actual', 'forecast']].sum().reset_index().sort_values('forecast', ascending=True)
        fig_rc = go.Figure()
        fig_rc.add_trace(go.Bar(y=reg_comp['region'], x=reg_comp['actual'], name='Actual', orientation='h',
                                 marker=dict(color='#3b82f6', line=dict(width=0)), opacity=0.85))
        fig_rc.add_trace(go.Bar(y=reg_comp['region'], x=reg_comp['forecast'], name='Forecast', orientation='h',
                                 marker=dict(color='#8b5cf6', line=dict(width=0)), opacity=0.85))
        style(fig_rc, height=300)
        fig_rc.update_layout(barmode='group', bargap=0.2, bargroupgap=0.1)
        st.plotly_chart(fig_rc, use_container_width=True)

with st.container():
    st.markdown("<div class='section-header'>📋 Weekly Performance Summary</div>", unsafe_allow_html=True)

    if not daily.empty:
        daily_copy = daily.copy()
        daily_copy['week_start'] = daily_copy['date'] - pd.to_timedelta(daily_copy['date'].dt.weekday, unit='D')
        weekly = daily_copy.groupby('week_start').agg(
            actual=('actual', 'sum'), forecast=('forecast', 'sum'),
            avg_error=('abs_error', 'mean'), anomalies=('is_anomaly', 'sum')
        ).reset_index()
        weekly['accuracy'] = np.where(weekly['actual'] != 0,
                                       (1 - weekly['avg_error'] * 7 / weekly['actual']) * 100, 100)
        weekly['accuracy'] = weekly['accuracy'].clip(0, 100)
        weekly = weekly.sort_values('week_start', ascending=False).head(10)

        rows_html = ""
        for _, r in weekly.iterrows():
            acc = r['accuracy']
            acc_class = 'good' if acc >= 90 else 'warn' if acc >= 75 else 'bad'
            anom_class = 'bad' if r['anomalies'] > 0 else 'good'
            rows_html += f"""
            <tr>
                <td>{r['week_start'].strftime('%b %d')}</td>
                <td>{int(r['actual']):,}</td>
                <td>{int(r['forecast']):,}</td>
                <td>{r['avg_error']:.0f}</td>
                <td class='{acc_class}'>{acc:.1f}%</td>
                <td class='{anom_class}'>{int(r['anomalies'])}</td>
            </tr>"""

        st.markdown(f"""
        <div class='chart-card'>
            <div class='chart-title'>Last 10 Weeks — Performance Breakdown</div>
            <div class='chart-subtitle'>Actual vs Forecast, Error, Accuracy, and Anomaly counts per week</div>
            <table class='styled-table' style='margin-top:0.8rem'>
                <thead><tr>
                    <th>Week Of</th><th>Actual</th><th>Forecast</th><th>Avg Error</th><th>Accuracy</th><th>Anomalies</th>
                </tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        """, unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='section-header'>🛡️ Model Monitoring & Risk</div>", unsafe_allow_html=True)

    col_r1, col_r2, col_r3 = st.columns([1, 1, 2])

    with col_r1:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Risk Score</div>
            <div class='chart-subtitle'>Composite RMSE + growth volatility</div>
        </div>""", unsafe_allow_html=True)
        r_color = "#ef4444" if risk_score > 75 else "#f59e0b" if risk_score > 40 else "#10b981"
        fig_g = go.Figure(go.Indicator(
            mode='gauge+number', value=risk_score,
            number=dict(font=dict(color='#fff', size=42), suffix='/100'),
            gauge=dict(axis=dict(range=[0, 100], tickcolor='#333', tickwidth=2),
                       bar=dict(color=r_color, thickness=0.75),
                       bgcolor='rgba(0,0,0,0)', borderwidth=0,
                       steps=[dict(range=[0, 40], color='rgba(16,185,129,0.06)'),
                              dict(range=[40, 75], color='rgba(245,158,11,0.06)'),
                              dict(range=[75, 100], color='rgba(239,68,68,0.06)')])))
        style(fig_g, height=240)
        fig_g.update_layout(margin=dict(l=20, r=20, t=28, b=8))
        st.plotly_chart(fig_g, use_container_width=True)

    with col_r2:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Performance Metrics</div>
            <div class='chart-subtitle'>Model accuracy indicators</div>
        </div>""", unsafe_allow_html=True)

        for lbl, val, clr, unit in [
            ("RMSE", RMSE, "#ef4444", ""), ("MAE", MAE, "#f59e0b", ""),
            ("MAPE", mape, "#8b5cf6", "%"), ("Accuracy", accuracy, "#10b981", "%"),
        ]:
            bar_w = min(val if not unit else val, 100)
            st.markdown(f"""
            <div style='margin-bottom:0.65rem'>
                <div style='display:flex;justify-content:space-between;font-size:0.78rem;color:#94a3b8;margin-bottom:2px'>
                    <span>{lbl}</span><span style='color:{clr};font-weight:700'>{val:.1f}{unit}</span>
                </div>
                <div style='height:5px;background:#14141e;border-radius:3px;overflow:hidden'>
                    <div style='width:{bar_w:.0f}%;height:100%;background:linear-gradient(90deg,{clr},{clr}aa);border-radius:3px'></div>
                </div>
            </div>""", unsafe_allow_html=True)

    with col_r3:
        st.markdown("""<div class='chart-card'>
            <div class='chart-title'>Error Trajectory</div>
            <div class='chart-subtitle'>Daily absolute error with 7-day smoothed MAE trend</div>
        </div>""", unsafe_allow_html=True)
        fig_err = go.Figure()
        fig_err.add_trace(go.Scatter(x=daily['date'], y=daily['abs_error'], mode='lines',
                                      name='Daily |Error|', line=dict(color='rgba(239,68,68,0.3)', width=1.2)))
        fig_err.add_trace(go.Scatter(x=daily['date'], y=daily['rolling_error_7'], mode='lines',
                                      name='7d Smoothed MAE', line=dict(color='#f59e0b', width=3, shape='spline'),
                                      fill='tozeroy', fillcolor='rgba(245,158,11,0.1)'))
        style(fig_err, height=240)
        st.plotly_chart(fig_err, use_container_width=True)

    if risk_score > 75 or RMSE > 150:
        st.markdown(f"""
        <div class="neon-alert" style="margin-top:1rem">
            <div style="font-size:2rem">⚠️</div>
            <div>
                <div style="font-weight:700;font-size:1.1rem;font-family:'Poppins',sans-serif;letter-spacing:0.03em">
                    MODEL RETRAINING RECOMMENDED</div>
                <div style="font-size:0.85rem;color:#fca5a5;margin-top:0.2rem">
                    Risk {risk_score:.0f}/100 &nbsp;·&nbsp; RMSE {RMSE:.1f} (threshold 150) &nbsp;·&nbsp; {anomaly_count} anomalies &nbsp;·&nbsp; Accuracy {accuracy:.1f}%
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="neon-success" style="margin-top:1rem">
            <div style="font-size:2rem">✅</div>
            <div>
                <div style="font-weight:700;font-size:1.1rem;font-family:'Poppins',sans-serif;letter-spacing:0.03em">
                    PREDICTIVE ENGINE NOMINAL</div>
                <div style="font-size:0.85rem;color:#a7f3d0;margin-top:0.2rem">
                    Risk {risk_score:.0f}/100 &nbsp;·&nbsp; RMSE {RMSE:.1f} &nbsp;·&nbsp; MAE {MAE:.1f} &nbsp;·&nbsp; Accuracy {accuracy:.1f}%
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class='app-footer'>
    <span style='font-weight:600; color:#94a3b8'>Azure Capacity Intelligence</span> &nbsp;·&nbsp;
    Powered by XGBoost &nbsp;·&nbsp;
    {len(df_raw)} training records &nbsp;·&nbsp;
    Built with Streamlit + Plotly &nbsp;·&nbsp;
    {datetime.now().strftime('%Y')}
</div>
""", unsafe_allow_html=True)