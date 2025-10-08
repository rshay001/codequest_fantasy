# Day 2 — The Locked Door

Deeper inside the castle, Link finds a massive door sealed with glowing runes.
A nearby pedestal holds another stone tablet, marked “Unit.”
When he touches it, lines of symbols appear:
```
#*#**###*#*##

***##

#*#*#*
```
At the bottom, faint text reads:

<blockquote>“Each line shows a failed attempt to open the door.<br>
# marks a strike of the red rune, * a strike of the blue rune.<br>
For each attempt, multiply the red strikes by the blue strikes.<br>
The door’s key number is the sum of all results.”</blockquote>

Examples:
<blockquote>
Line 1: #*# has 2 red (#) and 1 blue (*): 2 × 1 = 2 <br>
Line 2: ***## has 2 red (#) and 3 blue (*): 2 × 3 = 6 <br>
Line 3: #*#*#* has 3 red (#) and 3 blue (*): 3 × 3 = 9 <br>
</blockquote>
Total: 2 + 6 + 9 = 17

Link must calculate the total key number to unlock the door.

###Hints:

Process each line separately using a loop
For each line: red_count * blue_count
Add each result to a running total
The final sum is the apartment number