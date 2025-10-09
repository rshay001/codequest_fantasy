#Day 4 The Whispering Chamber

With a low rumble, the door creaks open. Link steps into a vast, silent hall lined with ancient banners. The air is thick with dust and faint whispers.
In the center of the room stands a circular stone table, with carved numbers around the edge of the table. Upon it lies a brittle scroll marked “The Chamber of Words.”
The scroll reads:
<blockquote>
Within this room, language itself has been bound by spells of silence.<br>
Each word holds either peace or danger.<br>
A safe word is one where no rune repeats.<br>
A cursed word repeats any rune twice.</blockquote>

At the bottom, written in fading ink:
<blockquote>Count only the safe words — for they reveal the secret number of this chamber.</blockquote>

###**Example:**

<blockquote>
room<br>
door<br>
lamp<br>
roar<br>
</blockquote>

Analysis:
<blockquote>
room → repeat “o” → cursed<br>
door → repeat “o” → cursed<br>
lamp → all unique → safe<br>
roar → repeat "r" → cursed<br>
</blockquote>

###**Hints:**
The basic method is to check character by character, and count the occurrance. 
A faster way is to utilize python's "sets". In a set, there cannot be any repeating element, so set of (a, p, p, l, e) will become (a,p,l,e)