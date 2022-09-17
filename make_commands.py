'''
Makes commands since python has GIL bleh
'''

# https://rpc.juno.strange.love/abci_info?
start_height = 4845300
end_height = 4444500 # 27 days ago
spread = 10_000

# loop between start and end height and make the commands
output = []
for height in range(start_height, end_height, -spread):
    # print(f"python3 main.py {height} {spread}")    
    output.append(f"python3 main.py {height} {spread}")

# save output to txt file in this dir
with open("commands.txt", "w") as f:
    f.write("\n".join(output))