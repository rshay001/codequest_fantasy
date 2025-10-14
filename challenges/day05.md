# **Day 5 — The Hall of Maze**

Link follows a faint hum through a stone corridor that spirals downward until he reaches a vast, dark space, so large, he could barely see the edge of it. In front of him, there is a threshold, beyond which, the mud floor becomes tiled floor. Each tile is about just big enough for one step. He crosses the threshold and starts running, but every few steps there is an invisible wall that blocks him. After a few attempts, he goes back behind the threshold. It is a maze! But he can't find any instructions or hints.

Exhausted at this point, Link sits down and takes out a cupcake he packed for the journey. As he is about to take a bite, an ancient-looking faerie appeared, "what is that?" She eyes the cupcake and keeps licking her lips. "It's a chocolate cupcake." Link ereplied. "ooohhh... cupcake. I haven't had one for sooo long..." The faerie croacked. She is a tiny little thing, hair long and so white it looks silver.

Link gives her half of the cupcake, and she gobbles down the cupcake. "You are such a nice young man. You look like you're a little lost? I remember how to get out of the maze. I've done it... about 150 years ago. I can't go with you though. Only one can enter the maze at any time. But I'll give you directions from here."

Link hesitates, "150 years ago? Hmm is she sure she remembers the way?" But he doesn't have much choice, so off he goes. Her instructions are to the north (^), south (v), east (>), or west (<). With each move, Link lands on a tile.

The faerie's instruction, not at all surprising to Link, is not very accurate. He needs to double back many many times. But eventually he exists the maze safely.

How many spots has Link returned to at least **once**?

### Example

> lands on 2 tiles: one at the starting tile, and one to the east.
^>v< lands on 4 tiles, including twice to the same tile that he starts with
^v^v^v^v^v lands on only 2 tiles.

### **Hints**

```python
Learn about python Sets. One of the difference between Sets and Lists is that, members of Sets cannot be repeated. For example:
List can be ['a','a','b','b','c]
With the same inputs, set will be
['a','b','c']
```
