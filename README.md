# 📊 Financial Statement Analyzer

A web-based financial analytics application designed to analyze real-world **SME financial statements**, compute key financial ratios, visualize multi-year trends, and generate exportable analytical reports.

Built using **Flask, Pandas, Matplotlib/Seaborn, and Bootstrap**, the application follows a modular architecture and standard financial analysis frameworks used in consulting and corporate finance.

---

## 🚀 Features

- 📁 Upload multi-year financial statements (CSV)
- 📈 Compute key financial metrics:
  - Return on Equity (ROE)
  - Return on Assets (ROA)
  - Debt–Equity Ratio
  - Net Profit Margin
  - Current Ratio 
  - EBITDA Margin 
- 📊 Visualize multi-year performance trends
- 🧮 Structured dashboard with:
  - Profitability analysis
  - Liquidity analysis
  - Leverage analysis
- 📄 Export professional PDF financial analysis reports
- 🧱 Modular and scalable architecture

---

## 🏗️ Project Architecture

```
financial-statement-analyzer/
│
├── app.py
├── requirements.txt
│
├── analysis/
│ ├── init.py
│ ├── preprocess.py
│ ├── metrics.py
│ └── visualizations.py
│
├── reports/
│ └── report_generator.py
│
├── templates/
│ ├── base.html
│ ├── upload.html
│ └── metrics.html
│
├── static/
│ ├── css/
│ │ └── styles.css
│ ├── plots/
│ ├── uploads/
│ └── reports/
│
└── data/
└── sample_sme_financials.csv
```


The system dynamically computes ratios based on available data, making it robust for real-world SME financial statements.

---

## 📊 Sample SME Dataset

A realistic multi-year SME dataset is included:
data/sample1_sme_financials.csv


The dataset simulates:
- Revenue growth
- Profitability fluctuations
- Balance sheet expansion
- Post-downturn recovery patterns

---

## 🧠 Financial Analysis Framework

The dashboard is structured into standard financial analysis sections:

### 🔹 Profitability
- ROE
- ROA
- Net Profit Margin
- EBITDA Margin (if available)

### 🔹 Liquidity
- Current Ratio (if available)

### 🔹 Leverage
- Debt–Equity Ratio

This structure mirrors professional financial statement analysis practices.

---

## 🖥️ How to Run the Application

### 1️⃣ Clone the Repository
```
git clone https://github.com/tanishk49/Financial-Statement-Analyzer.git
cd Financial-Statement-Analyzer
```
### 2️⃣ Create & Activate Virtual Environment
```
python -m venv venv
venv\Scriptsactivate
```
### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
### 4️⃣ Run the Application
```
python app.py
```
