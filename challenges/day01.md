# Day 1 — The Summons to the Castle

After a long journey through Hyrule, Link finally reaches the gates of the Forgotten Castle.
Princess Zelda’s letter was brief:

<blockquote><i>“Strange magic stirs beneath the old towers.<br>
Start from the ground floor. Follow the marks left behind.”</i></blockquote>

Inside the main hall, Link finds a stone tablet etched with a long string of symbols — nothing but curved carvings: ( and ).
A note beside it reads:

<blockquote><i>“The castle’s stairs rise with ( and descend with ).<br>

The ground floor is 0.<br>

The lowest chamber lies below the earth, and the upper towers reach toward the clouds.”</i></blockquote>
   
Link must follow the pattern to discover which floor the magic leads to.

For example:
<blockquote>
(()) and ()() both result in floor 0.<br>
((( and (()(()( both result in floor 3.<br>
))((((( also results in floor 3.<br>
()) and ))( both result in floor -1 (the first basement level).<br>
))) and )())()) both result in floor -3.
</blockquote>
To what floor will the instruction take Link to?

###**Hints:**
- There are two ways to get the input file into your python code:

    ####Method 1: Download and read the file
   
        # Download the input file and save it as 'day01_input.txt' in your project folder
        with open('day01_input.txt', 'r') as file:  #'r' means read-only
            input_data = file.read().strip()  # Read all text and remove extra whitespace

        print(f"Input length: {len(input_data)}")  # Optional: check how many characters you have
   

    ####Method 2: copy and paste the input

        # Copy the input from the webpage and paste it as a string
        input_data = """((()))(()()()((((()(((())(()(()((((((()(()(((())))((()(((()"""  # Your input here

        # Remove any accidental line breaks
        input_data = input_data.replace('\n', '').replace(' ', '')

