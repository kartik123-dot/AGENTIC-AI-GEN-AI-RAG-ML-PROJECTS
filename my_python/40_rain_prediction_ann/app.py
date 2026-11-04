"""Streamlit front end for the rain-prediction ANN (futuristic edition).

Run:  streamlit run app.py
Needs rain_model.keras and preprocessor.joblib (created by the notebook).
"""
import datetime
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from rain_utils import CAT_COLS, NUM_COLS  # noqa: F401  (needed to unpickle)

st.set_page_config(page_title="Rain Forecast AI", page_icon="🌧️", layout="wide")

MODEL_PATH = Path("rain_model.keras")
PRE_PATH = Path("preprocessor.joblib")

# ---------- plain-language labels, grouped into tabs ----------
LABELS = {
    "MinTemp": "Lowest temperature today (°C)", "MaxTemp": "Highest temperature today (°C)",
    "Temp9am": "Temperature at 9am (°C)", "Temp3pm": "Temperature at 3pm (°C)",
    "Humidity9am": "Humidity at 9am (%)", "Humidity3pm": "Humidity at 3pm (%)",
    "Cloud9am": "Cloud cover at 9am (0 clear – 8 overcast)",
    "Cloud3pm": "Cloud cover at 3pm (0 clear – 8 overcast)",
    "WindGustSpeed": "Strongest gust today (km/h)",
    "WindSpeed9am": "Wind speed at 9am (km/h)", "WindSpeed3pm": "Wind speed at 3pm (km/h)",
    "Pressure9am": "Air pressure at 9am (hPa)", "Pressure3pm": "Air pressure at 3pm (hPa)",
    "Rainfall": "Rain that fell today (mm)", "Evaporation": "Water evaporated today (mm)",
    "Sunshine": "Hours of sunshine today",
}
HELP = {
    "Humidity3pm": "Higher humidity in the afternoon is one of the strongest rain signals.",
    "Pressure3pm": "Falling pressure usually means unsettled weather.",
    "Cloud3pm": "Oktas = eighths of the sky covered by cloud.",
    "Sunshine": "Few sunshine hours often means a cloudy, damp day.",
}
GROUPS = [
    ("🌡️ Temperature", ["MinTemp", "MaxTemp", "Temp9am", "Temp3pm"]),
    ("💧 Humidity & clouds", ["Humidity9am", "Humidity3pm", "Cloud9am", "Cloud3pm"]),
    ("💨 Wind speed", ["WindGustSpeed", "WindSpeed9am", "WindSpeed3pm"]),
    ("🧭 Pressure & sun", ["Pressure9am", "Pressure3pm", "Sunshine", "Evaporation", "Rainfall"]),
]

# One-click example days so people can see how the model reacts.
PRESETS = {
    "☀️ Sunny day": {"Humidity3pm": 25, "Humidity9am": 45, "Cloud3pm": 1, "Cloud9am": 1,
                     "Sunshine": 11, "Pressure3pm": 1022, "Pressure9am": 1024, "Rainfall": 0},
    "⛈️ Stormy day": {"Humidity3pm": 90, "Humidity9am": 92, "Cloud3pm": 8, "Cloud9am": 8,
                      "Sunshine": 1, "Pressure3pm": 1004, "Pressure9am": 1008, "Rainfall": 12},
}

SENSITIVITY = {
    "Cautious (warn me at 30%)": 0.30,
    "Balanced (warn me at 50%)": 0.50,
    "Relaxed (warn me at 70%)": 0.70,
}

