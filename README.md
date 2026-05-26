# 🏦 Retail Loan Default Prediction & Risk Analytics

> End-to-end credit risk model built on LendingClub historical loan data (~2.2M records).

---

## 📁 Project Structure

```
loan-default/
├── loan.csv                         # Raw dataset (LendingClub ~1.1 GB)
├── LCDataDictionary.xlsx            # Data dictionary
├── loan_default_prediction.ipynb    # Main notebook (full pipeline)
├── generate_report.py               # PDF report generator
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── plots/                           # Auto-generated visualizations
│   ├── missing_values.png
│   ├── class_distribution.png
│   ├── default_rate_by_grade.png
│   ├── feature_distributions.png
│   ├── correlation_heatmap.png
│   ├── default_vs_dti.png
│   ├── model_comparison.png
│   ├── roc_curves.png
│   ├── confusion_matrix_best.png
│   ├── feature_importance.png
│   ├── risk_tier_analysis.png
│   ├── risk_score_distribution.png
│   ├── portfolio_analysis.png
│   ├── calibration_plot.png
│   ├── default_vs_income.png
│   ├── default_vs_loan_amnt.png
│   └── executive_dashboard.png
├── models/                          # Saved model artifacts
│   ├── scaler.pkl
│   ├── logistic_regression.pkl
│   ├── decision_tree.pkl
│   ├── random_forest.pkl
│   ├── xgboost.pkl
│   └── lightgbm.pkl
├── loan_default_predictions.csv     # Output: borrower-level predictions
├── model_metrics.csv                # Output: model comparison metrics
└── Loan_Default_Report.pdf          # PDF report (generated)
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the Dataset
> ⚠️ **Note:** The raw dataset `loan.csv` (1.18 GB) is excluded from this Git repository due to GitHub's **100 MB** file size limit.
> 
> To run this project locally, download the LendingClub historical loan dataset (e.g., from Kaggle) and place the `loan.csv` file in the root of the project folder.

### 3. Run the Notebook

```bash
jupyter notebook loan_default_prediction.ipynb
```

> **Note:** Running on the full dataset (~2.2M rows) may take 10–20 minutes depending on hardware. The notebook loads and processes data in-memory.

### 4. Generate the PDF Report

```bash
python generate_report.py
```

---

## 🎯 Objective

Build a predictive model to estimate the **Probability of Default (PD)** for retail loan borrowers using historical LendingClub data, and:

- Categorize borrowers into **risk tiers** (Low / Medium / High Risk)
- Recommend lending actions (Approve / Review / Reject)
- Compute **Expected Loss** at portfolio level
- Deliver actionable business insights

---

## 📊 Pipeline Overview

| Step | Description |
|------|-------------|
| **1. Data Loading** | Load 2.2M records, filter to binary classification statuses |
| **2. Preprocessing** | Handle missing values, encode categoricals, cap outliers |
| **3. EDA** | Class distribution, grade-wise default rates, correlation heatmap |
| **4. Feature Engineering** | Income-to-loan ratio, interest burden, delinquency score, etc. |
| **5. Modeling** | Logistic Regression, Decision Tree, Random Forest, XGBoost, LightGBM |
| **6. Evaluation** | Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix |
| **7. Risk Bucketing** | PD thresholds → Low / Medium / High Risk tiers |
| **8. Portfolio Analysis** | Expected Loss (EL = PD × LoanAmount), exposure concentration |
| **9. Insights** | Default rate vs income, DTI, loan amount; sample scorecard |

---

## 🔑 Key Features Used (15+)

| Category | Features |
|----------|----------|
| Loan Details | `loan_amnt`, `term`, `int_rate`, `grade`, `sub_grade`, `installment` |
| Borrower Profile | `annual_inc`, `emp_length`, `home_ownership`, `verification_status`, `purpose` |
| Credit History | `dti`, `delinq_2yrs`, `inq_last_6mths`, `revol_bal`, `revol_util`, `total_acc`, `open_acc`, `pub_rec` |
| Engineered | `income_to_loan_ratio`, `interest_burden`, `loan_to_income`, `open_acc_ratio`, `total_delinquency` |

---

## 📈 Risk Tier Strategy

| Tier | PD Range | Action | Suggested Rate |
|------|----------|--------|----------------|
| 🟢 Low Risk | < 30% | ✅ Approve | 5% – 10% |
| 🟡 Medium Risk | 30% – 55% | ⚠️ Manual Review | 11% – 17% |
| 🔴 High Risk | > 55% | ❌ Reject | 18% – 24%+ |

---

## 📐 Model Selection Rationale

- **Logistic Regression** — Baseline; high interpretability, easy coefficient analysis for regulatory compliance
- **Decision Tree** — Visual rule extraction; useful for explainability with business stakeholders
- **Random Forest** — Strong ensemble performance; handles non-linear interactions
- **XGBoost / LightGBM** — Best performance on tabular credit data; handles class imbalance via `scale_pos_weight`

**Class Imbalance Handling:** All models use `class_weight='balanced'` or `scale_pos_weight` to compensate for the natural imbalance between defaulters and non-defaulters.

---

## 🧾 Target Variable Mapping

| Original `loan_status` | Label |
|------------------------|-------|
| Fully Paid, Current | 0 (Not Defaulted) |
| Charged Off, Default, Late (16-30), Late (31-120) | 1 (Defaulted) |

---

## ✅ Reproducibility

All random states are fixed (`random_state=42`). The notebook runs end-to-end on the provided `loan.csv` file with no manual intervention required.
