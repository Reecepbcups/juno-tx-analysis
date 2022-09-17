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

MSGS = {            
    "cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward": {},
    "cosmos.distribution.v1beta1.SetWithdrawAddress": {},
    "cosmos.distribution.v1beta1.WithdrawValidatorCommission": {},
    "cosmos.staking.v1beta1.MsgDelegate": {},
    "cosmos.staking.v1beta1.MsgUndelegate": {},
    "cosmos.staking.v1beta1.MsgBeginRedelegate": {},
    "cosmos.authz.v1beta1.MsgExec": {},
    "cosmos.authz.v1beta1.MsgGrant": {},
    
    
    "cosmwasm.wasm.v1.MsgInstantiateContract": {},
    "cosmwasm.wasm.v1.MsgMigrateContract": {},
    "cosmwasm.wasm.v1.MsgExecuteContract": {},
    
    "cosmos.bank.v1beta1.MsgSend": {},
    
    "ibc.applications.transfer.v1.MsgTransfer": {},
    
    "other": {},
}

IGNORED = {
    "ibc.core.client.v1.MsgUpdateClient": {},
    "cosmwasm.wasm.v1.MsgStoreCode": {},
    "cosmos.staking.v1beta1.MsgCreateValidator": {},
    "cosmos.staking.v1beta1.MsgEditValidator": {},
    "cosmos.slashing.v1beta1.MsgUnjail": {},

    "ibc.core.channel.v1.MsgChannelOpenAck": {},
    "ibc.core.channel.v1.MsgChannelOpenInit": {},
    "ibc.core.client.v1.MsgCreateClient": {},

    "cosmos.gov.v1beta1.MsgSubmitProposal": {},
    "cosmos.gov.v1beta1.MsgDeposit": {},
}

all_data = os.path.join(current_dir, 'all_data.json')
with open(all_data, 'rb') as f:
    print('Parsing all_data.json...')
    parser = ijson.kvitems(f, "")


    for idx, (height, value) in enumerate(parser):
        if len(value['juno_txs']) == 0:
            continue
        # 4570598 {
        # 'time': '2022-08-29T04:46:40.171071833Z', 
        # 'num_txs': 1, 
        # 'juno_txs': ['CpMECo8CCiQvY29zbXdhc20ud2FzbS52MS5Nc2dFeGVjdXRlQ29udHJhY3QS5gEKK2p1bm8xcW5xd3hhenpoYTZsc3gycnMyZ2V3dTIzMzd1aGE1bHoyNGVwNDkSP2p1bm8xcjRwenc4Zjl6MHN5cGN0NWw5ajkwNmQ0N3o5OTh1bHd2aHZxZTV4ZHdneTh3Zjg0NTgzc3h3aDBwYRp2eyJpbmNyZWFzZV9hbGxvd2FuY2UiOnsiYW1vdW50IjoiNDgwMDY0Iiwic3BlbmRlciI6Imp1bm8xbTA4dm43a2x6eGg5dG1xd2FqdXV4MjAyeG1zMnF6M3Vja2xlN3p2dHR1cmNxN3ZrMnlhcXBjd3hseiJ9fQr+AQokL2Nvc213YXNtLndhc20udjEuTXNnRXhlY3V0ZUNvbnRyYWN0EtUBCitqdW5vMXFucXd4YXp6aGE2bHN4MnJzMmdld3UyMzM3dWhhNWx6MjRlcDQ5Ej9qdW5vMW0wOHZuN2tsenhoOXRtcXdhanV1eDIwMnhtczJxejN1Y2tsZTd6dnR0dXJjcTd2azJ5YXFwY3d4bHoaVXsiYWRkX2xpcXVpZGl0eSI6eyJ0b2tlbjFfYW1vdW50IjoiMzY0NDAiLCJtYXhfdG9rZW4yIjoiNDgwMDY0IiwibWluX2xpcXVpZGl0eSI6IjAifX0qDgoFdWp1bm8SBTM2NDQwEmgKUQpGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQOqslGEtljiHRL37XjdcvhLpToNT9j9LU4qfr+j4/hGoBIECgIIfxjJDxITCg0KBXVqdW5vEgQxNDYyEMLWIxpAIMv6R+Jdnw0Pyv/r3ACcd9xGN7byJ5wL8dKSAfVa0t0CrMqANGM1kIluHXMC/GDVL+XvScV5DJgKsl7R7t4F0g==']}

        height_txs = {}

        # WORKS
        for tx in value['juno_txs']:            
            decoded_tx = str(base64.b64decode(tx))

            wasFound = False
            for msg_type in MSGS.keys():
                if msg_type in decoded_tx and msg_type not in IGNORED.keys():
                    # FINAL_DATA[msg_type][height] = FINAL_DATA.get(msg_type, {}).get(height, {}) + [tx]                
                    height_txs[msg_type] = height_txs.get(msg_type, []) + [tx]
                    wasFound = True
                    break # beak inner loop
            if not wasFound:
                height_txs["other"] = height_txs.get("other", []) + [tx]            


        if idx % 1000:
            # update the main map only every 1000 blocks
            for msg in height_txs.keys():
                # MSGS[msg] = MSGS.get(msg, {})[str(height)] + [height_txs[msg]]
                values = MSGS.get(msg, {})
                values[height] = height_txs[msg]
                MSGS[msg] = values

        if idx % 10_000 == 0:
            print(f'Parsed {idx} blocks so far')


msgs_dir = "msgs"
if not os.path.exists(msgs_dir):
    os.makedirs(msgs_dir, exist_ok=True)

for msg_type in MSGS.keys():
    if msg_type in IGNORED.keys(): 
        continue
    with open(os.path.join(current_dir, msgs_dir, msg_type + ".json"), 'w') as f:
        print('Dumping ' + msg_type + ' to ' + os.path.join(current_dir, msgs_dir, msg_type + ".json") + '...')
        json.dump(MSGS[msg_type], f, indent=4)