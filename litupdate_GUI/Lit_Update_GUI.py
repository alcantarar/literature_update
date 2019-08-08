from tkinter import *
import pandas as pd

papers_df = pd.read_csv('../Literature_Updates/2019-8-8-litupdate.csv')
new_papers_df = papers_df
new_papers_df['new_topic'] = ''

all_topics = {'BONE', 'CARDIOVASCULAR/CARDOPULMONARY', 'CELLULAR/SUBCELLULAR', 'COMPARATIVE', 'DENTAL/ORAL/FACIAL',
              'EVOLUTION/ANTHROPOLOGY', 'GAIT/LOCOMOTION', 'JOINT/CARTILAGE', 'METHODS', 'MODELING', 'NEURAL',
              'ORTHOPAEDICS/SPINE', 'ORTHOPAEDICS/SURGERY', 'REHABILITATION', 'SPORT/EXERCISE', 'TENDON/LIGAMENT',
              'TISSUE/BIOMATERIAL', 'VETERINARY/AGRICULTURAL'}

def cat_buttons(frm, index, paper_list):

    b_dict = paper_list['pred_val'][index].split('; ')
    b_dict_new = {}
    for k in b_dict:
        b_dict_new[k] = 0
    b_dict = b_dict_new

    var = StringVar()
    var.trace('u', print(var.get()))

    def updateselect(index):
        if index < len(papers_df)-1:  # make sure we don't go past end of paper list
            listPapers.selection_clear(index)
            listPapers.activate(index + 1)
            listPapers.selection_set(index + 1)
            index = index + 1
        else:
            index = index

        value = listPapers.get(index)
        paper_info.config(text=papers_df['full_title'][index])
        abstract_info.config(text=papers_df['abstract'][index])

        # print(papers_df['full_title'][index])
        cat_buttons(button_frame, index, papers_df)

    def select_topic():
        new_papers_df['new_topic'].iloc[index] = str(var.get()).split()[1]
        updateselect(index)

    def change_dropdown(*args):
        # text = tkvar.get()
        # print(text)
        new_papers_df['new_topic'].iloc[index] = str(tkvar.get())
        print(new_papers_df.head(5))
        updateselect(index)

    c = 0
    for key in b_dict:
        b_dict[key] = Radiobutton(frm, text = key, bd = 4, width = 35, font = ('Helvetica',8),command = select_topic)
        b_dict[key].config(indicatoron=0, variable = var, value = key)
        b_dict[key].grid(row = c, column = 0, sticky = W, pady = 5, padx = 5)
        c = c+1

    top_topics = [key.split(' ')[1] for key in b_dict.keys()]
    choices = []
    tkvar = StringVar(frm)
    for k in all_topics:
        if k not in top_topics:
            choices.append(k)
    choices.sort()
    for ch in choices:
        ch = 0
    other_topics = OptionMenu(frm, tkvar, *choices)
    other_topics.config(font =('Helvetica', 10), width = 35)
    other_topics.grid(row = 0, column = 1, pady = 5, padx = 5)
    tkvar.trace('w', change_dropdown)


def onselect(event):
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    paper_info.config(text = papers_df['full_title'][index])
    abstract_info.config(text = papers_df['abstract'][index])

    # print(papers_df['full_title'][index])
    cat_buttons(button_frame, index, papers_df)

HEIGHT = 850
WIDTH = 1300

window = Tk()
window.title('Lit Update Checker')
window.config()
canvas = Canvas(window, height = HEIGHT, width = WIDTH)
canvas.pack()

paper_list = LabelFrame(window, bg = 'white', bd = 5, text = 'Paper Titles', font = ('Helvetica', 20,'bold'), relief = 'flat')
paper_list.place(relx = 0.21, rely = .05, relwidth = 0.4, relheight = 0.91, anchor = 'n')

scrollbar = Scrollbar(paper_list, orient="vertical")
scrollbar.pack(side=RIGHT, fill=Y)
#
listPapers = Listbox(paper_list, width=90, yscrollcommand=scrollbar.set, font=("Helvetica", 12))
listPapers.bind('<<ListboxSelect>>',onselect)
listPapers.pack(expand=True, fill=Y)
#
scrollbar.config(command=listPapers.yview)

for x, title in enumerate(papers_df.full_title):
    listPapers.insert(END, str(x+1) + '. ' + str(title))

# paper and abstract details
paper_details = LabelFrame(window, bg = 'white', bd = 5, text = 'Paper Details', font = ('Helvetica', 20,'bold'), relief = 'flat')
paper_details.place(relx = 0.7, rely = 0.05, relwidth = 0.55, relheight = 0.5, anchor = 'n')
paper_info = Label(paper_details, text = 'select a paper', font = ('Helvetica', 12,'bold'), bg = 'white', wraplength = 700, justify = 'left')
paper_info.pack()

abstract_info = Label(paper_details, text = '', font = ('Helvetica', 12), bg = 'white', wraplength = 700, justify = 'left', anchor = 'nw')
abstract_info.pack()

#button panel
button_frame = Frame(window, bg = 'white', bd = 5, relief = 'flat')
button_frame.place(relx = 0.7, rely = 0.58, relwidth = 0.55, relheight = 0.38, anchor = 'n')

cat_buttons

mainloop()