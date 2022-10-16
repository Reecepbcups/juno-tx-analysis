'''
Goal: Compare total network Txss for juno minus msgWithdrawDelegatorReward
'''

from cProfile import label
import os, json
import matplotlib.pyplot as plt

# loop through all msgs folder
current_dir = os.path.dirname(os.path.realpath(__file__))
total_msgs_file = f"{current_dir}/json/total_messages.json"

# make any dirs in path if they don't exist
for file in [total_msgs_file]:
    os.makedirs(os.path.dirname(file), exist_ok=True)    
    open(file, "w").close() # clear file

total_messages = {}
lowest_height = -1
highest_height = -1

def set_height(height):
    global lowest_height, highest_height
    height = int(height)
    if lowest_height == -1:
        lowest_height = height
    if highest_height == -1:
        highest_height = height
    if height < lowest_height:
        lowest_height = height
    if height > highest_height:
        highest_height = height    

# saves msg amounts by height to file
for file in os.listdir(f"{current_dir}/msgs"):
    if not file.endswith(".json"):
        continue

    print(f"Processing {file}")
    with open(f"{current_dir}/msgs/{file}", "r") as f:
        msg_list = json.load(f)    

    values_at_heights = {}
    for msg in msg_list:        
        height = msg["height"]   
        set_height(height)
        values_at_heights[height] = values_at_heights.get(height, 0) + 1
    total_messages[file] = values_at_heights

with open(total_msgs_file, "w") as f:
    json.dump(total_messages, f)

# exit()
# TODO calu

final_output = {}
# lowlow = 4_450_000
# highhigh = 4_850_000
range_jumps = 5_000 # maybe take a % of the highest height - lowest height

for msg_type, heights_data in total_messages.items():
    # {'4801196': 1, '4801189': 1, '4800030': 1}
    # sorted_heights = sorted(v.keys(), key=lambda x: x[0])
    # print(sorted_heights)
    if len(heights_data.keys()) == 0:
        continue

    all_txs = {k: 0 for k in range(lowest_height, highest_height, range_jumps)}

    for height, amt in heights_data.items():
        # find the closest key to k
        closest_height = min(all_txs, key=lambda x:abs(x-int(height)))
        # print(closest)

        # add the # of txs to the closest key
        # final_output[closest_height] = final_output.get(closest_height, 0) + amt
        all_txs[closest_height] = all_txs.get(closest_height, 0) + amt

    # print(final_output)
    # exit()

    name = msg_type.replace(".json", "")
    plt.plot(all_txs.keys(), all_txs.values(), label=name)    
    plt.legend(loc='upper left')
    plt.title(f'Juno Txs By Type')
    plt.xlabel('Block height')
    plt.ylabel('Txs Over Time')    
    
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
fig.savefig('test-juno_txs_over_time.png', dpi=100)