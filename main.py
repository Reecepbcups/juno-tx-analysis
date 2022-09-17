import os
import sys
import json
import httpx
import base64

RPC = "https://rpc.juno.strange.love"
LOWEST_HEIGHT = 4444463 # https://rpc.juno.strange.love/block?height=2000000

client = httpx.Client()

current_dir = os.path.dirname(os.path.realpath(__file__))

# Pulled from racoon.bet RPC queries via inspect element
list_of_racoon_contracts = {
    # Dungeon
    "juno1ft5nuq4ck8ucwaunv0l064e22gw4lndexswqu5772mslgvf43ymqsgxznw": "DungeonV1",  
    "juno1an55u6dmsuw9etmyw3pccjn2qm4uddnyu4c6yusc8y5mdf77yjlq9p4k9y": "Dungeon V2",  
    # Lotto  
    "juno1mpufvc3j6v2zc2959lf838lnfv80c3hscgpfzqzkezyeceth9z6s37yeck": "LottoV1",
    "juno1sr4d0lq5njnfs0l59u92cerhr24zkczysxft4rvaas6gw3zt9lhqju02x4": "LottoV2",  
    "juno1r4pzw8f9z0sypct5l9j906d47z998ulwvhvqe5xdwgy8wf84583sxwh0pa": "Lottery Buy Ticket Rac",
    # dice
    "juno1xkvhguzrectvswn6f20t4gggs8wl70sj2rd5rt3trl73fjn8666qer96u0": "DiceV1",
    "juno18hsatg55uk7sf2hm0j36402aej729g395egq9rt5rjvz7gazdfcss9egmd": "Dice V2",
    # slots (excludes empowered spin Txs)
    "juno1wgkhhyf5zg2pxfxfzmq7rtx7jx5r294m2kudq3vqktfua5jay6xs04375w": "Slots",
}

TOTAL_RAC_TXS = 0
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
    
    # loop through blocks backwards from latest to LOWEST_HEIGHT
    # for idx, block_h in enumerate(range(latest, LOWEST_HEIGHT, -1)):    
    for idx, block_h in enumerate(range(start, start-spread, -1)):     
        if idx % (spread/10) == 0:            
                with open(os.path.join(current_dir, "data", f"blocks_{block_h}.json"), "w") as f:
                    json.dump(data, f, indent=4)
                    data = {}
        get_block_data(block_h)



def get_block_data(height):
    global TOTAL_RAC_TXS, TOTAL_JUNO_TXS, data    
    block = get_block(height)
    get_time = block["header"]["time"]
    txs = block["data"]["txs"]
    num_txs = len(txs)
    # print(f"Block {height} has {num_txs} transactions. Time: {get_time}")

    before_rac_txs = TOTAL_RAC_TXS
    contracts_in_block = {}

    # loop through txs, and decode base64
    for tx in txs:
        TOTAL_JUNO_TXS += 1
        decoded = str(base64.b64decode(tx))

        # check if any list_of_racoon_contracts keys are in the decoded tx
        for key in list_of_racoon_contracts:
            if key in decoded:
                TOTAL_RAC_TXS += 1                
                contracts_in_block[key] = contracts_in_block.get(key, 0) + 1
                # print(f"Found {key} in {decoded}")

    after = TOTAL_RAC_TXS - before_rac_txs

    data[height] = {
        "time": get_time,
        "num_txs": num_txs,
        "rac_txs": after,
        "contract_addrs": contracts_in_block   
    }

    if height % 250 == 0:
        print(f"[{height}] RacTXs So Far: {TOTAL_RAC_TXS}. Total Juno: {TOTAL_JUNO_TXS}")


# == RPC Logic ==
def get_latest_height():    
    resp = client.get(f"{RPC}/abci_info")    
    height = int(resp.json()["result"]["response"]["last_block_height"])
    # round height down to nearest 100 for sake of file formatting
    height = height - (height % 100)
    return height

def get_block(height):
    # TODO: try catch if fail
    resp = client.get(f"{RPC}/block?height={height}")
    return resp.json()["result"]["block"]


if __name__ == "__main__":
    main()
