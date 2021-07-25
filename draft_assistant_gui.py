from tkinter import *
from PIL import ImageTk, Image

root = Tk()

root.title("DotA 2 Draft Assistant")

## make frames

#top row
teams = Frame(root)
teams.pack( side = TOP )
radiant = Frame(teams)
radiant.pack( side = LEFT )
dire = Frame(teams)
dire.pack( side = RIGHT)

#heroes row
heroes = Frame(root)
heroes.pack(side=TOP)

strength = Frame(heroes)
strength.grid(column=0,row=0)
agility = Frame(heroes)
agility.grid(column=1,row=0)
intelligence = Frame(heroes)
intelligence.grid(column=2,row=0)

#heroes
menu = Frame(root)
menu.pack(side=BOTTOM)

lbl = Label(radiant, text="Test")
lbl.pack(side=LEFT)

txt = Entry(dire,width=10)
txt.pack(side=LEFT)

def clicked():
    res = "Welcome to " + txt.get()
    lbl.configure(text= res)

btn = Button(menu, text="Click Me", command=clicked)
btn.pack(side=LEFT)

exit_button = Button(menu, text="Exit", command=root.destroy)
exit_button.pack(side=LEFT)

root.mainloop()
