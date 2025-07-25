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

## 🚀 Workflow & Usage
1. Fetch raw transactions
```
python src/fetch_compound.py \
  --input data/wallet_list.csv \
  --output data/raw/compound_wallet_transactions.json
```
Retrieves all Compound V2/V3 events (supply, borrow, repay, withdraw, liquidate) for each wallet.

2. Filter & flatten
```
python src/filter_compound_transaction.py
```
Reads raw JSON, extracts only relevant function calls, and writes a flat CSV at data/filtered_compound_transactions.csv.

3. Feature engineering
```
python src/feature_engineering.py
```
Aggregates per‑wallet metrics (total borrowed, repay count, liquidation count, activity span, etc.) into data/wallet_features.csv.

4. Compute risk scores
```
python src/scoring_model.py --normalize zscore --debug
```
* Normalizes selected features (net_borrowed, avg_time_between_tx, liquidation_count, borrow_count)

* Applies weighted formula → integer score [0, 1000]

* Outputs output/wallet_scores.csv.

5. Analyze & visualize

* Open notebooks/analysis.ipynb in Jupyter or VS Code.

* Inspect histograms, top‑10 bar charts, and write your interpretations.