# ---------- futuristic theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Outfit:wght@300;400;500;600&display=swap');
:root{--void:#070B1A;--panel:rgba(20,28,60,.55);--edge:rgba(120,160,255,.22);
--cyan:#4CC9F0;--violet:#7B5CFF;--ice:#E6ECFF;--mute:#93A0C8;--amber:#FFB86B;}
html,body,.stApp{font-family:'Outfit',sans-serif;color:var(--ice);}
.stApp{background:radial-gradient(1200px 600px at 85% -10%,rgba(123,92,255,.28),transparent 60%),
radial-gradient(900px 500px at -10% 10%,rgba(76,201,240,.18),transparent 60%),var(--void);}
#MainMenu,footer{visibility:hidden;} header[data-testid="stHeader"]{background:transparent;}
.block-container{padding-top:2.2rem;max-width:1200px;}
h1,h2,h3,.hero-title{font-family:'Chakra Petch',sans-serif!important;letter-spacing:.2px;}
.hero-title{font-size:2.6rem;font-weight:700;line-height:1.1;margin:0;
background:linear-gradient(90deg,var(--ice),var(--cyan) 60%,var(--violet));
-webkit-background-clip:text;background-clip:text;color:transparent;}
.hero-sub{color:var(--mute);font-size:1.05rem;margin:.5rem 0 1.4rem;max-width:62ch;}
.steps{display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:1.2rem;}
.step{border:1px solid var(--edge);background:var(--panel);border-radius:999px;
padding:.35rem .9rem;color:var(--mute);font-size:.9rem;backdrop-filter:blur(8px);}
.step b{color:var(--cyan);font-weight:600;}
.glass{border:1px solid var(--edge);background:var(--panel);border-radius:20px;
padding:1.4rem 1.4rem 1.1rem;backdrop-filter:blur(14px);
box-shadow:0 0 40px rgba(76,201,240,.07),inset 0 1px 0 rgba(255,255,255,.05);}
.verdict{font-family:'Chakra Petch',sans-serif;font-size:1.5rem;font-weight:600;text-align:center;margin:.2rem 0;}
.advice{color:var(--mute);text-align:center;margin-bottom:.4rem;}
.chips{display:flex;gap:.5rem;flex-wrap:wrap;justify-content:center;margin-top:.8rem;}
.chip{border:1px solid var(--edge);border-radius:12px;padding:.35rem .7rem;font-size:.85rem;color:var(--ice);}
.chip span{color:var(--mute);}
/* tabs */
.stTabs [data-baseweb="tab-list"]{gap:.4rem;border-bottom:1px solid var(--edge);}
.stTabs [data-baseweb="tab"]{background:transparent;border-radius:10px 10px 0 0;color:var(--mute);padding:.55rem .9rem;}
.stTabs [aria-selected="true"]{color:var(--cyan)!important;}
.stTabs [data-baseweb="tab-highlight"]{background:var(--cyan);}
/* inputs */
label,.stMarkdown p{color:var(--ice);}
div[data-baseweb="input"],div[data-baseweb="select"]>div,.stNumberInput input{
background:rgba(10,16,40,.7)!important;border-color:var(--edge)!important;border-radius:10px!important;}
.stButton>button{border:1px solid var(--edge);background:var(--panel);color:var(--ice);
border-radius:12px;font-family:'Outfit',sans-serif;font-weight:500;transition:all .2s;}
.stButton>button:hover{border-color:var(--cyan);color:var(--cyan);box-shadow:0 0 18px rgba(76,201,240,.25);}
.stButton>button:focus-visible,input:focus-visible{outline:2px solid var(--cyan)!important;}
details{border:1px solid var(--edge)!important;border-radius:14px!important;background:var(--panel);}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important;}}
@keyframes sweep{from{stroke-dashoffset:var(--len);}}
.arc{animation:sweep 1.1s ease-out;}
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Starting the forecast engine...")
def load_artifacts():
    from tensorflow import keras  # imported lazily so the page loads fast
    return keras.models.load_model(MODEL_PATH), joblib.load(PRE_PATH)


def gauge(prob: float, color: str) -> str:
    """Half-circle dial that fills to the rain chance."""
    length = 3.14159 * 80  # arc length of the half circle
    fill = max(prob, 0.004) * length
    return (
        '<svg viewBox="0 0 200 125" style="width:100%;max-width:340px;display:block;margin:0 auto">'
        '<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#4CC9F0"/>'
        f'<stop offset="1" stop-color="{color}"/></linearGradient></defs>'
        '<path d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="rgba(120,160,255,.15)" '
        'stroke-width="14" stroke-linecap="round"/>'
        '<path class="arc" d="M20 100 A80 80 0 0 1 180 100" fill="none" stroke="url(#g)" '
        f'stroke-width="14" stroke-linecap="round" stroke-dasharray="{fill:.1f} {length:.1f}" '
        f'style="--len:{fill:.1f}px;filter:drop-shadow(0 0 8px {color})"/>'
        f'<text x="100" y="92" text-anchor="middle" font-family="Chakra Petch" font-size="34" '
        f'font-weight="700" fill="#E6ECFF">{prob:.0%}</text>'
        '<text x="100" y="114" text-anchor="middle" font-family="Outfit" font-size="11" '
        'fill="#93A0C8">chance of rain tomorrow</text>'
        '<text x="14" y="120" font-size="9" fill="#93A0C8" font-family="Outfit">0%</text>'
        '<text x="186" y="120" text-anchor="end" font-size="9" fill="#93A0C8" font-family="Outfit">100%</text>'
        '</svg>'
    )


def describe(prob: float):
    if prob < 0.20: return "Very unlikely", "#4CC9F0"
    if prob < 0.40: return "Unlikely", "#4CC9F0"
    if prob < 0.60: return "Could go either way", "#B48CFF"
    if prob < 0.80: return "Likely", "#FFB86B"
    return "Very likely", "#FF8A5C"


def apply_preset(name: str):
    """Fill the sliders with an example day (runs before widgets are drawn)."""
    for key, val in PRESETS[name].items():
        lo, hi = pre.num_ranges[key]
        st.session_state[key] = float(min(max(val, lo), hi))
    if "RainToday" in pre.classes and "Yes" in pre.classes["RainToday"]:
        st.session_state["rain_today"] = "Yes" if name.startswith("⛈") else "No"


