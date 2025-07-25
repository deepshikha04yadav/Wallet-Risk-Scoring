import requests
import pandas as pd
from tqdm import tqdm
import time

ETHERSCAN_API_KEY = 'Q47WWYYFC89PFKG5B6ZCTR6UCKCMWEIW54'  # Replace this with your Etherscan API key
ETHERSCAN_URL = 'https://api.etherscan.io/api'

# Load wallet list
wallet_df = pd.read_csv('../data/Wallet-id.csv')
wallets = wallet_df.iloc[:, 0].tolist()

def get_normal_tx(wallet):
    """Fetch normal transactions for a given wallet."""
    url = ETHERSCAN_URL
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': wallet,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'asc',
        'apikey': ETHERSCAN_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data['result']
    except Exception as e:
        print(f"Error fetching data for {wallet}: {e}")
        return []

# Fetch transactions for all wallets
wallet_tx_data = {}
for wallet in tqdm(wallets, desc="Fetching transactions"):
    txs = get_normal_tx(wallet)
    wallet_tx_data[wallet] = txs
    time.sleep(0.2)  # To avoid rate limits (5 req/sec for Etherscan)

# Save as JSON
import json
with open('../data/compound_wallet_transactions.json', 'w') as f:
    json.dump(wallet_tx_data, f)

print("✅ Saved all transaction data to 'compound_wallet_transactions.json'")
