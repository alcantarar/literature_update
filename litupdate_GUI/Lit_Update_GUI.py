from tkinter import *
import pandas as pd

papers_df = pd.read_csv('../Literature_Updates/2019-5-29-litupdate_TEST.csv')



def cat_buttons(frm, index, paper_list):

    b_dict = paper_list['pred_val'][index].split('; ')
    b_dict_new = {}
    for k in b_dict:
        b_dict_new[k] = 0
    b_dict = b_dict_new

    var = StringVar()
    var.trace('u', print(var.get()))

    def select_topic():
        print(var.get())


    c = 2
    for key in b_dict:
        # print(key)
        b_dict[key] = Radiobutton(frm, text = key, bd = 4, width = 30, font = ('Helvetica',10),command = select_topic)
        b_dict[key].config(indicatoron=0, variable = var, value = key)
        b_dict[key].grid(row = c-2, column = 0, sticky = W)
        c = c+1


    # print(b_dict)
def onselect(event):
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    paper_info.config(text = papers_df['full_title'][index])
    abstract_info.config(text = papers_df['abstract'][index])

    # print(papers_df['full_title'][index])
    cat_buttons(button_frame, index, papers_df)

current_id = 0

HEIGHT = 800
WIDTH = 1300

window = Tk()
window.title('Lit Update Checker')
window.config()
canvas = Canvas(window, height = HEIGHT, width = WIDTH)
canvas.pack()

paper_list = LabelFrame(window, bg = 'white', bd = 5, text = 'Paper Titles', font = ('Helvetica', 20,'bold'), relief = 'flat')
paper_list.place(relx = 0.21, rely = .05, relwidth = 0.4, relheight = 0.91, anchor = 'n')

# window.rowconfigure(1, weight=1)
# window.columnconfigure(1, weight=1)
#
scrollbar = Scrollbar(paper_list, orient="vertical")
scrollbar.pack(side=RIGHT, fill=Y)
#
listPapers = Listbox(paper_list, width=90, yscrollcommand=scrollbar.set, font=("Helvetica", 12))
listPapers.bind('<<ListboxSelect>>',onselect)
listPapers.pack(expand=True, fill=Y)
#
scrollbar.config(command=listPapers.yview)

for x, title in enumerate(papers_df.full_title):
    listPapers.insert(END, str(x) + '. ' + str(title))

# paper and abstract details
paper_details = LabelFrame(window, bg = 'white', bd = 5, text = 'Paper Details', font = ('Helvetica', 20,'bold'), relief = 'flat')
paper_details.place(relx = 0.7, rely = 0.05, relwidth = 0.55, relheight = 0.5, anchor = 'n')
paper_info = Label(paper_details, text = 'select a paper', font = ('Helvetica', 12,'bold'), bg = 'white', wraplength = 700, justify = 'left')
paper_info.pack()

abstract_info = Label(paper_details, text = '', font = ('Helvetica', 12), bg = 'white', wraplength = 700, justify = 'left')
abstract_info.pack()

#button panel
button_frame = Frame(window, bg = 'white', bd = 5, relief = 'flat')
button_frame.place(relx = 0.7, rely = 0.58, relwidth = 0.55, relheight = 0.38, anchor = 'n')
#buttons
topics = {'BONE':0, 'CARDIO':0, 'MODELING':0, 'SPORT/EXERC':0, 'METHODS':0, 'GAIT':0, 'NEURAL':0, 'SPINE':0, 'COMPARATIVE':0, 'EVOLUTION':0}

cat_buttons

mainloop()