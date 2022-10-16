'''
Reece Williams | 2022-Sept-17
Iterates over JUNO's data in the all_data json file & gets information about transactions
'''

import pprint
import base64
import ijson # pip install ijson
import json
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

ALL_MSGS = {}

all_data = os.path.join(current_dir, 'all_data.json')
with open(all_data, 'rb') as f:
    print('Parsing all_data.json...')
    parser = ijson.kvitems(f, "")

    for idx, (height, value) in enumerate(parser):
        if len(value['decoded_txs']) == 0:
            continue
        # 4570598 {
        # 'time': '2022-08-29T04:46:40.171071833Z', 
        # 'num_txs': 1, 
        # 'decoded_txs': [{msg_here}]
        
        
        for msg in value['decoded_txs']:            
            # decoded_tx = str(base64.b64decode(tx))
            msg_type = msg["@type"]     
            msg['height'] = height       

            ALL_MSGS[msg_type] = ALL_MSGS.get(msg_type, []) + [msg]
            

        if idx % 10_000 == 0:
            print(f'Parsed {idx} blocks so far')


msgs_dir = "msgs"
if not os.path.exists(msgs_dir):
    os.makedirs(msgs_dir, exist_ok=True)

for msg_type in ALL_MSGS.keys():      
    loc = os.path.join(current_dir, msgs_dir, f"{msg_type[1:]}.json")
    with open(loc, 'w') as f:
        print(f'Dumping {msg_type} to {loc}...')
        # json.dump(ALL_MSGS[msg_type], f, indent=4)
        json.dump(ALL_MSGS[msg_type], f)