# Day 1 — A Strange Call

Detective Yolo has just joined the department when a mysterious 911 call comes in — somewhere inside a massive skyscraper.

Unfortunately, the only clue left for him is a string of parentheses. That’s it. No floor number, no room. Just a jumble of ( and ).

He knows the ground floor is floor 0, and an opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), means he should go down one floor. The skyscraper is very tall, obviously, but what's even more maddening, is that its basement is very deep. 

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
        with open('day01_input.txt', 'r') as file:
            input_data = file.read().strip()  # Read all text and remove extra whitespace

        print(f"Input length: {len(input_data)}")  # Optional: check how many characters you have
   

    ####Method 2: copy and paste the input

        # Copy the input from the webpage and paste it as a string
        input_data = """((()))(()()()((((()(((())(()(()((((((()(()(((())))((()(((()"""  # Your input here

        # Remove any accidental line breaks
        input_data = input_data.replace('\n', '').replace(' ', '')

    ####Method 3: Fetch directly from URL (advanced)

        import requests

        # Fetch input directly from your local server
        response = requests.get('http://127.0.0.1:4000/input/day01') #or whatever the url for the input is
        input_data = response.text.strip()

        print(f"Input length: {len(input_data)}") # Optional: check how many characters you have
