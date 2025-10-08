with open("inputs/day01.txt","r") as file:
    input_data = file.text.strip()

count = 0
pos = 0
for char in input_data:
    pos+=1
    if char=="(":
        count+=1
    elif char==")":
        count-=1
        

print(f"part 1 answer: {count}")