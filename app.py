import streamlit as st
import numpy as np
import pandas as pd
import joblib
import json
import os
from pathlib import Path
from PIL import Image

# ── PAGE CONFIGURATION ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Loan Default Prediction Sandbox",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── DESIGN SYSTEM & STYLING (GLASSMORPHISM & PREMIUM DARK MODE) ────────────────
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* Overall Page Styles */
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0A0F1D 0%, #070A14 100%);
            color: #E2E8F0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
            color: #FFFFFF !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid #1E293B !important;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #38BDF8 !important;
        }

        /* Premium Glassmorphism Cards */
        .glass-card {
            background: rgba(30, 41, 59, 0.45);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .glass-card:hover {
            border-color: rgba(56, 189, 248, 0.4);
            box-shadow: 0 12px 40px 0 rgba(56, 189, 248, 0.15);
            transform: translateY(-2px);
        }

        /* Stat Metrics Display */
        .metric-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 16px;
            border-radius: 12px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            margin: 8px 0;
            background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-value-low {
            background: linear-gradient(135deg, #34D399 0%, #059669 100%) !important;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .metric-value-med {
            background: linear-gradient(135deg, #FBBF24 0%, #D97706 100%) !important;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .metric-value-high {
            background: linear-gradient(135deg, #F87171 0%, #DC2626 100%) !important;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .metric-label {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94A3B8;
        }
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 4px;
        }
        .badge-low {
            background-color: rgba(52, 211, 153, 0.15);
            color: #34D399;
            border: 1px solid rgba(52, 211, 153, 0.3);
        }
        .badge-med {
            background-color: rgba(251, 191, 36, 0.15);
            color: #FBBF24;
            border: 1px solid rgba(251, 191, 36, 0.3);
        }
        .badge-high {
            background-color: rgba(248, 113, 113, 0.15);
            color: #F87171;
            border: 1px solid rgba(248, 113, 113, 0.3);
        }

        /* Custom Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(15, 23, 42, 0.8);
            padding: 8px 12px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .stTabs [data-baseweb="tab"] {
            height: 48px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 8px;
            color: #94A3B8;
            font-size: 0.95rem;
            font-weight: 600;
            border: none;
            padding: 0 20px;
            transition: all 0.2s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #FFFFFF;
            background-color: rgba(255, 255, 255, 0.03);
        }
        .stTabs [aria-selected="true"] {
            background-color: #1E293B !important;
            color: #38BDF8 !important;
            border: 1px solid rgba(56, 189, 248, 0.2) !important;
        }
        
        /* Highlight sections */
        .glow-text {
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        }
        
        .footer {
            text-align: center;
            margin-top: 48px;
            padding: 24px 0;
            font-size: 0.8rem;
            color: #64748B;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }
    </style>
""", unsafe_allow_html=True)


# ── CACHED MODEL LOADER ───────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    """Loads XGBoost classifier and RobustScaler preprocessor."""
    try:
        scaler = joblib.load("models/scaler.pkl")
        xgb_model = joblib.load("models/xgboost.pkl")
        return scaler, xgb_model
    except Exception as e:
        st.error(f"Error loading models from directory: {e}")
        return None, None


@st.cache_data
def get_categories():
    """Returns static categorical mappings extracted from the training set."""
    # We define them explicitly for instant loading without needing raw files
    return {
        "grade": {
            "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6
        },
        "sub_grade": {
            "A1": 0, "A2": 1, "A3": 2, "A4": 3, "A5": 4,
            "B1": 5, "B2": 6, "B3": 7, "B4": 8, "B5": 9,
            "C1": 10, "C2": 11, "C3": 12, "C4": 13, "C5": 14,
            "D1": 15, "D2": 16, "D3": 17, "D4": 18, "D5": 19,
            "E1": 20, "E2": 21, "E3": 22, "E4": 23, "E5": 24,
            "F1": 25, "F2": 26, "F3": 27, "F4": 28, "F5": 29,
            "G1": 30, "G2": 31, "G3": 32, "G4": 33, "G5": 34
        },
        "home_ownership": {
            "ANY": 0, "MORTGAGE": 1, "OWN": 2, "RENT": 3
        },
        "verification_status": {
            "Not Verified": 0, "Source Verified": 1, "Verified": 2
        },
        "purpose": {
            "Car": 0, "Credit Card": 1, "Debt Consolidation": 2, "Home Improvement": 3,
            "House": 4, "Major Purchase": 5, "Medical": 6, "Moving": 7,
            "Other": 8, "Renewable Energy": 9, "Small Business": 10, "Vacation": 11
        },
        "addr_state": [
            "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN",
            "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH",
            "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA",
            "VT", "WA", "WI", "WV", "WY"
        ]
    }


scaler, xgb_model = load_models()
cats = get_categories()

# Define the exact features sequence expected by RobustScaler and XGBoost (36 features)
FEATURE_COLS = [
    'loan_amnt', 'term', 'int_rate', 'grade', 'sub_grade', 'annual_inc', 'emp_length',
    'home_ownership', 'verification_status', 'purpose', 'addr_state', 'dti',
    'delinq_2yrs', 'inq_last_6mths', 'revol_bal', 'revol_util', 'total_acc',
    'open_acc', 'pub_rec', 'chargeoff_within_12_mths', 'mort_acc',
    'num_actv_bc_tl', 'num_bc_sats', 'num_il_tl', 'mths_since_recent_inq',
    'bc_util', 'pct_tl_nvr_dlq', 'installment', 'funded_amnt', 'funded_amnt_inv',
    'income_to_loan_ratio', 'interest_burden', 'loan_to_income', 'open_acc_ratio',
    'total_delinquency', 'high_interest'
]

# ── HEADER & BRANDING ─────────────────────────────────────────────────────────
st.write("")
col_logo, col_title = st.columns([1, 10])
with col_title:
    st.markdown("""
        <h1 style='margin-bottom: 0px;'>🔮 RETAIL LOAN DEFAULT PREDICTION</h1>
        <p style='color: #64748B; font-size: 1.1rem; margin-top: 4px; font-weight: 500;'>
            Enterprise-grade Machine Learning Credit Scoring & Borrower Risk Sandbox
        </p>
    """, unsafe_allow_html=True)


# ── MAIN TABS CONFIGURATION ───────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 Risk Assessment Sandbox", 
    "📊 Portfolio & Credit Insights (EDA)", 
    "⚙️ Model Diagnostics & Performance", 
    "📄 Executive Briefing Report"
])


# ── SIDEBAR: BORROWER INPUTS ──────────────────────────────────────────────────
st.sidebar.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h2 style='margin: 0; font-size: 1.5rem;'>📝 Borrower Profile</h2>
        <span class="badge badge-low" style="font-size: 0.65rem;">XGBoost Sandbox v1.0</span>
    </div>
    <hr style='border-color: #1E293B; margin-top: 10px; margin-bottom: 20px;'/>
""", unsafe_allow_html=True)

st.sidebar.subheader("💵 Loan Proposal")
loan_amnt = st.sidebar.number_input("Requested Loan Amount ($)", min_value=500, max_value=40000, value=15000, step=500)
term_str = st.sidebar.selectbox("Repayment Term", ["36 Months", "60 Months"])
term = 36.0 if "36" in term_str else 60.0

int_rate = st.sidebar.slider("Interest Rate (%)", min_value=4.0, max_value=35.9, value=12.5, step=0.1)
grade = st.sidebar.selectbox("Loan Grade", list(cats["grade"].keys()), index=1) # Default B
sub_grade = st.sidebar.selectbox("Loan Sub-Grade", list(cats["sub_grade"].keys()), index=7) # Default B3

# Custom automatic installment calculator using standard PMT formula
# r = monthly rate, n = total months
r_monthly = (int_rate / 100.0) / 12.0
n_months = term
if r_monthly > 0:
    auto_inst = loan_amnt * (r_monthly * (1 + r_monthly)**n_months) / ((1 + r_monthly)**n_months - 1)
else:
    auto_inst = loan_amnt / n_months

st.sidebar.markdown(f"<p style='color: #64748B; font-size: 0.8rem; margin-bottom: 2px;'>Calculated Installment: <b>${auto_inst:.2f}/mo</b></p>", unsafe_allow_html=True)
override_inst = st.sidebar.checkbox("Manually override monthly installment?")
if override_inst:
    installment = st.sidebar.number_input("Monthly Installment ($)", min_value=1.0, max_value=2000.0, value=float(round(auto_inst, 2)), step=10.0)
else:
    installment = float(round(auto_inst, 2))

# We set funded amounts to match loan amount (standard retail setup)
funded_amnt = float(loan_amnt)
funded_amnt_inv = float(loan_amnt)

st.sidebar.markdown("<hr style='border-color: #1E293B; margin: 15px 0;'/>", unsafe_allow_html=True)
st.sidebar.subheader("👤 Borrower Financials")
annual_inc = st.sidebar.number_input("Annual Income ($)", min_value=5000, max_value=500000, value=65000, step=1000)
emp_length_str = st.sidebar.selectbox("Employment Length", [
    "< 1 year", "1 year", "2 years", "3 years", "4 years", "5 years", 
    "6 years", "7 years", "8 years", "9 years", "10+ years"
], index=5)
# Extract employment years
if emp_length_str == "< 1 year":
    emp_length = 0.0
elif emp_length_str == "10+ years":
    emp_length = 10.0
else:
    emp_length = float(emp_length_str.split()[0])

home_ownership = st.sidebar.selectbox("Home Ownership Status", list(cats["home_ownership"].keys()), index=1) # Default MORTGAGE
verification_status = st.sidebar.selectbox("Verification Status", list(cats["verification_status"].keys()), index=1) # Default Source Verified
purpose_str = st.sidebar.selectbox("Loan Purpose", list(cats["purpose"].keys()), index=2) # Default Debt Consolidation
purpose_map = {
    "Car": "car", "Credit Card": "credit_card", "Debt Consolidation": "debt_consolidation",
    "Home Improvement": "home_improvement", "House": "house", "Major Purchase": "major_purchase",
    "Medical": "medical", "Moving": "moving", "Other": "other",
    "Renewable Energy": "renewable_energy", "Small Business": "small_business", "Vacation": "vacation"
}
purpose = purpose_map[purpose_str]

addr_state = st.sidebar.selectbox("State of Residence", cats["addr_state"], index=33) # Default NY (index 33)

st.sidebar.markdown("<hr style='border-color: #1E293B; margin: 15px 0;'/>", unsafe_allow_html=True)
st.sidebar.subheader("🛡️ Credit History & Risk")
dti = st.sidebar.slider("Debt-To-Income (DTI) Ratio (%)", min_value=0.0, max_value=100.0, value=18.0, step=0.1)

# Combined delinquencies
delinq_2yrs = st.sidebar.slider("Delinquencies (Last 2 Years)", min_value=0, max_value=15, value=0, step=1)
pub_rec = st.sidebar.slider("Public Records (e.g. Bankruptcies)", min_value=0, max_value=5, value=0, step=1)
chargeoff_within_12_mths = st.sidebar.slider("Charge-offs (Last 12 Months)", min_value=0, max_value=5, value=0, step=1)

inq_last_6mths = st.sidebar.slider("Credit Inquiries (Last 6 Months)", min_value=0, max_value=8, value=0, step=1)
mths_since_recent_inq = st.sidebar.number_input("Months Since Recent Inquiry", min_value=0, max_value=24, value=6, step=1)

revol_bal = st.sidebar.number_input("Total Revolving Balance ($)", min_value=0, max_value=250000, value=12000, step=500)
revol_util = st.sidebar.slider("Revolving Utilization Rate (%)", min_value=0.0, max_value=120.0, value=45.0, step=0.5)
bc_util = st.sidebar.slider("Bankcard Utilization Rate (%)", min_value=0.0, max_value=120.0, value=48.0, step=0.5)

st.sidebar.markdown("<hr style='border-color: #1E293B; margin: 15px 0;'/>", unsafe_allow_html=True)
st.sidebar.subheader("📐 Account Profiles")
open_acc = st.sidebar.slider("Open Credit Lines", min_value=1, max_value=40, value=10, step=1)
total_acc = st.sidebar.slider("Total Credit Lines", min_value=1, max_value=80, value=22, step=1)
# Prevent logic errors where open > total
if open_acc > total_acc:
    total_acc = open_acc

mort_acc = st.sidebar.slider("Mortgage Accounts", min_value=0, max_value=10, value=1, step=1)
num_actv_bc_tl = st.sidebar.slider("Active Bankcard Accounts", min_value=0, max_value=15, value=3, step=1)
num_bc_sats = st.sidebar.slider("Satisfactory Bankcard Accounts", min_value=0, max_value=15, value=4, step=1)
num_il_tl = st.sidebar.slider("Installment Accounts", min_value=0, max_value=30, value=6, step=1)
pct_tl_nvr_dlq = st.sidebar.slider("Accounts Never Delinquent (%)", min_value=0.0, max_value=100.0, value=100.0, step=1.0)


# ── TAB 1: RISK ASSESSMENT SANDBOX ──────────────────────────────────────────
with tab1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🔮 Instant Risk Assessment Sandbox")
    st.markdown("""
        Modify the borrower's parameters in the left panel to dynamically score this loan.
        Our enterprise classifier leverages an advanced gradient-boosted ensemble trained on LendingClub historical performance.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if scaler is None or xgb_model is None:
        st.warning("⚠️ ML Model or Scaler not found in directory. Displaying static simulator mode.")
        # Fallback simulator for demonstrations
        pd_value = 0.125 + (int_rate / 100.0) * 0.5 + (dti / 100.0) * 0.3 - (annual_inc / 500000.0) * 0.2
        pd_value = max(0.01, min(0.99, pd_value))
    else:
        # Encode Categorical inputs using training mappings
        encoded_grade = cats["grade"][grade]
        encoded_sub_grade = cats["sub_grade"][sub_grade]
        encoded_home = cats["home_ownership"][home_ownership]
        encoded_verif = cats["verification_status"][verification_status]
        
        # State mappings
        state_mapping = {
            "AK": 0, "AL": 1, "AR": 2, "AZ": 3, "CA": 4, "CO": 5, "CT": 6, "DC": 7, "DE": 8,
            "FL": 9, "GA": 10, "HI": 11, "ID": 12, "IL": 13, "IN": 14, "KS": 15, "KY": 16,
            "LA": 17, "MA": 18, "MD": 19, "ME": 20, "MI": 21, "MN": 22, "MO": 23, "MS": 24,
            "MT": 25, "NC": 26, "ND": 27, "NE": 28, "NH": 29, "NJ": 30, "NM": 31, "NV": 32,
            "NY": 33, "OH": 34, "OK": 35, "OR": 36, "PA": 37, "RI": 38, "SC": 39, "SD": 40,
            "TN": 41, "TX": 42, "UT": 43, "VA": 44, "VT": 45, "WA": 46, "WI": 47, "WV": 48,
            "WY": 49
        }
        encoded_state = state_mapping[addr_state]
        
        # Purpose mapping
        purpose_mapping = {
            "car": 0, "credit_card": 1, "debt_consolidation": 2, "home_improvement": 3,
            "house": 4, "major_purchase": 5, "medical": 6, "moving": 7,
            "other": 8, "renewable_energy": 9, "small_business": 10, "vacation": 11
        }
        encoded_purpose = purpose_mapping[purpose]
        
        # ── CALCULATE ENGINEERED FEATURES ────────────────────────────────────
        income_to_loan_ratio = annual_inc / (loan_amnt + 1.0)
        interest_burden = (installment * 12.0) / (annual_inc + 1.0)
        loan_to_income = loan_amnt / (annual_inc + 1.0)
        open_acc_ratio = open_acc / (total_acc + 1.0)
        total_delinquency = float(delinq_2yrs + pub_rec + chargeoff_within_12_mths)
        
        q75_int = 15.99
        high_interest = 1.0 if int_rate > q75_int else 0.0
        
        # Build raw features dictionary
        raw_features = {
            'loan_amnt': float(loan_amnt),
            'term': float(term),
            'int_rate': float(int_rate),
            'grade': float(encoded_grade),
            'sub_grade': float(encoded_sub_grade),
            'annual_inc': float(annual_inc),
            'emp_length': float(emp_length),
            'home_ownership': float(encoded_home),
            'verification_status': float(encoded_verif),
            'purpose': float(encoded_purpose),
            'addr_state': float(encoded_state),
            'dti': float(dti),
            'delinq_2yrs': float(delinq_2yrs),
            'inq_last_6mths': float(inq_last_6mths),
            'revol_bal': float(revol_bal),
            'revol_util': float(revol_util),
            'total_acc': float(total_acc),
            'open_acc': float(open_acc),
            'pub_rec': float(pub_rec),
            'chargeoff_within_12_mths': float(chargeoff_within_12_mths),
            'mort_acc': float(mort_acc),
            'num_actv_bc_tl': float(num_actv_bc_tl),
            'num_bc_sats': float(num_bc_sats),
            'num_il_tl': float(num_il_tl),
            'mths_since_recent_inq': float(mths_since_recent_inq),
            'bc_util': float(bc_util),
            'pct_tl_nvr_dlq': float(pct_tl_nvr_dlq),
            'installment': float(installment),
            'funded_amnt': float(funded_amnt),
            'funded_amnt_inv': float(funded_amnt_inv),
            'income_to_loan_ratio': float(income_to_loan_ratio),
            'interest_burden': float(interest_burden),
            'loan_to_income': float(loan_to_income),
            'open_acc_ratio': float(open_acc_ratio),
            'total_delinquency': float(total_delinquency),
            'high_interest': float(high_interest)
        }
        
        # Convert to exact DataFrame shape & ordering
        input_df = pd.DataFrame([raw_features])[FEATURE_COLS]
        
        # Scale inputs using RobustScaler
        scaled_input = scaler.transform(input_df)
        
        # Run prediction
        pd_value = float(xgb_model.predict_proba(scaled_input)[0][1])

    # Assign risk tier & threshold levels based on notebook
    # low_risk: prob < 0.30, med_risk: prob < 0.55, high_risk: prob >= 0.55
    if pd_value < 0.30:
        risk_tier = "Low Risk"
        risk_class = "metric-value-low"
        badge_style = "badge-low"
        action = "APPROVE"
        suggested_rate_range = "5.0% – 10.0%"
        expected_loss = loan_amnt * pd_value * 0.45 # standard LGD of 45%
        markup_rate = "Prime + 1.25%"
    elif pd_value < 0.55:
        risk_tier = "Medium Risk"
        risk_class = "metric-value-med"
        badge_style = "badge-med"
        action = "REVIEW"
        suggested_rate_range = "11.0% – 17.0%"
        expected_loss = loan_amnt * pd_value * 0.45
        markup_rate = "Prime + 4.50%"
    else:
        risk_tier = "High Risk"
        risk_class = "metric-value-high"
        badge_style = "badge-high"
        action = "REJECT"
        suggested_rate_range = "18.0% – 24.0%+"
        expected_loss = loan_amnt * pd_value * 0.45
        markup_rate = "N/A (Prohibitive)"

    # ── METRIC CARDS ──────────────────────────────────────────────────────────
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown(f"""
            <div class="glass-card metric-container">
                <span class="metric-label">Probability of Default</span>
                <span class="metric-value">{pd_value:.1%}</span>
                <span class="badge {badge_style}">Lending Scorecard</span>
            </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
            <div class="glass-card metric-container">
                <span class="metric-label">Risk Rating Tier</span>
                <span class="metric-value {risk_class}">{risk_tier}</span>
                <span class="badge {badge_style}">{action}</span>
            </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""
            <div class="glass-card metric-container">
                <span class="metric-label">Expected Credit Loss</span>
                <span class="metric-value">${expected_loss:,.2f}</span>
                <span class="badge {badge_style}">45% LGD Base</span>
            </div>
        """, unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"""
            <div class="glass-card metric-container">
                <span class="metric-label">Markup / Recommended Rate</span>
                <span class="metric-value">{suggested_rate_range}</span>
                <span class="badge {badge_style}">{markup_rate}</span>
            </div>
        """, unsafe_allow_html=True)

    # ── GRID LAYOUT FOR ASSESSMENT DETAILS ────────────────────────────────────
    grid_col1, grid_col2 = st.columns([1, 1])
    
    with grid_col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("💡 Underwriting Summary")
        
        # Display elegant progress bar for PD
        pd_pct = int(pd_value * 100)
        progress_color = "#10B981" if risk_tier == "Low Risk" else "#F59E0B" if risk_tier == "Medium Risk" else "#EF4444"
        st.markdown(f"""
            <div style='background: #1E293B; border-radius: 9999px; height: 16px; margin: 15px 0; overflow: hidden; border: 1px solid rgba(255,255,255,0.05);'>
                <div style='background: {progress_color}; width: {pd_pct}%; height: 100%; border-radius: 9999px; box-shadow: 0 0 10px {progress_color};'></div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            - **System Decision Recommendation:** <b style='color: {progress_color};'>{action}</b>
            - **Borrower Risk Profile:** Rated as **{risk_tier}** due to a credit score PD profile of **{pd_value:.2f}**.
            - **Suggesting Risk-based Markup:** Pricing markup is evaluated at **{markup_rate}**, giving a target APR rate between **{suggested_rate_range}**.
            - **Primary Indicators:** 
              - The borrower's annual income is **${annual_inc:,.0f}**, compared to a requested debt footprint of **${loan_amnt:,.0f}** (Income-to-Loan Ratio is **{income_to_loan_ratio:.2f}**).
              - Monthly debt obligations are at **{dti:.2f}%** DTI.
              - The borrower has a total revolving credit exposure of **${revol_bal:,.0f}** utilized at **{revol_util:.2f}%**.
              - There have been **{delinq_2yrs}** delinquencies and **{pub_rec}** public records associated with this credit line.
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with grid_col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📐 Engineered Credit Features")
        st.markdown("""
            Derived features computed on-the-fly and processed by our predictive model:
        """)
        
        eng_col1, eng_col2 = st.columns(2)
        with eng_col1:
            st.metric("Income-to-Loan Cover Ratio", f"{income_to_loan_ratio:.2f}x")
            st.metric("Loan-to-Income Ratio", f"{loan_to_income:.2%}")
            st.metric("Credit Line Utilization Breadth", f"{open_acc_ratio:.2%}")
        with eng_col2:
            st.metric("Monthly Installment Debt Burden", f"{interest_burden:.2%}")
            st.metric("Total Cumulative Delinquencies", f"{int(total_delinquency)}")
            st.metric("High Interest Risk Flag", "Active (1.0)" if high_interest > 0 else "Inactive (0.0)")
        st.markdown("</div>", unsafe_allow_html=True)


# ── TAB 2: PORTFOLIO & CREDIT INSIGHTS (EDA) ──────────────────────────────────
with tab2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📊 Portfolio Credit Analysis & Exploratory Insights")
    st.markdown("""
        The following charts present in-depth Exploratory Data Analysis (EDA) on the underlying LendingClub dataset.
        Use these visualizations to understand empirical relationships between credit characteristics and loan default rates.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Grid of EDA plots
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("💳 Default Rate vs Loan Grade")
        st.image("plots/default_rate_by_grade.png", use_container_width=True)
        st.caption("Default rates rise dramatically for lower grade classifications (E, F, G), representing a strong monotonic relation.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🏠 Default Rate vs Home Ownership Status")
        st.image("plots/default_by_homeownership.png", use_container_width=True)
        st.caption("Borrowers renting homes have higher empirical default rates compared to home owners with mortgages.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("💰 Default Rate by Annual Income Bracket")
        st.image("plots/default_vs_income.png", use_container_width=True)
        st.caption("Empirical default probabilities grouped by annual income deciles, illustrating how higher earnings insulate risk.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_e2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📉 Default Rate vs Debt-To-Income (DTI) Ratio")
        st.image("plots/default_vs_dti.png", use_container_width=True)
        st.caption("Empirical relationship illustrating rising credit default risk as debt service burdens increase relative to income.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("💵 Default Rate by Loan Amount Bracket")
        st.image("plots/default_vs_loan_amnt.png", use_container_width=True)
        st.caption("Distribution showing that larger loans face elevated default risks, often reflecting debt stretching.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🔀 Borrower Feature Distributions")
        st.image("plots/feature_distributions.png", use_container_width=True)
        st.caption("Distributions of numeric credit features highlighting the extreme right skewness of financial metrics.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Correlation Heatmap
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔗 Credit Feature Heatmap: Multicollinearity & Correlation Structure")
    st.image("plots/correlation_heatmap.png", use_container_width=True)
    st.caption("Pairwise Pearson correlations across all engineered and primary credit attributes.")
    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB 3: MODEL DIAGNOSTICS & PERFORMANCE ────────────────────────────────────
with tab3:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Predictive Model Diagnostics & Validation")
    st.markdown("""
        Detailed performance diagnostics, evaluation metrics, and validation curves for our credit scoring models.
        The system benchmarks **XGBoost** against **LightGBM**, **Random Forest**, and **Logistic Regression**.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🏆 Model Classifier AUC Comparison")
        st.image("plots/model_comparison.png", use_container_width=True)
        st.caption("ROC-AUC comparisons on holdout validation splits. Advanced ensemble tree models outclass classic logit.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📈 Receiver Operating Characteristic (ROC) Curves")
        st.image("plots/roc_curves.png", use_container_width=True)
        st.caption("ROC curves comparing the true positive rate (sensitivity) against the false positive rate across decision thresholds.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🎯 Model Calibration: Predicted PD vs Empirical Default")
        st.image("plots/calibration_plot.png", use_container_width=True)
        st.caption("Calibration decile plot showing near-perfect alignment between predicted probability of default and actual default rate.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_d2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("💡 Best Classifier (XGBoost) Confusion Matrix")
        st.image("plots/confusion_matrix_best.png", use_container_width=True)
        st.caption("Confusion matrix of our primary deployment model (XGBoost) indicating high classification precision and recall.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("🗝️ Feature Importance: Primary Credit Drivers")
        st.image("plots/feature_importance.png", use_container_width=True)
        st.caption("Relative information gain of credit features, showing interest rates, grades, DTI, and income to be dominant risk drivers.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("💼 Portfolio Credit Risk Tier Segmentation")
        st.image("plots/risk_tier_analysis.png", use_container_width=True)
        st.caption("Portfolio analysis showing high borrower density in low-risk tiers and extremely high target defaults in high-risk tiers.")
        st.markdown("</div>", unsafe_allow_html=True)


# ── TAB 4: EXECUTIVE BRIEFING REPORT ──────────────────────────────────────────
with tab4:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 📄 Executive Summary & Professional Briefing")
    st.markdown("""
        We have compiled an enterprise-grade Credit Risk Prediction Report detailing the entire data exploration, model validation, and deployment methodology.
        This professional PDF document is instantly downloadable for corporate stakeholders and auditing committees.
    """)
    
    # Load PDF binary for download
    pdf_path = Path("Loan_Default_Report.pdf")
    if pdf_path.exists():
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        
        st.success("🎉 Professional PDF Briefing Report found! Click below to download.")
        st.download_button(
            label="⬇️ Download Executive Credit Risk PDF Report",
            data=pdf_bytes,
            file_name="Loan_Default_Prediction_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.error("⚠️ Loan_Default_Report.pdf not found in the root directory. Run 'python generate_report.py' first.")
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Full Executive Summary Dashboard Image
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📰 Corporate Performance Executive Dashboard")
    st.image("plots/executive_dashboard.png", use_container_width=True)
    st.caption("A summary visualization of performance metrics, ROC curves, calibration deciles, and portfolio risk distributions.")
    st.markdown("</div>", unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="footer">
        🔮 Developed as part of the Retail Loan Default Prediction Suite • Streamlit Cloud Sandbox Integration<br/>
        Enterprise Grade AI Credit Scoring • Google DeepMind Advanced Pair Programming Project • 2026
    </div>
""", unsafe_allow_html=True)
