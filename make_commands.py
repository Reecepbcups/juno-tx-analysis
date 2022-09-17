'''
Makes commands since python has GIL bleh
'''

# https://rpc.juno.strange.love/abci_info?
start_height = 4846600
end_height = 4446200 # 27 days ago
spread = 5_000

# loop between start and end height and make the commands
output = []
for height in range(start_height, end_height, -spread):
    # print(f"python3 main.py {height} {spread}")    
    # output.append(f"python3 main.py {height} {spread} &")
    if height - spread < end_height:
        spread = height - end_height
    output.append(f"python3 main.py {height} {spread} &") # kill python3 to stop since httpx & background

# save output to txt file in this dir
with open("commands.sh", "w") as f:
    f.write("\n".join(output))