import tkinter

root = tkinter.Tk()


def button1_push():
    import os
    import tkinter.filedialog
    initDir = os.path.abspath(os.path.dirname(__file__))
    filenames = tkinter.filedialog.askopenfilenames(initialdir=initDir)
    for filename in filenames:
        list1.insert(tkinter.END, filename)

label1 = tkinter.Label(root, text="Inputs:")
label1.pack(expand=True, fill=tkinter.BOTH)

button1 = tkinter.Button(root, text="add...", command=button1_push)
button1.pack(expand=True, fill=tkinter.BOTH)

list1_scroll_y = tkinter.Scrollbar(root)
list1 = tkinter.Listbox(root, selectmode="extended", yscrollcommand=list1_scroll_y.set)
list1_scroll_y["command"] = list1.yview
list1_scroll_y.pack(side=tkinter.RIGHT,fill="y")
list1.pack(expand=True, fill=tkinter.BOTH)


frame = tkinter.Frame(root)
button = tkinter.Button(frame, text="select...")
textbox1 = tkinter.Entry(frame)
button.grid(row=1, column=2)
textbox1.grid(row=1, column=1)
frame.pack()

tkinter.Label(root, text="Outputs:").pack(expand=True, fill=tkinter.BOTH)
tkinter.Button(root, text="GO").pack(expand=True, fill=tkinter.BOTH)

root.mainloop()