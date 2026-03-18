# Project Tasks

## TODO
- [x] **Implement MCP Server for Blockchain RPC Data**
  - Connect to a blockchain RPC endpoint (e.g. Alchemy, Infura, or local node) using `web3.py`.
  - Set up an MCP Server using the `mcp` SDK (e.g. `fastmcp`).
  - Expose tools to fetch blockchain data directly:
    - `get_transaction(tx_hash)` to retrieve details by transaction hash.
    - `get_latest_block_number()` to fetch the latest block.
    - `get_block(block_number)` to fetch block details.
    - `get_address_balance(address)` to check ETH balance.
    - `get_address_tx_count(address)` to get transaction count.
    - `analyse_transaction_fraud(tx_hash)` to run AI fraud detection.
    - `get_model_info()` to retrieve model metrics.
  - Integrated with the AI fraud detection system for interactive analysis.
  - **Implementation:** `src/backend/mcp_server.py`
