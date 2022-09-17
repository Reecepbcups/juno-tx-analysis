'''
Goal: Compare total network Txss for juno minus msgWithdrawDelegatorReward
'''

from cProfile import label
import os, json
import matplotlib.pyplot as plt

# loop through all msgs folder
current_dir = os.path.dirname(os.path.realpath(__file__))

total_messages = {}

# savesa msg amoutns by height to file
for file in os.listdir(f"{current_dir}/msgs"):
    if file.endswith(".json"):
        print(f"Processing {file}")
        with open(f"{current_dir}/msgs/{file}", "r") as f:
            data = json.load(f)     


        values_at_heights = {}
        for height, txs in data.items(): 
            # input(f"{height}, {len(txs)}")     
            # total_messages["total"] = total_messages.get("total", 0) + len(txs)
            
            num_of_txs = len(txs)
            total_messages[file] = {}
            # break

            # for each height, set height key = num of txs
            # total_messages[file][int(height)] = num_of_txs            
            values_at_heights[int(height)] = num_of_txs

        total_messages[file] = values_at_heights                
# 1,221,567 Total Messages
# dump to file, is in graphs/ now
# {'total': 1221567, 'cosmos.staking.v1beta1.MsgEditValidator.json': 17, 'cosmos.distribution.v1beta1.MsgWithdrawDelegatorReward.json': 252642, 'cosmos.staking.v1beta1.MsgDelegate.json': 172595, 'cosmos.authz.v1beta1.MsgGrant.json': 2070, 'cosmos.gov.v1beta1.MsgSubmitProposal.json': 2, 'cosmos.slashing.v1beta1.MsgUnjail.json': 6, 'other.json': 121783, 'ibc.core.client.v1.MsgCreateClient.json': 20, 'ibc.applications.transfer.v1.MsgTransfer.json': 61643, 'cosmos.bank.v1beta1.MsgSend.json': 52246, 'cosmos.gov.v1beta1.MsgDeposit.json': 18, 'cosmos.authz.v1beta1.MsgExec.json': 32, 'cosmos.staking.v1beta1.MsgUndelegate.json': 4678, 'cosmos.staking.v1beta1.MsgCreateValidator.json': 7, 'cosmwasm.wasm.v1.MsgMigrateContract.json': 25, 'cosmwasm.wasm.v1.MsgInstantiateContract.json': 508, 'ibc.core.channel.v1.MsgChannelOpenAck.json': 5, 'ibc.core.channel.v1.MsgChannelOpenInit.json': 5, 'cosmos.staking.v1beta1.MsgBeginRedelegate.json': 8492, 'cosmwasm.wasm.v1.MsgExecuteContract.json': 544773}
with open(f"{current_dir}/json/total_messages.json", "w") as f:
    json.dump(total_messages, f, indent=4)

filename = f"{current_dir}/json/messages_by_heights.json"
# with open(filename, "w") as f:
#     json.dump(total_messages, f)

# load filename to memory
with open(filename, "r") as f:
    total_messages = json.load(f)


final_output = {}
lowlow = 4_450_000
highhigh = 4_850_000
for k, v in total_messages.items():
    # sorted_heights = sorted(v.keys(), key=lambda x: x[0])
    # print(sorted_heights)
    if len(v.keys()) == 0:
        continue

    all_txs = {k: 0 for k in range(lowlow, highhigh, 5_000)}

    for height, amt in v.items():
        # find the closest key to k
        closest_height = min(all_txs, key=lambda x:abs(x-int(height)))
        # print(closest)

        # add the # of txs to the closest key
        # final_output[closest_height] = final_output.get(closest_height, 0) + amt
        all_txs[closest_height] = all_txs.get(closest_height, 0) + amt

    # print(final_output)
    # exit()

    name = k.replace(".json", "")
    plt.plot(all_txs.keys(), all_txs.values(), label=name)    
    plt.legend(loc='upper left')
    plt.title(f'Juno Txs By Type')
    plt.xlabel('Block height')
    plt.ylabel('Txs Over Time')    
    
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig('juno_txs_over_time.png', dpi=100)