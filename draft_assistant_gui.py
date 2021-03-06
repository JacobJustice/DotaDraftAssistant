from tkinter import *
import pandas as pd
from PIL import ImageTk, Image, ImageOps
import tkinter.font as tkFont
from pprint import pprint
from ast import literal_eval

BUTTON_PAD_X=4
BUTTON_PAD_Y=2

root = Tk()

root.title("DotA 2 Draft Assistant")
#root.attributes('-fullscreen', True)

largefont = tkFont.Font(family='Helvetica',size=32)

### Frames
#

# team title row
team_titles = Frame(root,bg='white')
team_titles.pack(side=TOP,fill=X)

# teams row
teams = Frame(root,bg='white')
teams.pack(side = TOP,fill=X)
radiant = Frame(teams,bg='limegreen')
radiant.pack(side = LEFT,fill=X,expand=True)
dire = Frame(teams,bg='darkred')
dire.pack(side = RIGHT,fill=X,expand=True)

# search bar
search_bar_frame = Frame(root,bg='lightgrey')
search_bar_frame.pack(side=TOP,fill=X)

# selectable heroes row
heroes_frame = Frame(root,bg='black')
heroes_frame.pack(side=TOP,fill=BOTH,expand=True)

strength = Frame(heroes_frame,bg='indianred')
strength.pack(side=LEFT,fill=BOTH,expand=True)
agility = Frame(heroes_frame,bg='lightgreen')
agility.pack(side=LEFT,fill=BOTH,expand=True)
intelligence = Frame(heroes_frame,bg='lightblue')
intelligence.pack(side=LEFT,fill=BOTH,expand=True)

# menu row
menu = Frame(root,bg='white')
menu.pack(side=BOTTOM,fill=X)

### global state variables
# if referencing a team True is Radiant and False is Dire
team_radiant = None # are you on the radiant?
selecting_hero = False # are you selecting a hero?
drafting_team = None # are you drafting for the radiant?
current_drafted_button = None # pointer to the hero slot you are currently drafting for

###
### Buttons Labels and Input
###
info_label = Label(search_bar_frame,font=largefont,text='Select a team at the top',bg='lightgrey',pady=3)
info_label.pack(side=RIGHT)


def print_out(text):
    info_label.configure(text=text)

## team title select
def radiant_select():
    global team_radiant
    if team_radiant is None:
        print_out(text='You are on The Radiant, now select the draft')
        team_radiant = True
    else:
        print_out(text='You\'ve already selected a team.')

def dire_select():
    global team_radiant
    if team_radiant is None:
        print_out(text='You are on The Dire, now select the draft')
        team_radiant = False
    else:
        print_out(text='You\'ve already selected a team.')

select_radiant = Button(team_titles, text='The Radiant', bg='limegreen', command=radiant_select,width=5,cursor='hand1')
select_radiant.pack(side=LEFT,fill=X,expand=True)
select_dire = Button(team_titles, text='The Dire', bg='indianred', command=dire_select,width=5,cursor='hand1')
select_dire.pack(side=RIGHT,fill=X,expand=True)

## team heroes
radiant_heroes = []
dire_heroes = []

## radiant hero buttons
def radiant_draft(button):
    if team_radiant is None:
        print_out('Select a team')
    else:
        print_out('Drafting for The Radiant, select a hero')
        global selecting_hero
        global drafting_team
        selecting_hero = True #currently selecting a hero
        drafting_team = True #drafting for Radiant
        global current_drafted_button
        current_drafted_button = button

img = Image.open('./data/portraits/dummy.png')
dummy_image = ImageTk.PhotoImage(img)
radiant1 = Button(radiant, image=dummy_image, activebackground="white", bg='green',cursor='hand1',command=lambda:radiant_draft(radiant1))
radiant1.pack(side=LEFT,padx=2)
radiant2 = Button(radiant, image=dummy_image, activebackground="white", bg='green',cursor='hand1',command=lambda:radiant_draft(radiant2))
radiant2.pack(side=LEFT,padx=2)
radiant3 = Button(radiant, image=dummy_image, activebackground="white", bg='green',cursor='hand1',command=lambda:radiant_draft(radiant3))
radiant3.pack(side=LEFT,padx=2)
radiant4 = Button(radiant, image=dummy_image, activebackground="white", bg='green',cursor='hand1',command=lambda:radiant_draft(radiant4))
radiant4.pack(side=LEFT,padx=2)
radiant5 = Button(radiant, image=dummy_image, activebackground="white", bg='green',cursor='hand1',command=lambda:radiant_draft(radiant5))
radiant5.pack(side=LEFT,padx=2)

