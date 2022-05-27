from tkinter import *
import pandas as pd
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
flip_timer = "after#0" #For the first timer get a value
current_word = {}

######################## GET DATA ######################################################

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
finally:
    data_dict = data.to_dict(orient="records")
    
######################## GET WORD ######################################################

def get_card():
    global flip_timer, current_word
    window.after_cancel(flip_timer)
    current_word = choice(data_dict)
    canva.itemconfig(canva_img, image=img_front)
    canva.itemconfig(card_language, fill="black", text="French")
    canva.itemconfig(card_word, fill="black", text=current_word['French'])
    flip_timer = window.after(2000, english_card)

#Flip the card to english after 2s
def english_card():
    canva.itemconfig(canva_img, image=img_back)
    canva.itemconfig(card_language, fill="white", text="English")
    canva.itemconfig(card_word, fill="white", text=current_word['English'])

#When know the card, remove it
def card_known():
    global data_dict
    data_dict.remove(current_word)
    print(len(data_dict))
    get_card()

#When close the window save the cards that not know
def on_closing():
    global data_dict
    data_df = pd.DataFrame(data_dict)
    data_df.to_csv("data/words_to_learn.csv", index=False)
    window.destroy()
    
######################## UI SETUP ######################################################

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canva = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
img_front = PhotoImage(file="images/card_front.png")
img_back = PhotoImage(file="images/card_back.png")
canva_img = canva.create_image(400, 268, image=img_front)
card_language = canva.create_text(400, 150, font=("Arial", 40, "italic"))
card_word = canva.create_text(400, 263, font=("Arial", 60, "bold"))
canva.grid(column=0, row=0, columnspan=2, pady=(0,50))

wrong_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, border=0,
                   activebackground=BACKGROUND_COLOR, command=get_card)
wrong_btn.grid(column=0, row=1)

right_img = PhotoImage(file="images/right.png")
right_btn = Button(image=right_img, highlightthickness=0, border=0,
                   activebackground=BACKGROUND_COLOR, command=card_known)
right_btn.grid(column=1, row=1)

#Get card for the first time
get_card()

#Closing the window
window.protocol("WM_DELETE_WINDOW", on_closing)

window.mainloop()