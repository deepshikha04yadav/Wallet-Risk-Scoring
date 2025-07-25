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
### 1. Fetch raw transactions
```
python src/fetch_compound.py \
  --input data/wallet_list.csv \
  --output data/raw/compound_wallet_transactions.json
```
Retrieves all Compound V2/V3 events (supply, borrow, repay, withdraw, liquidate) for each wallet.

### 2. Filter & flatten
```
python src/filter_compound_transaction.py
```
Reads raw JSON, extracts only relevant function calls, and writes a flat CSV at ```data/filtered_compound_transactions.csv```.

### 3. Feature engineering
```
python src/feature_engineering.py
```
Aggregates per‑wallet metrics (total borrowed, repay count, liquidation count, activity span, etc.) into ```data/wallet_features.csv```.

### 4. Compute risk scores
```
python src/scoring_model.py --normalize zscore --debug
```
* Normalizes selected features (net_borrowed, avg_time_between_tx, liquidation_count, borrow_count)

* Applies weighted formula → integer score [0, 1000]

* Outputs ```output/wallet_scores.csv```.

### 5. Analyze & visualize

* Open notebooks/analysis.ipynb in Jupyter or VS Code.

* Inspect histograms, top‑10 bar charts, and write your interpretations.

## 📑 Methodology
### 1. Data Collection
* Source: Etherscan API

* Scope: All mint/supply, borrow, repayBorrow, redeem/withdraw, liquidateBorrow events

### 2. Feature Selection

| __Feature__        	|  __Rationale__                                         |
| --------------------|--------------------------------------------------------|
| net_borrowed	      |  Unpaid loan principal ⇒ high values → higher risk    |
| borrow_count	      |  Frequency of borrow actions → potential over-leverage |
| liquidation_count   | 	Direct indicator of past defaults                    |
| avg_time_between_tx | 	Wallet engagement; long gaps → unmanaged positions   |
| total_tx_count	    |  Overall activity; more active → better risk management|
| unique_functions	  |  Protocol usage diversity → risk diversification       |

### 3. Normalization & Scoring
* Normalization: Min‑Max or Z‑Score to place features on comparable scales

* Weighted sum:
```
score_raw = 0.4·net_borrowed_norm
          + 0.1·borrow_count_norm
          + 0.2·liquidation_count_norm
          + 0.3·avg_time_between_tx_norm
score = clip(int(score_raw × 1000), 0, 1000)
```
* Interpretation:
  *  0 – 300 = Low risk
  *  301 – 700 = Medium risk
  *  701 – 1000 = High risk

## 📄 Deliverables
### 1. ```output/wallet_scores.csv```

| wallet_id                                   |	score |
| --------------------------------------------|-------|
| 0x0039f22efb07a647557c7c5d17854cfd6d489ef3	| 37    |
|  ...	                                      | ...   |

### 2. Brief Write‑Up

* __Data Collection:__ APIs used, query parameters, pagination

* __Feature Rationale:__ Why each metric correlates with risk

* __Scoring Logic:__ Normalization choice, weight justification

* __Scalability:__ Pipeline modularity, configuration flags, extensibility for other protocols

## 🔮 Future Work

* __Weight Optimization:__ Use backtesting on historical liquidation data or supervised learning with labeled defaults to fine-tune feature weights.

* __Enhanced Features:__ Incorporate collateral asset diversity, on-chain health factor trends, and external oracle price feeds.

* __Protocol Extension:__ Adapt the pipeline to other DeFi lending platforms (e.g., Aave, MakerDAO) with minimal changes.

* __Real-Time Scoring:__ Deploy as a real-time microservice with live event streaming, alerting on high-risk wallets.

## ✍️ Author Note

This risk-scoring pipeline is designed for clarity and modularity. Each step—from data ingestion to scoring—can be configured or swapped for alternative data sources and algorithms. Feel free to extend the codebase with additional indicators or integrate with dashboarding tools for richer insights.


