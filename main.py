import os
import json
import requests
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("ETHERSCAN_API_KEY")
TOKEN_CONTRACT = "0x940a2db1b7008b6c776d4faaca729d6d4a4aa551"
BLOCK_RANGE = 100000  # Adjust the block range as needed

def fetch_transactions_by_block_range(start_block, end_block):
    transactions = []
    page = 1
    while True:
        print(f"Fetching page {page} for block range {start_block} to {end_block}...")
        response = requests.get(
            f"https://api.etherscan.io/api",
            params={
                "module": "account",
                "action": "tokentx",
                "contractaddress": TOKEN_CONTRACT,
                "startblock": start_block,
                "endblock": end_block,
                "page": page,
                "offset": 1000,
                "sort": "asc",
                "apikey": API_KEY
            },
        )
        try:
            data = response.json()
            if data.get("status") != "1" or "result" not in data:
                print(f"Unexpected API response: {data}")
                break

            # Append transactions to the list
            new_transactions = data['result']
            if not new_transactions:
                break
            transactions.extend(new_transactions)

            # Stop if fewer than 1000 transactions are returned
            if len(new_transactions) < 1000:
                break

            page += 1
        except Exception as e:
            print(f"Error fetching or processing page {page} for block range {start_block} to {end_block}: {e}")
            break

    print(f"Fetched {len(transactions)} transactions for block range {start_block} to {end_block}.")
    return transactions

def fetch_all_transactions():
    all_transactions = []
    current_block = 0
    latest_block = get_latest_block()

    while current_block < latest_block:
        next_block = min(current_block + BLOCK_RANGE, latest_block)
        transactions = fetch_transactions_by_block_range(current_block, next_block)
        all_transactions.extend(transactions)
        current_block = next_block + 1

    return all_transactions

def get_latest_block():
    print("Fetching the latest block number...")
    response = requests.get(
        f"https://api.etherscan.io/api",
        params={
            "module": "proxy",
            "action": "eth_blockNumber",
            "apikey": API_KEY
        },
    )
    try:
        data = response.json()
        if "result" in data:
            latest_block = int(data["result"], 16)  # Convert hexadecimal to decimal
            print(f"Latest block number fetched: {latest_block}")
            return latest_block
        else:
            raise ValueError(f"API response does not contain 'result': {data}")
    except Exception as e:
        raise ValueError(f"Error fetching latest block: {e}")

def save_transactions_to_file(transactions, filename="all_transactions.json"):
    with open(filename, "w") as file:
        json.dump(transactions, file, indent=4)
    print(f"Transactions saved to {filename}")

def main():
    all_transactions = fetch_all_transactions()
    if all_transactions:
        save_transactions_to_file(all_transactions)
    else:
        print("No transactions fetched.")

if __name__ == "__main__":
    main()
