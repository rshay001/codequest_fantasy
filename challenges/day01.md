# Day 1 — A Strange Call

Detective Yolo has just joined the department when a mysterious 911 call comes in — somewhere inside a massive skyscraper.

He only received the address from his unit, no floor number and no apartment number. He asked the lobby security if he noticed anything suspicious. To his surprise, the security guard said, "Detective Yolo is it? I got an envelope for you an hour ago from a visitor." Then handed Yolo the envelope.

Inside the envelope, there are two cards. One is labeled "floor" and the other is labeled "unit". He flipped over the "floor" card, and it is a string of parentheses. That’s it. No floor number, no room. Just a jumble of ( and ). There is a line of fine points explaining that the ground floor is floor 0, and an opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), means he should go down one floor. 

For example:

(()) and ()() both result in floor 0.
((( and (()(()( both result in floor 3.
))((((( also results in floor 3.
()) and ))( both result in floor -1 (the first basement level).
))) and )())()) both result in floor -3.

To what floor will the instruction take Detective Yolo?

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

