import tkinter as tk
from PIL import ImageTk, Image
HEIGHT = 850
WIDTH = 1200
paper_title = 'Regular changes in foot strike pattern during prolonged downhill running do not influence neuromuscular, energetics, or biomechanical parameters.'


def sel(var):
    try:
        print(str(var['text'].split()[0])) #in case any percentages make it through
    except:
        print(str(var)) #from dropdown


def list_paper(loc, row_num, title, top_topics, all_topics):
    label = tk.Label(loc, font=('Century Gothic', 10), text=title, wraplength=500)
    label.grid(column=0, row=row_num, pady=5, padx=5, columnspan=3)

    def print_var(*args):
        print(var.get())
        print(title)
    var = tk.StringVar()
    var.trace('w', print_var)

    b_dict = top_topics
    c = 3
    for key in b_dict:
        b_dict[key] = tk.Radiobutton(loc, text = key, bd = 4, width = 12, font = ('Century Gothic',10))
        b_dict[key].config(indicatoron=0, variable = var, value = key)
        b_dict[key].grid(column = c, row = row_num)
        c = c+1

    def change_dropdown(*args):
        text = tkvar.get()
        sel(text)
        print(title)

    # define dropdown options
    choices = []
    tkvar = tk.StringVar(loc)
    for k in all_topics:
        if k not in top_topics:
            choices.append(k)

    b4 = tk.OptionMenu(loc, tkvar, *choices)
    b4.config(font = ('Century Gothic',10))
    b4.grid(column=c+1, row=row_num, pady=5, padx=5, sticky = tk.W+tk.E)
    tkvar.trace('w', change_dropdown)


#build GUI
root = tk.Tk()

canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

background_image = ImageTk.PhotoImage(Image.open('gang.gif'))
background_label = tk.Label(root, image = background_image)
background_label.place(relwidth = 1, relheight = 1)

lower_frame = tk.Frame(root, bg = 'grey', bd = 10)
lower_frame.place(relx = 0.5, rely = .1, relwidth = 0.85, relheight = 0.8, anchor = 'n')

#top 3 values, remove percentages and replace with 0 for radiobuttons
top = {'BONE':0, 'CARDIO':0, 'MODELING':0}
top2 = {'MODELING':0, 'SPORT/EXERC':0, 'METHODS':0}

#need to insert values into topic_list keys like so:

topics = {'BONE':0, 'CARDIO':0, 'MODELING':0, 'SPORT/EXERC':0, 'METHODS':0, 'GAIT':0, 'NEURAL':0, 'SPINE':0, 'COMPARATIVE':0, 'EVOLUTION':0}

#list the papers. can be done in loop through pandas df
list_paper(lower_frame,0, paper_title, top, topics)

list_paper(lower_frame, 1, paper_title, top2, topics)

list_paper(lower_frame,2, paper_title, top, topics)

list_paper(lower_frame, 3, paper_title, top2, topics)

list_paper(lower_frame,4, paper_title, top, topics)

list_paper(lower_frame, 5, paper_title, top2, topics)

root.mainloop()
