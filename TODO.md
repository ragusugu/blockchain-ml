# Project Tasks

## TODO
- [ ] **Implement MCP Server for Blockchain RPC Data**
  - Connect to a blockchain RPC endpoint (e.g. Alchemy, Infura, or local node) using `web3.py`.
  - Set up an MCP Server using the `mcp` SDK (e.g. `fastmcp`).
  - Expose tools to fetch blockchain data directly:
    - `get_transaction(tx_hash)` to retrieve details by transaction hash.
    - `get_latest_block_number()` to fetch the latest block.
    - Additional tools to inspect smart contract states or balances as needed.
  - Integrate with the AI fraud detection system to provide interactive, real-time contextual context for transactions.
