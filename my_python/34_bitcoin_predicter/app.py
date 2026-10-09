import streamlit as st
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor

# Page appearance
st.set_page_config(page_title='BTC Price Predictor', page_icon='🪙', layout='wide')

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top right, #263044 0%, #0b1120 55%);
        color: #f1f5f9;
        font-family: 'Segoe UI', sans-serif;
    }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1050px; padding-top: 2rem; padding-bottom: 2rem; }
    [data-testid="stSidebar"] {
        background: #101827;
        border-right: 1px solid #263247;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label { color: #e2e8f0; }
    [data-testid="stNumberInput"] input {
        background: #192438;
        color: #ffffff;
        -webkit-text-fill-color: #ffffff;
    }
    [data-testid="stNumberInput"] [data-baseweb="input"] {
        background: #192438;
        border-color: #3a4962;
        border-radius: 10px;
    }
    [data-testid="stNumberInput"] button { background: #25334a; color: #ffffff; }
    [data-testid="stSidebar"] hr { border-color: #334155; }
    .hero {
        display: flex; align-items: center; justify-content: space-between;
        gap: 24px; padding: 32px; margin-bottom: 26px;
        background: linear-gradient(135deg, #1c283c, #111a29);
        border: 1px solid #34435b; border-radius: 22px;
    }
    .eyebrow { color: #fbbf24; font-size: 12px; letter-spacing: 2px; font-weight: 700; }
    .hero h1 { color: #ffffff; font-size: clamp(28px, 4vw, 44px); margin: 10px 0; padding: 0; }
    .hero p { color: #b5c1d4; margin: 0; line-height: 1.7; }
    .bitcoin {
        flex-shrink: 0; display: grid; place-items: center;
        width: 86px; height: 86px; border-radius: 50%;
        background: linear-gradient(135deg, #ffda71, #f59e0b);
        color: #382200; font-size: 52px; font-weight: 800;
        box-shadow: 0 0 36px #f59e0b22;
    }
    .section-title { font-size: 19px; font-weight: 700; margin: 8px 0 14px; }
    .input-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
    .input-card {
        background: #131e30; border: 1px solid #2b3a52;
        border-radius: 16px; padding: 22px; margin-bottom: 22px;
    }
    .coin-name { font-size: 19px; font-weight: 700; margin-bottom: 16px; }
    .usdt { color: #5eead4; }
    .bnb { color: #fcd34d; }
    .data-row { display: flex; justify-content: space-between; gap: 16px; padding: 9px 0; }
    .data-label { color: #b5c1d4; }
    .data-value { color: #f8fafc; font-weight: 600; overflow-wrap: anywhere; text-align: right; }
    .stButton > button {
        width: 100%; min-height: 52px; border: none; border-radius: 12px;
        background: linear-gradient(90deg, #fbbf24, #f59e0b);
        color: #241800; font-size: 16px; font-weight: 700;
        transition: filter 0.2s, transform 0.2s;
    }
    .stButton > button p { color: #241800; font-weight: 700; }
    .stButton > button:hover { filter: brightness(1.08); transform: translateY(-1px); }
    .stButton > button:focus-visible { outline: 3px solid #fff3bd; outline-offset: 3px; }
    .result {
        margin-top: 24px; padding: 28px; text-align: center;
        background: linear-gradient(135deg, #10372e, #142738);
        border: 1px solid #347e69; border-radius: 18px;
    }
    .result-label { color: #c0e8dd; font-size: 16px; }
    .result-value { color: #6ee7b7; font-size: clamp(32px, 5vw, 48px); font-weight: 800; margin: 10px 0; }
    .placeholder {
        margin-top: 24px; padding: 24px; text-align: center;
        color: #b5c1d4; border: 1px dashed #43516a; border-radius: 16px;
    }
    .footer { text-align: center; color: #a7b4c8; font-size: 13px; margin-top: 28px; }
    @media (max-width: 640px) {
        .hero { padding: 22px; gap: 14px; }
        .bitcoin { width: 56px; height: 56px; font-size: 34px; }
        .input-grid { grid-template-columns: 1fr; gap: 0; }
        .input-card { padding: 18px; margin-bottom: 14px; }
    }
</style>

""", unsafe_allow_html=True)

# Load the same trained model
model_path = 'random_forest_model.pkl'
with open(model_path, 'rb') as file:
    model_rf = pickle.load(file)


def predict_btc_price(input_data):
    prediction = model_rf.predict(input_data)
    return prediction[0]


def main():
    st.markdown("""
    <div class="hero">
        <div>
            <div class="eyebrow">BITCOIN · BTC</div>
            <h1>Predict BTC Close Price</h1>
            <p>Enter your USDT and BNB values to generate a BTC close price estimate.</p>
        </div>
        <div class="bitcoin">₿</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.title('Input Features')
    st.sidebar.markdown('Enter the closing prices and volumes below.')

    # Same inputs and parameters
    st.sidebar.markdown('### 🟢 USDT')
    usdt_close = st.sidebar.number_input('USDT Close Price', min_value=0.0, format="%.2f")
    usdt_volume = st.sidebar.number_input('USDT Volume', min_value=0.0, format="%.2f")

    st.sidebar.markdown('---')
    st.sidebar.markdown('### 🟡 BNB')
    bnb_close = st.sidebar.number_input('BNB Close Price', min_value=0.0, format="%.2f")
    bnb_volume = st.sidebar.number_input('BNB Volume', min_value=0.0, format="%.2f")

    # Same dataframe columns and order
    input_data = pd.DataFrame({
        'USDT_Close': [usdt_close],
        'USDT_Volume': [usdt_volume],
        'BNB_Close': [bnb_close],
        'BNB_Volume': [bnb_volume]
    })

    st.markdown('<div class="section-title">Your input overview</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="input-grid">
        <div class="input-card">
            <div class="coin-name usdt">₮ &nbsp; USDT</div>
            <div class="data-row"><span class="data-label">Close price</span><span class="data-value">{usdt_close:,.2f}</span></div>
            <div class="data-row"><span class="data-label">Volume</span><span class="data-value">{usdt_volume:,.2f}</span></div>
        </div>
        <div class="input-card">
            <div class="coin-name bnb">B &nbsp; BNB</div>
            <div class="data-row"><span class="data-label">Close price</span><span class="data-value">{bnb_close:,.2f}</span></div>
            <div class="data-row"><span class="data-label">Volume</span><span class="data-value">{bnb_volume:,.2f}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Same button and prediction logic
    if st.button('Predict BTC Close Price'):
        predicted_price = predict_btc_price(input_data)
        st.markdown(f"""
        <div class="result">
            <div class="result-label">Predicted BTC Close Price</div>
            <div class="result-value">{predicted_price:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="placeholder">Your prediction will appear here after you click the button.</div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer">🪙 BTC Price Predictor</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
