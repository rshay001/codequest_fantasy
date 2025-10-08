with open("inputs/day02.txt","r") as file:
    input_data = file.read().strip()

lines = input_data.split("\n")

total = 0

for line in lines:
    count_red = line.count("#")
    count_blue = line.count("*")
    total += count_red * count_blue

print(f"The apartment umber is {total}")
