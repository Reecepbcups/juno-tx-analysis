import os
import sys
import json
import httpx
import base64

RPC = "https://rpc.juno.strange.love"
LOWEST_HEIGHT = 4444463 # https://rpc.juno.strange.love/block?height=2000000

client = httpx.Client()

current_dir = os.path.dirname(os.path.realpath(__file__))


# TOTAL_RAC_TXS = 0
TOTAL_JUNO_TXS = 0
data = {} # int(height) = {other_data_here}

def main():
    global data

    # latest = int(get_latest_height())
    # print("Latest" + str(latest))

    start = int(sys.argv[1]) # starting height
    # end = int(sys.argv[2]) # start - spread
    spread = int(sys.argv[2]) #10k

    os.makedirs(os.path.join(current_dir, "data"), exist_ok=True)

    save_per = 500
    if spread < save_per:
        save_per = spread
    
    # loop through blocks backwards from latest to LOWEST_HEIGHT
    # for idx, block_h in enumerate(range(latest, LOWEST_HEIGHT, -1)):    
    for idx, block_h in enumerate(range(start, start-spread, -1)):     
        if idx % (save_per) == 0:            
            if len(data) == 0:
                # print(f"{block_h} was empty")
                pass
            else:
                with open(os.path.join(current_dir, "data", f"blocks_{block_h}.json"), "w") as f:
                    json.dump(data, f, indent=4)
                    data = {}
        get_block_data(block_h)



def get_block_data(height):
    # global TOTAL_RAC_TXS
    global TOTAL_JUNO_TXS, data    
    block = get_block(height)

    if block == -2: # height too low
        return
    if block == -1: # error getting block
        return

    get_time = block["header"]["time"]
    txs = block["data"]["txs"]
    num_txs = len(txs)
    # print(f"Block {height} has {num_txs} transactions. Time: {get_time}")

    # before_rac_txs = TOTAL_RAC_TXS
    contracts_in_block = {}

    # loop through txs, and decode base64
    TOTAL_JUNO_TXS += num_txs

    # for tx in txs:
    #     TOTAL_JUNO_TXS += 1
    #     decoded = str(base64.b64decode(tx))
    #     # check if any list_of_racoon_contracts keys are in the decoded tx
    #     for key in list_of_racoon_contracts:
    #         if key in decoded:
    #             TOTAL_RAC_TXS += 1                
    #             contracts_in_block[key] = contracts_in_block.get(key, 0) + 1
    #             # print(f"Found {key} in {decoded}")

    # after = TOTAL_RAC_TXS - before_rac_txs

    data[height] = {
        "time": get_time,
        "num_txs": num_txs,
        "juno_txs": txs, # base64 encoded
    }

    if height % 500 == 0:
        print(f"[{height}] Total Juno: {TOTAL_JUNO_TXS}")


# == RPC Logic ==
def get_latest_height():    
    resp = client.get(f"{RPC}/abci_info")    
    height = int(resp.json()["result"]["response"]["last_block_height"])
    # round height down to nearest 100 for sake of file formatting
    height = height - (height % 100)
    return height

def get_block(height) -> int:
    if height < LOWEST_HEIGHT:
        # print("Height too low")
        return -2

    try:
        resp = client.get(f"{RPC}/block?height={height}")
        return resp.json()["result"]["block"]
    except Exception as e:
        # print(f"Error getting block {height}")
        # print(f"Error getting block {height}. {e}")
        return -1


if __name__ == "__main__":
    main()
