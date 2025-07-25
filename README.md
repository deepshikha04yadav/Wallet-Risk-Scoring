# Wallet-risk-score

This project fetches on‑chain Compound V2/V3 transaction data for a set of Ethereum wallets, engineers features to capture their lending/borrowing behavior, and computes a 0–1000 risk score based on repayment habits, activity patterns, and liquidation history.

---

## 📂 Repository Structure

```
wallet-risk-scoring/
│
├── data/
│ ├── compound_wallet_transactions.json   # Raw JSON from fetch_compound.py
│ ├── filtered_compound_transactions.csv   # Flat CSV output of filter_compound_transaction.py
│ ├── Wallet-id.csv   # Original list of 100 wallet addresses
│ └── wallet_features.csv   # Per‑wallet features from feature_engineering.py
│
├── notebooks/
│ └── analysis.ipynb 
│
├── src/
│ ├── fetch_compound.py   # Pulls tx history via Etherscan
│ ├── filter_compound_transaction.py   # Filters & flattens relevant Compound txs to CSV
│ ├── feature_engineering.py   # Aggregates & computes numeric features per wallet
│ └── scoring_model.py   # Normalizes features, computes risk scores 0–1000
│
├── output/
│ ├── wallet_scores.csv # Final deliverable: wallet_id,score
| ├── plot.png
| └── score_histogra.png
│
├── requirements.txt
└── README.md 
```


---

## ⚙️ Prerequisites

- Python 3.8 or higher  
- Install dependencies:
```bash
  pip install -r requirements.txt
```
- Obtain an API key for your chosen data source (Etherscan) and set as an environment variable:
```
export ETHERSCAN_API_KEY=your_api_key_here
```