## dire hero buttons
def dire_draft(button):
    if team_radiant is None:
        print_out('Select a team')
    else:
        print_out('Drafting for The Dire, select a hero')
        global selecting_hero
        global drafting_team
        selecting_hero = True #currently selecting a hero
        drafting_team = False #drafting for Dire
        global current_drafted_button
        current_drafted_button = button
dire1 = Button(dire, image=dummy_image, activebackground="white", bg='red',cursor='hand1',command=lambda:dire_draft(dire1))
dire1.pack(side=RIGHT,padx=2)
dire2 = Button(dire, image=dummy_image, activebackground="white", bg='red',cursor='hand1',command=lambda:dire_draft(dire2))
dire2.pack(side=RIGHT,padx=2)
dire3 = Button(dire, image=dummy_image, activebackground="white", bg='red',cursor='hand1',command=lambda:dire_draft(dire3))
dire3.pack(side=RIGHT,padx=2)
dire4 = Button(dire, image=dummy_image, activebackground="white", bg='red',cursor='hand1',command=lambda:dire_draft(dire4))
dire4.pack(side=RIGHT,padx=2)
dire5 = Button(dire, image=dummy_image, activebackground="white", bg='red',cursor='hand1',command=lambda:dire_draft(dire5))
dire5.pack(side=RIGHT,padx=2)

## search bar
def search_callback(event):
    #small delay to ensure tkinter has handled the keypress
    root.after(1,_search_callback)

def _search_callback():
    for hero in heroes.keys():
        if search_bar.get() not in hero:
            heroes[hero].set_to_bw()
        else:
            heroes[hero].set_to_color()

search_label = Label(search_bar_frame,text='Search for a hero',bg='lightgrey')
search_label.pack(side=LEFT,padx=2,pady=3)

search_bar = Entry(search_bar_frame,font=largefont)
search_bar.bind("<Key>",search_callback)
search_bar.pack(side=LEFT,padx=2)



