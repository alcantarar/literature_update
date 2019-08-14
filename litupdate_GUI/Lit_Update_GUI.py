from tkinter import *
import pandas as pd
import numpy as np
import grip as gr
import webbrowser
import os
litupdate_fname = '../Literature_Updates/2019-8-13-litupdate.csv'
new_litupdate_fname = litupdate_fname[0:-4] + '-ADJUSTED.csv'
new_litupdate_mdname = litupdate_fname[0:-4] + '-ADJUSTED.md'
papers_df = pd.read_csv(litupdate_fname)
new_papers_df = papers_df
# new_papers_df['new_topic'] = ''

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

    def get_var(*args): # <- idk why this works.
        return var.get()
    var = StringVar()
    var.trace('w', get_var)

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
        # print(var.get())
        # print(index)
        new_papers_df['topic'].iloc[index] = str(var.get()).split()[1]
        print(new_papers_df.head(10)) # for debugging
        updateselect(index)
        new_papers_df.sort_values('topic').to_csv(new_litupdate_fname, index = False)
        print(new_litupdate_fname)
    def change_dropdown(*args):
        # text = tkvar.get()
        # print(text)
        new_papers_df['topic'].iloc[index] = str(tkvar.get())
        print(new_papers_df.head(10)) # for debugging
        new_papers_df.sort_values('topic').to_csv(new_litupdate_fname, index = False)
        updateselect(index)


    c = 0
    for key in b_dict:
        b_dict[key] = Radiobutton(frm, text = key,  bd = 4, width = 40, font = ('Helvetica',10),command = select_topic)
        b_dict[key].config(indicatoron=0, offrelief = FLAT, bg = 'azure3', variable = var, value = key)
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
    other_topics.config(font =('Helvetica', 10),  bg = 'azure3', width = 40, relief = FLAT)
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

def writemarkdown():

    # Markdown header
    urlname = new_litupdate_mdname[0:-3].split('/')[-1]  # Keep just last part of file for website
    print(urlname)
    md_file = open(new_litupdate_mdname, 'w', encoding='utf-8')
    md_file.write('---  \n')
    md_file.write('layout: single  \n')
    md_file.write('title: Biomechanics Literature Update  \n')
    md_file.write('collection: literature  \n')
    md_file.write('permalink: /literature/%s  \n' % urlname)
    md_file.write('excerpt: <br>\n')
    md_file.write('toc: true  \n')
    md_file.write('toc_sticky: true  \n')
    md_file.write('toc_label: Topics  \n')
    md_file.write('---\n')
    # Add Paper Entries
    topic_list = np.unique(papers_df.sort_values('topic')['topic'])
    st = '### Created by: [Ryan Alcantara](https://twitter.com/Ryan_Alcantara_)'
    st = st + ' & [Gary Bruening](https://twitter.com/garebearbru) -'
    st = st + ' University of Colorado Boulder\n\n'
    md_file.write(st)

    papers = pd.read_csv(new_litupdate_fname)
    for topic in topic_list:
        papers_subset = pd.DataFrame(papers[papers.topic == topic].reset_index(drop = True))
        md_file.write('----\n')
        if topic == 'unknown':
            md_file.write('# %s: Num=%i\n' % (topic,len(papers_subset)))
        else:
            md_file.write('# %s\n' % topic)
        md_file.write('----\n')
        md_file.write('\n')
        md_file.write('[Back to top](#created-by-ryan-alcantara--gary-bruening---university-of-colorado-boulder)')
        md_file.write('\n')
        for i,paper in enumerate(papers_subset['links']):
            md_file.write('%s\n' % paper)
            md_file.write('%s\n' % papers_subset['authors'][i])
            md_file.write('%s.  \n' % papers_subset['journal'][i])
            # try: #don't include percentages
            #     md_file.write('(%.1f%%) \n' % papers_subset['pred_val'][i])
            # except:
            #     md_file.write('%s\n' % papers_subset['pred_val'][i])
            md_file.write('\n')

    md_file.close() #saves markdown
    print('Literature Update Exported as Markdown')
    # Preview Markdown offline
    gr.export(path=new_litupdate_mdname) # open markdown and save as html for previewing (offline)
    htmlname = (new_litupdate_mdname[0:-3] + '.html')
    webbrowser.open(os.path.realpath(htmlname), new = 2) #open html in browser
    print('Opening Preview of Markdown')


HEIGHT = 900
WIDTH = 1300

window = Tk()
window.title('Lit Update Checker')
window.config()
canvas = Canvas(window, height = HEIGHT, width = WIDTH)
canvas.pack()

paper_list = LabelFrame(window, bg = 'white', bd = 5, text = 'Paper Titles', fg = 'red4', font = ('Helvetica', 20,'bold'), relief = 'flat')
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
paper_details = LabelFrame(window, bg = 'white', bd = 5, text = 'Paper Details', fg = 'red4', font = ('Helvetica', 20,'bold'), relief = 'flat')
paper_details.place(relx = 0.7, rely = 0.05, relwidth = 0.55, relheight = 0.5, anchor = 'n')
paper_info = Label(paper_details, text = 'select a paper', font = ('Helvetica', 12,'bold'), bg = 'white', wraplength = 700, justify = 'left')
paper_info.pack()

abstract_info = Label(paper_details, text = '', font = ('Helvetica', 12), bg = 'white', wraplength = 700, justify = 'left', anchor = 'nw')
abstract_info.pack()

#button panel
button_frame = Frame(window, bg = 'white', bd = 5, relief = 'flat')
button_frame.place(relx = 0.7, rely = 0.58, relwidth = 0.55, relheight = 0.38, anchor = 'n')
button_frame.grid_rowconfigure(3, weight =1)
#paper categories
cat_buttons


close_bttn = Button(button_frame, text = 'CLOSE', relief = FLAT, bg = 'azure4', fg = 'black', bd = 4, width = 25, font = ('Helvetica',10,'bold'), command = window.destroy)
close_bttn.grid(row = 5, column = 0, pady = 5, sticky = 'nw')

gen_md_bttn = Button(button_frame, text = 'Generate Markdown', relief = FLAT, bg = 'azure4', fg = 'black', bd = 4, width = 25, font = ('Helvetica',10,'bold'), command = writemarkdown)
gen_md_bttn.grid(row = 4, column = 0, pady = 5, sticky = 'nw')

mainloop()
