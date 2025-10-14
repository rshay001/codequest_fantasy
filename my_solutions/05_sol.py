with open('inputs/day05.txt','r') as f:
    lines=f.read().split()
print(type(lines))

pos = (0,0)
steps = 0
visited = {(0,0)}
r=0
c=0
for char in lines[0]:
    #print(char)
    if char == '>':
        c+=1
    elif char == '<':
        c-=1
    elif char == 'v':
        r+=1
    elif char == '^':
        r-=1
    visited.add((r,c))

print(len(visited))