import json
import pandas as pd
from pathlib import Path

INPUT_PATH = "data/compound_wallet_transactions.json"
OUTPUT_PATH = "data/filtered_compound_transactions.csv"

# Keyword mapping
KEYWORDS = {
    "supply": ["mint", "supply", "addliquidity", "deposit"],
    "borrow": ["borrow"],
    "repay": ["repay"],
    "withdraw": ["redeem", "withdraw", "removeliquidity"],
    "liquidation": ["liquidate"],
}

def detect_tx_type(function_name):
    function_name = function_name.lower()
    for tx_type, keywords in KEYWORDS.items():
        if any(kw in function_name for kw in keywords):
            return tx_type
    return None

def filter_and_flatten(raw_data):
    rows = []
    for wallet, txs in raw_data.items():
        for tx in txs:
            fname = tx.get("functionName", "").lower()
            tx_type = detect_tx_type(fname)
            if not tx_type:
                continue  # skip irrelevant tx

            row = {
                "wallet_address": wallet,
                "tx_type": tx_type,
                "timestamp": tx.get("timeStamp"),
                "value": tx.get("value"),
                "gasUsed": tx.get("gasUsed"),
                "functionName": tx.get("functionName"),
                "blockNumber": tx.get("blockNumber"),
                "hash": tx.get("hash"),
                "from": tx.get("from"),
                "to": tx.get("to"),
            }
            rows.append(row)
    return rows

def main():
    with open(INPUT_PATH, "r") as f:
        raw_data = json.load(f)

    flat_rows = filter_and_flatten(raw_data)
    df = pd.DataFrame(flat_rows)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"[✔] Filtered & flattened CSV saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
