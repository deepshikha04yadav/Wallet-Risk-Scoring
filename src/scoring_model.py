import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

INPUT_FEATURES = "data/wallet_features.csv"
OUTPUT_SCORES = "output/wallet_scores.csv"

def load_features():
    df = pd.read_csv(INPUT_FEATURES)

    # Derived features
    df["net_borrowed"] = df["total_borrow_value"] - df["total_repay_value"]
    df["avg_time_between_tx"] = (df["last_tx_time"] - df["first_tx_time"]) / df["total_tx_count"].clip(lower=1)

    return df

def normalize_features(df, feature_cols, method="minmax", debug=False):
    if method == "minmax":
        scaler = MinMaxScaler()
    elif method == "zscore":
        scaler = StandardScaler()
    else:
        raise ValueError("Unsupported normalization method. Use 'minmax' or 'zscore'.")

    scaled_data = scaler.fit_transform(df[feature_cols])
    norm_cols = [f"{col}_norm" for col in feature_cols]
    norm_df = pd.DataFrame(scaled_data, columns=norm_cols)

    if debug:
        print("\n Feature Normalization Preview:")
        for col, norm_col in zip(feature_cols, norm_cols):
            print(f"{col}: min={df[col].min()}, max={df[col].max()}, norm → {norm_col}")

    return pd.concat([df.reset_index(drop=True), norm_df], axis=1)

def compute_score(df, debug=False):
    # Define feature weights
    weights = {
        "net_borrowed_norm": 0.4,
        "avg_time_between_tx_norm": 0.3,
        "liquidation_count_norm": 0.2,
        "borrow_count_norm": 0.1
    }

    df["score"] = sum(df[feat] * weight for feat, weight in weights.items())
    df["score"] = (df["score"] * 1000).clip(0, 1000).astype(int)

    if debug:
        print("\n Sample Wallet Scores:")
        print(df[["wallet_address", "score"]].sort_values(by="score", ascending=False).head(5))

    return df[["wallet_address", "score"]]

def main(normalization_method="minmax", debug=False):
    df = load_features()

    features_to_normalize = [
        "net_borrowed",
        "avg_time_between_tx",
        "liquidation_count",
        "borrow_count"
    ]

    df = normalize_features(df, features_to_normalize, method=normalization_method, debug=debug)
    score_df = compute_score(df, debug=debug)

    score_df.to_csv(OUTPUT_SCORES, index=False)
    print(f"\n Wallet scores saved to: {OUTPUT_SCORES}")

if __name__ == "__main__":
    # Change these as needed
    main(normalization_method="zscore", debug=True)
