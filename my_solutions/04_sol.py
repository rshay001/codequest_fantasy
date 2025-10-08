with open('inputs/day04.txt','r') as file:
    input_data = file.read().strip()

lines = input_data.split('\n')

safe_count = 0

for word in lines:
    if len(word) == len(set(word)):
        safe_count += 1

print(f"Answer: {safe_count}")