# ---------- header ----------
st.markdown(
    '<p class="hero-title">Will it rain tomorrow?</p>'
    '<p class="hero-sub">Tell the AI about today’s weather and it estimates the chance of rain '
    'tomorrow. It was trained on years of Australian weather records.</p>'
    '<div class="steps"><div class="step"><b>1</b> Pick the place and day</div>'
    '<div class="step"><b>2</b> Enter today’s weather</div>'
    '<div class="step"><b>3</b> Read the forecast on the right</div></div>',
    unsafe_allow_html=True,
)

if not (MODEL_PATH.exists() and PRE_PATH.exists()):
    st.error(
        "The model files are missing. Put `rain_model.keras` and `preprocessor.joblib` "
        "in this folder. Run `rain-prediction-ann-fixed.ipynb` first; its last cell saves them."
    )
    st.stop()

model, pre = load_artifacts()

# ---------- layout: inputs left, forecast right ----------
inputs, result = st.columns([3, 2], gap="large")

with inputs:
    st.markdown("##### Try an example day, or enter your own")
    b1, b2, _ = st.columns([1, 1, 2])
    b1.button("☀️ Sunny day", on_click=apply_preset, args=("☀️ Sunny day",), use_container_width=True)
    b2.button("⛈️ Stormy day", on_click=apply_preset, args=("⛈️ Stormy day",), use_container_width=True)

    values = {}
    tab_names = ["📍 Place & day"] + [g[0] for g in GROUPS] + ["🧭 Wind direction"]
    tabs = st.tabs(tab_names)

    with tabs[0]:
        c1, c2 = st.columns(2)
        date = c1.date_input("Today’s date", datetime.date.today())
        location = c2.selectbox("Weather station", pre.classes["Location"])
        rt = pre.classes["RainToday"]
        rain_today = st.selectbox(
            "Did it rain today?", rt, key="rain_today",
            index=rt.index(pre.modes["RainToday"]),
            help="Rain today makes rain tomorrow a little more likely.",
        )

    shown = set()
    for tab, (_, names) in zip(tabs[1:-1], GROUPS):
        with tab:
            cols = st.columns(2)
            for i, name in enumerate([n for n in names if n in NUM_COLS]):
                lo, hi = pre.num_ranges[name]
                shown.add(name)
                values[name] = cols[i % 2].number_input(
                    LABELS[name], min_value=float(lo), max_value=float(hi),
                    value=float(min(max(pre.medians[name], lo), hi)), step=0.1,
                    key=name, help=HELP.get(name),
                )
    # safety net: any numeric column not placed in a tab
    for name in NUM_COLS:
        if name not in shown:
            lo, hi = pre.num_ranges[name]
            values[name] = st.session_state.get(name, float(min(max(pre.medians[name], lo), hi)))

    with tabs[-1]:
        st.caption("Which way the wind was blowing from.")
        w1, w2, w3 = st.columns(3)

        def wind(col, label, key):
            opts = pre.classes[key]
            return col.selectbox(label, opts, index=opts.index(pre.modes[key]), key=key)

        wind_gust_dir = wind(w1, "Strongest gust", "WindGustDir")
        wind_9am = wind(w2, "At 9am", "WindDir9am")
        wind_3pm = wind(w3, "At 3pm", "WindDir3pm")

    st.caption("Every field starts at a typical value from the dataset, so you only change what you know.")

# ---------- prediction (updates live) ----------
row = pd.DataFrame([{
    "Date": pd.Timestamp(date), "Location": location, "RainToday": rain_today,
    "WindGustDir": wind_gust_dir, "WindDir9am": wind_9am, "WindDir3pm": wind_3pm,
    **values,
}])
X = pre.transform(row).to_numpy("float32")
prob = float(model.predict(X, verbose=0)[0][0])
prob = min(max(prob, 0.0), 1.0)

with result:
    level = st.select_slider(
        "How careful should the warning be?", options=list(SENSITIVITY), value="Balanced (warn me at 50%)",
        help="Cautious warns you about rain more often, including some false alarms.",
    )
    threshold = SENSITIVITY[level]
    label, color = describe(prob)
    rainy = prob >= threshold

    advice = ("☔ Pack an umbrella. Rain is likely." if rainy
              else "☀️ No umbrella needed. Rain is unlikely.")
    st.markdown(
        '<div class="glass">'
        f'{gauge(prob, color)}'
        f'<div class="verdict" style="color:{color}">{label}</div>'
        f'<div class="advice">{advice}</div>'
        '<div class="chips">'
        f'<div class="chip"><span>Station </span>{location}</div>'
        f'<div class="chip"><span>Humidity 3pm </span>{values.get("Humidity3pm", 0):.0f}%</div>'
        f'<div class="chip"><span>Cloud 3pm </span>{values.get("Cloud3pm", 0):.0f}/8</div>'
        f'<div class="chip"><span>Rained today </span>{rain_today}</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    with st.expander("How do I read this?"):
        st.markdown(
            "- The dial shows how likely rain is tomorrow, from 0% to 100%.\n"
            "- Below 20% is very unlikely. Above 80% is very likely.\n"
            f"- With your warning level, you get a rain alert at **{threshold:.0%}** or higher.\n"
            "- This is an estimate from past patterns, not a guarantee. "
            "Check your local forecast before big plans."
        )