# create list to store entered words
user_text = []

# set current word being typed
current_word = ""

# set textbox position and size
box_x, box_y, box_w, box_h = 150, 720, 700, 50
active = False  # making the textbox inactive when window is opened  

def setup():
    size(1000, 1000) #setting window size

# setting colour cycle for every 5 words
word_colors = [
    color(173, 151, 227),    # purple
    color(226, 151, 227),    # dark pink
    color(93, 149, 237),    # blue
    color(255, 240, 234),  # light pink
    color(255, 251, 180)   # yellow
]

font = [] # defining font variable
bg_image = None # setting background variable


def setup():
    global fonts, bg_image # setting variables for font and background
    size(1000, 1000) 
    
    # creating fonts for words to cycle through
    fonts = [
             loadFont ("AmericanTypewriter-20.vlw"),
             loadFont ("SnellRoundhand-20.vlw"),
             loadFont ("TimesNewRomanPSMT-20.vlw"),
             loadFont ("Baskerville-Italic-20.vlw")
]

    bg_image = loadImage("bg_image.jpg") # uploading background image

def draw():
    image(bg_image, 0, 0, width, height) # setting background as uploaded image
    
    # text properties for title
    textSize(36)
    textFont(fonts[1], 35) # make font always snellroundhand
    fill(255, 252, 162)
    textAlign(CENTER, TOP)
    text("Daily Gratitude Wall", width / 2, 25)
    
    # text properties for textbox prompt
    textSize(24)
    textFont(fonts[2], 20) # make font always times new roman
    fill(245, 84, 216)
    textAlign(RIGHT, BOTTOM)
    text("I am grateful for...", width / 3.2, 710)

    if active: #when the textbox has been selected (ready for user entries), textbox outline will turn pink
        stroke(245, 84, 216) #textbox outline colour when selcted
    else:
        stroke(0)
    strokeWeight(2)
    fill(255) # texbox outline colour for when not selected
    rect(box_x, box_y, box_w, box_h, 5)
    
    # show current word being typed
    fill(0)
    noStroke()
    textAlign(LEFT, CENTER)
    textFont(fonts[0])  # make textbox font always american typewritter
    textSize(15)
    text(current_word, box_x + 10, box_y + (box_h + textAscent() - textDescent()) / 2.5)
    
    for i in range(len(user_text)):
        word, pos = user_text[i]
        
        word_color = word_colors[i % len(word_colors)]  # cycle through colors
        font = fonts[i % len(fonts)] # cycle through fonts
        
        fill(word_color)
        textFont(font)
        text(word, pos[0], pos[1])

def mousePressed(): # activate textbox if clicked
    global active

    if box_x <= mouseX <= box_x + box_w and box_y <= mouseY <= box_y + box_h:
        active = True
    else:
        active = False

def keyPressed(): # enter letter of keys that are pressed and store them into user_text
    global current_word, user_text
    if active:
        if key == BACKSPACE:
            current_word = current_word[:-1] # setting backspace function
        elif key == ENTER or key == RETURN:
            if current_word.strip() != "": # setting enter function
               
                x, y = find_free_position(current_word)  # finds a free, non-overlapping position
                user_text.append((current_word, (x, y)))
                current_word = ""  # reset current word
        else:
            current_word += key
            

def find_free_position(word): # finding a random x, y that is above the textbox and doesn't overlap
    
    max_attempts = 100 # max 100 attempts to find a non-overlapping position to avoid loop
    for _ in range(max_attempts):
        x = random(50, width - 100)
        y = random(100, box_y - 40)  # finds random x, y coordinated only above the textbox and below the title

        if not check_overlap(word, x, y): # check if any overlap is found 
            return x, y # if no overlap is found then use this position 

    return random(100, width - 100), random(50, box_y - 20) # if no free position is found after max attempts find any random position

def check_overlap(word, x, y):
    # check if (word at x,y) overlaps existing words
    word_w = textWidth(word)
    word_h = textAscent() + textDescent() # estimates the width and height of the word 

    for existing_word, (ex, ey) in user_text: # loop through all previously entered words and their stored coordinates
        ex_w = textWidth(existing_word) # get dimensions of the existing word
        ex_h = textAscent() + textDescent()

   # check if the bounding boxes of the two words intersect 
        if (x < ex + ex_w and      # new word starts before existing word ends 
            x + word_w > ex and    # new word ends after existing word starts
            y - word_h < ey and    # new word’s top is above the bottom of existing word
            y > ey - ex_h):        # new word’s bottom is below the top of existing word
            return True  # overlap detected

    # if no overlap detected with any existing words:
    return False
