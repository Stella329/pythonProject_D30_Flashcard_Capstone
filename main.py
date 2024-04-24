BACKGROUND_COLOR = "#B1DDC6"
TITLE =('Arial', 40, 'italic')
FONT = ('Arial', 60, 'bold')

#GLOBAL
current_word_pair = None
lang_title = None
lang_word = None



from tkinter import *
import pandas
import random

#-------------- DATA -------------#
try:
    to_learn_df = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    french_words_df = pandas.read_csv('data/french_words.csv')  ##--type=dataframe
    words_list = french_words_df.to_dict(orient='records')
else:
    words_list = to_learn_df.to_dict(orient='records')
# DataFrame.to_dict(orient="records")
## To get all the rows out as a LIST of dictionaries e.g. [{french_word: english_word}, {french_word2: english_word2}, {french_word3: english_word3}]
# try: + with open: 会乱码



# --------BUTTON ACTION------------#
def change_word():
    # new word
    global current_word_pair
    current_word_pair = random.choice(words_list)

    #flip
    global flip_timer
    window.after_cancel(flip_timer) ##每次重启timer
    change_tofront()
    # LOOP #
    flip_timer = window.after(3000, change_toback)


def tick(): ## 出现过的词移除，不会再出现
    global current_word_pair
    words_list.remove(current_word_pair)
    words_df = pandas.DataFrame(words_list)
    words_df.to_csv ('data/words_to_learn.csv', index=False)
    change_word()
    ##1.save updated data into a new .csv so to read it next time --为了不对原french_words.csv做修改
    ##2.data.to_csv("filename.csv", index=False): If you don't want to create an index for the new csv, set the index parameter to False
    ##encoding = 'utf-8-sig'  --解决pandas.to_csv() 中文乱码问题



# ACTION -------------#
def FRword():
    global current_word_pair
    FRword = current_word_pair['French']
    return FRword

def ENword():
    global current_word_pair
    ENword = current_word_pair['English']
    return ENword


def change_toback():
    global lang_title
    global lang_word
    canvas.itemconfig(card_image, image=cardback_img)
    canvas.itemconfig(lang_title, text = 'English', fill='white')
    canvas.itemconfig(lang_word, text=ENword(), fill='white')
    # METHOD 2: 清空，重新填充
    # canvas.itemconfig(lang_title, text='')  ##清空
    # canvas.itemconfig(lang_word, text='')
    # lang_title = canvas.create_text(400, 150, fill='white', text='English', font=TITLE)
    # lang_word = canvas.create_text(400, 283, fill='white', text=ENword(), font=FONT)

def change_tofront():
    global lang_title
    global lang_word
    canvas.itemconfig(card_image, image=cardfront_img)
    canvas.itemconfig(lang_title, text = 'French', fill='black')
    canvas.itemconfig(lang_word, text=FRword(), fill='black')




#-------------- UI SETUP -------------#
# WINDOW
window = Tk()
window.title('Flashy: My Flash Card')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, change_toback)  ## Global; 不能建在最开头--NameError: name 'window' is not defined


# CANVAS
canvas = Canvas(width=800, height=526)
canvas.config(highlightthickness=0, bg=BACKGROUND_COLOR) # 加入highlightthickness=0 & bg去白边

cardfront_img = PhotoImage(file='images/card_front.png')
cardback_img = PhotoImage(file='images/card_back.png')
card_image = canvas.create_image(400, 263, image=cardfront_img)
lang_title = canvas.create_text(400, 150, fill ='black', text='', font=TITLE)
lang_word = canvas.create_text(400, 283, fill = 'black', text='', font=FONT)
# print(to_learn_df) ##乱码测试
print(words_list)
change_word() ##首次触发：第一个单词不点button



canvas.grid(column=0, row=0, columnspan=2)


# BUTTONS AND STUFF
tick_img = PhotoImage(file='images/right.png')
cross_img = PhotoImage(file='images/wrong.png')

tick_button = Button(image=tick_img,command=tick) #去白边move_1
tick_button.config(highlightthickness=0, borderwidth=0) #去白边move_2
tick_button.grid(column=0, row=1, pady=20)

cross_button = Button(image=cross_img, command=change_word)
cross_button.config(highlightthickness=0,borderwidth=0)
cross_button.grid(column=1, row=1)




window.mainloop()