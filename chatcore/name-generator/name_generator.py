with open("Name", "r") as file:
    lines = file.readlines()
    list = [line.strip() for line in lines]

with open("Ten", "w") as file:
    for x in list:
        file.write(f"- Tôi là [{x}](\"entity\": \"cust_name\").\n")