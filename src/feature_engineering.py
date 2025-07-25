import pandas as pd
from pathlib import Path

INPUT_CSV = "data/filtered_compound_transactions.csv"
OUTPUT_FEATURES = "data/wallet_features.csv"

def load_data():
    return pd.read_csv(INPUT_CSV)

def compute_features(df):
    features = []

    # Convert timestamp to numeric (if not already)
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors="coerce")

    # Group by wallet
    grouped = df.groupby("wallet_address")

    for wallet, group in grouped:
        feature_dict = {"wallet_address": wallet}

        # Total value per tx_type
        for tx_type in ["supply", "borrow", "repay", "withdraw", "liquidation"]:
            txs = group[group["tx_type"] == tx_type]
            total_value = txs["value"].astype(float).sum()
            tx_count = len(txs)
            feature_dict[f"total_{tx_type}_value"] = total_value
            feature_dict[f"{tx_type}_count"] = tx_count

        # Activity metrics
        feature_dict["first_tx_time"] = group["timestamp"].min()
        feature_dict["last_tx_time"] = group["timestamp"].max()
        feature_dict["total_tx_count"] = len(group)
        feature_dict["unique_functions"] = group["functionName"].nunique()

        features.append(feature_dict)

    return pd.DataFrame(features)

def main():
    df = load_data()
    features_df = compute_features(df)
    features_df.to_csv(OUTPUT_FEATURES, index=False)
    print(f"Feature-engineered data saved to {OUTPUT_FEATURES}")

if __name__ == "__main__":
    main()
