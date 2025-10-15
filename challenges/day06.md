## Day 6: The Prize Lattice

After Link exits the maze, he emerges into a bustling open market filled with people, elves, and dwarves. Vendors hawk weapons, mysterious foods, and magical trinkets he has never seen before. 

One booth catches his attention immediately. Behind a wooden counter, stands a big, tall board with ropes that make a kind of a lattice pattern. Numbers 1 to 25 mark the starting positions, and letters A to Y line the bottom, each with a "prize" underneath. Some prizes look valuable, some look plain, some look outright nasty, like a box of worms under "W". Letter **S** makes Link's heart race. It is a magnificent sword with a beautifully carved silver handle, and a blade that gleams with an otherworldly dark purple radiance. Link wants the blade, not just for its appearance, but to protect himself on the journey of unknown.

The booth vendor, a grizzled dwarf, explains the rules:

<blockquote> "Pick any starting position (1-25) at the top. Follow the rope straight down. When you hit a horizontal line (`-`), you MUST follow it sideways to reach the next straightline, then continue down from that new column. You don't ever go back up, only down, left or right. Wherever you end up at the bottom, that's your prize - no exchanges, no refunds!" </blockquote>

### Example (simple 10-position board):

This practice board shows 10 starting positions. 
-If a user starts at #10 (displayed as 1 and 0 below), he'll get to E, which converts to a box of eggs. 
-If starting at 5, the user will get to C, which translates to a chic. 
-If starting at 3, the user will get to B, a bomb that will explode as soon as the player receives it.

```
0 0 0 0 0 0 0 0 0 1
1 2 3 4 5 6 7 8 9 0
| | | | | | | |-| | 
|-| | | | |-| | | | 
| |-| | | | |-| | | 
| | | |-| | | | |-| 
| | |-| | | | |-| | 
|-| | | | |-| | | | 
| | | | | | | | |-| 
| |-| | |-| |-| | | 
| | | | | | | | | | 
| | |-| | |-| |-| | 
| |-| | | | | | | | 
|-| | |-| | | | |-| 
| | | | |-| |-| | | 
A B C D E F G H I J
```

Help Link pick a position that will lead to **S**, the sword! Note, for 2-digit starting position, just enter it like a regular 2-digit number, like 10. Not 1, 0.

## **Hints**
Learn about Python dictionary. A dictionary has key: value pair, for example, a dictionary of student report card data may contain:
```python
report_cards={"Stitchy":20, "Baby Stitchy": 19, "Daddy Stitchy": 5}
``` 
in which "Stitchy" is the key and 20 is a value of of the key. This is a common setup for a grid problem. 

Here are some brief overview:<br>

- Creating and populating a dictionary:<br>
`report_cards = {} #declare an empty dictionary `

- Access value: <br>
`report_cards["Stitchy"] = 20`

- Look up value:

```python
    #Safe - returns None if key doesn't exist (no crash)
    if report_cards.get("Stitchy") == 20:
        # do something

    #Unsafe - crashes if key missing  
    if report_cards["Wild Stitchy"] == 12:    # KeyError if Wild Stitchy not a student
```
- Google how to find Keys by Value. For example, what if you want to know who in the class got 19?