## juno-txs
Counting number of Txs per block for the RAC community.

Solution:
- Use RPC / REST to query every block.
- Saves every XXXXX blocks to a JSON file with the data we want, using height as the key.
- Set of contract addresses which are Rac based (from their games). If it is one, we count it.

Todo:
- save all blocks & txs to files then combine to be nice to RPC endpoints.