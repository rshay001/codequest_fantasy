# Day 2 — Which unit

Flipping it over, he finds another cryptic message: multiple lines of mixed symbols like:
```
#*#**###*#*##

***##

#*#*#*
```



At the bottom of the card, there's a note in small print:

"The suspect tried multiple keypad combinations before getting into their apartment. Each line represents one attempt: # means 'press the red button' and * means 'press the blue button'. For each attempt, multiply the red presses by the blue presses. The apartment number equals the sum of all these multiplication results."

Examples:
```
Line 1: #*# has 2 red (#) and 1 blue (*): 2 × 1 = 2
Line 2: ***## has 2 red (#) and 3 blue (*): 2 × 3 = 6
Line 3: #*#*#* has 3 red (#) and 3 blue (*): 3 × 3 = 9
```
Total apartment number: 2 + 6 + 9 = 17
Detective Yolo needs to process each keypad attempt, calculate the result for each line, then add them all together to get the final apartment number.

Your task: For each line of symbols, count the red (#) and blue (*) presses, multiply them together, then sum all the results to find Detective Yolo's target apartment number.

###Hints:

Process each line separately using a loop
For each line: red_count * blue_count
Add each result to a running total
The final sum is the apartment number