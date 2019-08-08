import tkinter as tk
import pandas as pd

papers_df = pd.read_csv('../Literature_Updates/2019-5-29-litupdate.csv')

def onselect(event):
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    
    label = tk.Label(lower_frame, font=('Century Gothic', 10), text=value, wraplength=500)
    label.grid(column=1, row=1, pady=5, padx=5, columnspan=3)
    
    listSelection.delete(0, tk.END)
    listSelection.insert(tk.END, 'Title: ' + value)
    listSelection.insert(tk.END, 'Predicted Value: %.1f%%' % float(papers_df.pred_val[index]))
    listSelection.insert(tk.END, 'Abstract: NEED TO ADD')# + papers_df[]
    index = int(w.curselection()[0])
    value = w.get(index)
    print(papers_df.pred_val[index])
    print('You selected item %d: "%s"' % (index, value))

current_id = 0

HEIGHT = 850
WIDTH = 1200

window = tk.Tk() # create window
window.configure(bg='lightgrey')
window.title("Gary and Ryan Lit Update Checker")
window.geometry(str(WIDTH)+ 'x' + str(HEIGHT))

lbl1 = tk.Label(window, text="Paper List:", fg='black', font=("Helvetica", 16, "bold"))
lbl2 = tk.Label(window, text="Paper Information:", fg='black', font=("Helvetica", 16,"bold"))
lbl1.grid(row=0, column=0, sticky=tk.W)
lbl2.grid(row=0, column=1, sticky=tk.W)

frm = tk.Frame(window)
frm.grid(row=1, column=0, sticky=tk.N+tk.S)
window.rowconfigure(1, weight=1)
window.columnconfigure(1, weight=1)

scrollbar = tk.Scrollbar(frm, orient="vertical")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listPapers = tk.Listbox(frm, width=40, yscrollcommand=scrollbar.set, font=("Helvetica", 12))
listPapers.bind('<<ListboxSelect>>',onselect)
listPapers.pack(expand=True, fill=tk.Y)

scrollbar.config(command=listPapers.yview)

listSelection = tk.Listbox(window, width=int(.3*WIDTH), height=7, font=("Helvetica", 12))
listSelection.grid(row=1, column=1, sticky=tk.E+tk.W+tk.N)

lower_frame = tk.Frame(window, bg = 'grey', bd = 10)
lower_frame.place(relx = .33+.25, rely = .3, relwidth = .5, relheight = .5, anchor = 'n')

for k, title in enumerate(papers_df.full_title):
    listPapers.insert(tk.END, str(k+1) + '. ' + title)

tk.mainloop()