import random

data = [
    ["Shirt", 1000, 2000, "Store_1"],
    ["Shirt", 1500, 3000, "Store_2"],
    ["Pant", 2000, 4000, "Store_3"],
    ["Shalwar_Kameez", 2500, 5000, "Store_4"],
    ["Pant", 3000, 6000, "Store_5"],
    ["Shirt", 3500, 7000, "Store_6"],
    ["Shalwar_Kameez", 4000, 8000, "Store_7"],
    ["Pant", 4500, 9000, "Store_8"],
    ["Shirt", 5000, 10000, "Store_9"],
    ["Shirt", 1500, 6000, "Store_10"],
    ["Pant", 3500, 7000, "Store_11"],
    ["Shalwar_Kameez", 5000, 9000, "Store_12"],
    ["Shalwar_Kameez", 1000, 15000, "Store_13"],
    ["Shirt", 2500, 6000, "Store_14"],
    ["Pant", 3500, 11000, "Store_15"],
    ["Shalwar_Kameez", 5000, 12000, "Store_16"],
    ["Shalwar_Kameez", 3000, 9000, "Store_17"],
    ["Shirt", 7000, 16000, "Store_18"],
    ["Pant", 8500, 15000, "Store_19"],
    ["Pant", 7500, 17000, "Store_20"]
    ]

def generate_price(min_price, max_price):
    return random.randint(min_price, max_price)

records = []
for _ in range(200):
    category, min_price, max_price, store_name = random.choice(data)
    new_price = generate_price(min_price, max_price)
    records.append([category, new_price, new_price + 5000, store_name])  # Increase max_price by 1000 for variation

with open("data.csv", "w") as file:
    file.write("category,min_price,max_price,store_name\n")
    for record in records:
        file.write(",".join(map(str, record)) + "\n")