## draftable heroes
class Hero:
    title = None
    title_raw = None
    image_path = None
    primary_stat = None
    good_against = None
    bad_against = None
    well_with = None

    pil_image = None
    hero_image = None
    active_image = None

    button = None

    draftability = 0

    drafted = False
    bw = False
    def __init__(self, row, column_n, row_n):
        self.title = row['title']
        self.title_raw = row['title_raw']
        self.image_path = row['image_path']
        self.primary_stat = row['primary_stat']
        self.good_against = row['good_against']
        self.bad_against = row['bad_against']
        self.well_with = row['well_with']

        img = Image.open(self.image_path)
        img = img.resize((85,48), Image.ANTIALIAS)
        self.pil_image = img
        self.hero_image = ImageTk.PhotoImage(img)
        self.active_image = ImageTk.PhotoImage(img)
        
        if self.primary_stat.lower() == 'strength':
            self.button = Button(strength,image=self.hero_image,cursor='hand1',command=self.clicked_callback,activebackground='lightyellow')
        elif self.primary_stat.lower() == 'agility':
            self.button = Button(agility,image=self.hero_image,cursor='hand1',command=self.clicked_callback,activebackground='lightyellow')
        elif self.primary_stat.lower() == 'intelligence':
            self.button = Button(intelligence,image=self.active_image,cursor='hand1',command=self.clicked_callback,activebackground='lightyellow')
        self.button.grid(column=column_n,row=row_n,padx=BUTTON_PAD_X, pady=BUTTON_PAD_Y,sticky='NESW')

    def clicked_callback(self):
        global selecting_hero
        if selecting_hero:
            global drafting_team
            global current_drafted_button
            current_drafted_button.configure(image=self.hero_image)
            self.drafted = True
            current_drafted_button = None
            self.update_portrait()

            if drafting_team:
                radiant_heroes.append(self.title)
            else:
                dire_heroes.append(self.title)

            for hero in heroes.keys():
                heroes[hero].compute_draftability()
                
            selecting_hero = False

    def compute_draftability(self):
        self.draftability = 0
        global heroes
        global team_radiant
        good_against_copy = self.good_against
        bad_against_copy = self.bad_against
        well_with_copy = self.well_with
        selecting_hero = False
        for radiant_hero in radiant_heroes:
            # if this hero is good against a hero on the radiant
            self.update_draftability(radiant_hero, self.good_against, not team_radiant, True)
            # if this hero is bad against a hero on the radiant
            self.update_draftability(radiant_hero, self.bad_against, not team_radiant, False)
            # if this hero works well with a hero on the radiant
            self.update_draftability(radiant_hero, self.well_with, team_radiant, True)

            # if a hero is good against this hero on the radiant and you're on the dire subtract 1
            self.update_draftability(self.title, heroes[radiant_hero].good_against, not team_radiant, False)
            self.update_draftability(self.title, heroes[radiant_hero].bad_against, not team_radiant, True)
            self.update_draftability(self.title, heroes[radiant_hero].well_with,  team_radiant, True)

        for dire_hero in dire_heroes:
            # if this hero is good against a hero on the dire and you're on the radiant add 1
            self.update_draftability(dire_hero, self.good_against, team_radiant, True)
            self.update_draftability(dire_hero, self.bad_against, team_radiant, False)
            self.update_draftability(dire_hero, self.well_with, not team_radiant, True)

            # if a hero on the dire is good against this hero and you're on the radiant subtract 1
            self.update_draftability(self.title, heroes[dire_hero].good_against, team_radiant, False)
            self.update_draftability(self.title, heroes[dire_hero].bad_against, team_radiant, True)
            self.update_draftability(self.title, heroes[dire_hero].well_with, not team_radiant, True)


        self.update_portrait()


    def update_draftability(self, hero_in, hero_list, correct_team, add_):
        # if given hero is in given hero_list
        if hero_in in hero_list:
            # true if on the correct team
            if correct_team:
                # true if adding 1 to draftability false for subtract
                if add_:
                    self.draftability += 1
                else:
                    self.draftability -= 1


    def set_to_bw(self):
        self.bw = True
        self.update_portrait()

    def set_to_color(self):
        self.bw = False
        self.update_portrait()

    def update_portrait(self):
        img = self.pil_image
        if not self.drafted:
            if self.draftability >= 0:
                img = ImageOps.expand(img,border=self.draftability*2,fill='limegreen')
                img = img.resize((85,48), Image.ANTIALIAS)
                if self.draftability > 0:
                    print(self.title, self.draftability)
                    self.button.configure(bg='limegreen',text=str(self.draftability))
                else:
                    self.button.configure(bg='grey')
            else:
                img = ImageOps.expand(img,border=self.draftability*-2,fill='red')
                img = img.resize((85,48), Image.ANTIALIAS)
                self.button.configure(bg='red',text=str(self.draftability))

            if self.bw:
                img = ImageOps.grayscale(img)
            self.active_image = ImageTk.PhotoImage(img)
            self.button.configure(image=self.active_image)
        else:
            img = ImageOps.grayscale(img)
            self.active_image = ImageTk.PhotoImage(img)
            self.button.configure(image=self.active_image,bg='yellow')



## hero buttons
df = pd.read_csv('./data/hero_data.csv')
df.good_against = df.good_against.apply(literal_eval)
df.bad_against = df.bad_against.apply(literal_eval)
df.well_with = df.well_with.apply(literal_eval)

#print(df)
heroes = {}

# undoubtedly a better way to pass this info around but /shrug
str_column = 0
agi_column = 0
int_column = 0
str_row = 0
agi_row = 0
int_row = 0

strength.update()
num_columns = strength.winfo_width()//(85+BUTTON_PAD_X*2)
strength.grid_columnconfigure(list(range(num_columns)),weight=1)
agility.grid_columnconfigure(list(range(num_columns)),weight=1)
intelligence.grid_columnconfigure(list(range(num_columns)),weight=1)
print('num_columns',num_columns)
for index, row in df.iterrows():
    if row['primary_stat'].lower() == 'strength':
        heroes.update({row['title']:Hero(row,str_column,str_row)})
        str_column+=1
        if str_column==num_columns:
            str_row+=1
            str_column=0
    elif row['primary_stat'].lower() == 'agility':
        heroes.update({row['title']:Hero(row,agi_column,agi_row)})
        agi_column+=1
        if agi_column==num_columns:
            agi_row+=1
            agi_column=0
    elif row['primary_stat'].lower() == 'intelligence':
        heroes.update({row['title']:Hero(row,int_column,int_row)})
        int_column+=1
        if int_column==num_columns:
            int_row+=1
            int_column=0

print('number of hero buttons is',len(heroes))

exit_button = Button(menu, text="Exit", command=root.destroy,cursor='hand1',font=largefont)
exit_button.pack(side=BOTTOM,fill=X,expand=True)

root.mainloop()

