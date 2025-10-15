with open('inputs/day06.txt') as f:
    inputs = f.read().splitlines()

def understand_data():
    ln=0
    for line in inputs:
        i=0
        print("line: ",ln)
        for ele in line.split():
            print(i, ele) 
            i+=1
        ln+=1

#understand_data()

#make a grid
grid = {}
r = 0
for line in inputs:
    c=0
    for char in line:
        grid[r,c] = char
        c+=1
    r+=1
#print(grid)
    
#Find the starting coordinate (from the bottom)    
key = next(k for k, v in grid.items() if v=='S')
print(f'key is: {key}')

def walk(coor):
    r,c = coor
    while r>1:   
        print(f'beginning: ',{r},{c})  
        if grid.get((r,c-1)) == '-':
            #print(f'left: r, c=',{r},{c})
            r=r-1
            c = c-2
            #print(f'After left: r, c=',{r},{c})
        elif grid.get((r,c+1)) == '-':
            #print(f'right: r,c=',{r},{c})
            r=r-1
            c = c+2
            #print(f'after right: r,c=',{r},{c})
        else:
            #print(f'straight: r,c=',{r},{c})
            r= r-1
            #print(f'after straight: r,c=',{r},{c})
       # print(f'existing:',{r},{c})
    return((r-1,c),(r,c))

fir_num, sec_num = walk(key)
print(fir_num, sec_num)
print(f'========answer: {grid[fir_num]},{grid[sec_num]}')
