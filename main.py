from random import choice
from tkinter import *

import pandas as pd
from PIL import Image, ImageTk  # To resize flags

BACKGROUND_COLOR = "#B1DDC6"

#  Working with tkinter windows as classes instead would avoid all the None value assignment but just practising
front_img, back_img, wrong_img, right_img, back_button_img = None, None, None, None, None
master, window, canvas, timer, img, word1, word2, idx = None, None, None, None, None, None, None, 0
words_to_learn = []
new_pair = {}
language, word, english_word = None, None, None
words_learned = []


# -----------------------------------SELECT LANGUAGE & READ DATA----------------------------------#

def select_language(args):
    global language

    language = args


def read_data():
    global words_to_learn
    #  Reads from words that haven't been learned if it exists else read from the main file
    try:
        data = pd.read_csv(f"data/words_to_learn({language}-english).csv")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        original_data = pd.read_csv(f"data/{language}-english.csv")
        print(original_data)
        words_to_learn = original_data.to_dict(orient="records")
    else:
        words_to_learn = data.to_dict(orient="records")


# -----------------------------------WHEN USER EXIT----------------------------------#
def on_closing():
    """Saves unlearned words to new file to track user progress and reads from it on next run"""
    global words_learned, words_to_learn
    if language is not None:  # if user exit window without starting the app
        words_learned = pd.DataFrame(words_learned)
        words_learned.to_csv(f"data/{language}-words-learned.csv", mode="a", index=False)
        words_to_learn = pd.DataFrame(words_to_learn)
        words_to_learn.to_csv(f"data/words_to_learn({language}-english).csv", index=False)

    try:
        window.destroy()
    except (TclError, AttributeError):
        master.destroy()


# -----------------------------------TRACK PROGRESS / GENERATE NEW PAIR----------------------------------#
def track_progress():
    """To keep tracked of learned and unlearned words"""
    words_learned.append(new_pair)
    words_to_learn.remove(new_pair)


def generate_pair():
    """generates a new pair of words, the word & its english translation"""
    global word, english_word, new_pair
    new_pair = choice(words_to_learn)
    word, english_word = (value for key, value in new_pair.items())  # Unpacks the values to the variables


# -----------------------------------CARD FLIPPING----------------------------------#
def english_card():
    canvas.itemconfig(img, image=back_img)
    canvas.itemconfig(word1, text="English", fill="white")
    canvas.itemconfig(word2, text=english_word, fill="white")


def word_card():
    generate_pair()
    global idx, timer
    window.after_cancel(timer)  # prevents the automatic flipping if user press the right or wrong button abruptly
    canvas.itemconfig(img, image=front_img)
    canvas.itemconfig(word1, text=language, fill="black")
    canvas.itemconfig(word2, text=word, fill="black")
    timer = window.after(3000, english_card)  # flips for english card after 3 seconds


# -----------------------------------ANOTHER WINDOW CALL----------------------------------#

def call_master_window():
    window.after_cancel(timer)  # Cancel timer before destroying window to avoid the timed function from executing
    window.destroy()
    master_window()


def another_window():
    global window, timer, canvas, img, word1, word2
    global front_img, back_img, wrong_img, right_img, back_button_img

    master.destroy()  # Destroys the old window
    window = Tk()
    window.title("Superlang")
    window.config(bg=BACKGROUND_COLOR, padx=50, pady=50, highlightthickness=0)
    window.protocol("WM_DELETE_WINDOW", on_closing)  # To perform an action when user exits program

    front_img = PhotoImage(file="images/card_front.png")
    back_img = PhotoImage(file="images/card_back.png")
    wrong_img = PhotoImage(file="images/wrong.png")
    right_img = PhotoImage(file="images/right.png")
    back_button_img = (Image.open("images/back-button.png"))
    back_button_img = back_button_img.resize((80, 70), Image.Resampling.LANCZOS)
    back_button_img = ImageTk.PhotoImage(back_button_img)

    canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
    img = canvas.create_image(400, 263, image=front_img)
    word1 = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"), fill="black")
    word2 = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"), fill="black")
    canvas.grid(row=0, column=0, columnspan=2)

    # Using lambda to pass multiple commands to the right button
    right_button = Button(image=right_img, highlightthickness=0, bd=0, command=lambda: [track_progress(), word_card()])
    right_button.grid(row=1, column=1)

    wrong_button = Button(image=wrong_img, highlightthickness=0, bd=0, command=word_card)
    wrong_button.grid(row=1, column=0)

    back_button = Button(image=back_button_img, highlightthickness=0, bd=0, command=call_master_window)
    back_button.grid(row=2, column=0, columnspan=2)

    timer = window.after(0, func=word_card)  # To start the flipping


# -----------------------------------MASTER WINDOW----------------------------------#
def master_window():
    global master

    master = Tk()
    master.title("Superlang")
    master.config(bg=BACKGROUND_COLOR, padx=100, pady=100, highlightthickness=0)
    master.protocol("WM_DELETE_WINDOW", on_closing)

    click_label = Label(text=" CLICK FLAG\n", font=("Ariel", 40, "bold"), bg=BACKGROUND_COLOR, highlightthickness=0)
    click_label.grid(row=0, column=1, columnspan=4, rowspan=2)

    german_flag = (Image.open("images/germany_flag.png"))
    german_flag = german_flag.resize((100, 70), Image.Resampling.LANCZOS)
    german_flag = ImageTk.PhotoImage(german_flag)
    german_button = Button(image=german_flag,
                           command=lambda: [select_language("german"), read_data(), another_window()])
    german_button.grid(row=2, column=0, columnspan=2)

    german_label = Label(text="German - English", font=("Ariel", 15, "italic"), bg=BACKGROUND_COLOR)
    german_label.grid(row=3, column=0, columnspan=2)

    spanish_flag = (Image.open("images/spain_flag.png"))
    spanish_flag = spanish_flag.resize((100, 70), Image.Resampling.LANCZOS)
    spanish_flag = ImageTk.PhotoImage(spanish_flag)
    spanish_button = Button(image=spanish_flag,
                            command=lambda: [select_language("spanish"), read_data(), another_window()])
    spanish_button.grid(row=2, column=2, columnspan=2)

    spanish_label = Label(text="Spanish - English", font=("Ariel", 15, "italic"), bg=BACKGROUND_COLOR)
    spanish_label.grid(row=3, column=2, columnspan=2)

    french_flag = (Image.open("images/france_flag.png"))
    french_flag = french_flag.resize((100, 70), Image.Resampling.LANCZOS)
    french_flag = ImageTk.PhotoImage(french_flag)
    french_button = Button(image=french_flag,
                           command=lambda: [select_language("french"), read_data(), another_window()])
    french_button.grid(row=2, column=4, columnspan=2)

    french_label = Label(text="French - English", font=("Ariel", 15, "italic"), bg=BACKGROUND_COLOR)
    french_label.grid(row=3, column=4, columnspan=2)

    master.mainloop()


master_window()
