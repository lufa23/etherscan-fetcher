#!/bin/bash

# Total number of chunks
CHUNKS=30

# File name of the JSON file
INPUT_FILE="all_transactions.json"

# Total length of the JSON array
LENGTH=$(jq 'length' "$INPUT_FILE")

# Length of each chunk
CHUNK_SIZE=$((LENGTH / CHUNKS))

# Generate chunks
for i in $(seq 0 $((CHUNKS - 1))); do
  START=$((i * CHUNK_SIZE))
  if [ "$i" -eq $((CHUNKS - 1)) ]; then
    # Last chunk includes all remaining elements
    END=""
  else
    END=$(((i + 1) * CHUNK_SIZE))
  fi
  jq ".[$START:$END]" "$INPUT_FILE" > "chunk_$((i + 1)).json"
done

