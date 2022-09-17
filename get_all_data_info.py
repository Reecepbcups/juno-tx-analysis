# load all_data.json

import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(current_dir, "all_data.json"), 'r') as f:
    all_data = dict(json.load(f))


DATA = {
    "total_txs": 0,
    "rac_txs": 0,
    "contract_addrs": {}
}

# loop through all keys
for height, v in all_data.items():
    # print key
    # print(height, "\n", v)
    # input()
    DATA['total_txs'] = DATA.get('total_txs', 0) + v['num_txs']
    DATA['rac_txs'] = DATA.get('rac_txs', 0) + v['rac_txs']
    
    if len(v['contract_addrs']) > 0:
        for addr, amt in v['contract_addrs'].items():
            DATA['contract_addrs'][addr] = DATA['contract_addrs'].get(addr, 0) + amt

    # input()

# dump data to file
with open(os.path.join(current_dir, "final.json"), 'w') as f:
    json.dump(DATA, f, indent=4)