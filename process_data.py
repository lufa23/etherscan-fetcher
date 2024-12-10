import json
import pandas as pd

# Load the JSON file
with open("all_transactions.json", "r") as file:
    data = json.load(file)

# Convert to DataFrame
df = pd.DataFrame(data)

# Ensure 'timeStamp' exists and filter by date
if 'timeStamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timeStamp'].astype(int), unit='s')
    filtered = df[(df['timestamp'] >= '2024-09-01') & (df['timestamp'] <= '2024-12-31')]

# Aggregate daily data
daily_data = filtered.groupby(filtered['timestamp'].dt.date).agg(
    tx_count=('hash', 'count'),
    active_users=('from', 'nunique')
).reset_index()

# Save the result to CSV
daily_data.to_csv("daily_data.csv", index=False)

print("Filtered and aggregated data saved to daily_data.csv")
