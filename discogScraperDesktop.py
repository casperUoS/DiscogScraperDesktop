# Import Module
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import discogs_client
import discogs_scraper

# create root window
root = Tk()

# root window title and dimension
root.title("DiscogScaper")
# Set geometry(widthxheight)
root.geometry('600x500')

# adding menu bar in root window
# new item in menu bar labelled as 'New'
# adding more items in the menu bar
menu = Menu(root)
item = Menu(menu)
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)


items = ["Curator 949x","Type 949t","Shelfmark {087}", "Barcode{023}", "Company {031}", "Label {032}", "Label Match {035}",
             "Date {260}","Copyright {536}", "Manufacture {044}","Title {499}", "Contributor 1 {702}","Contents note {505}", "505-2",
             "Genre 1 {633}", "Country {631}","Culture {632}", "Tag {650}","Format {310}", "Prod note {502}", "Doc {525}",
             "Copy condition {092}", "Copy note {956}", "Acq date {959}", "Donor {548}", "Series {440}", "{312}", "Cat {971}"]



# function to display user text when
# button is clicked
def clickedAdd():
    Lb1.insert(END, txt.get())
    txt.delete(0, END)

def clickedClear():
    Lb1.delete(0,'end')

def clickedDelete():
    selected_checkboxs = Lb1.curselection()

    for selected_checkbox in selected_checkboxs[::-1]:
        Lb1.delete(selected_checkbox)

def clickedDeleteLast():
    Lb1.delete('end')

def clickedDeleteColumn():
    selected_checkboxs = Lb2.curselection()

    for selected_checkbox in selected_checkboxs[::-1]:
        Lb2.delete(selected_checkbox)

def clickedResetColumn():
    constItems = ["Curator 949x","Type 949t","Shelfmark {087}", "Barcode{023}", "Company {031}", "Label {032}", "Label Match {035}",
             "Date {260}","Copyright {536}", "Manufacture {044}","Title {499}", "Contributor 1 {702}","Contents note {505}", "505-2",
             "Genre 1 {633}", "Country {631}","Culture {632}", "Tag {650}","Format {310}", "Prod note {502}", "Doc {525}",
             "Copy condition {092}", "Copy note {956}", "Acq date {959}", "Donor {548}", "Series {440}", "{312}", "Cat {971}"]
    Lb2.delete(0, END)
    for i in constItems:
        Lb2.insert(END, i)

def enterPressed(event):
    clickedAdd()

def backSpacePressed(event):
    clickedDelete()
    clickedDeleteColumn()

def clickedSave():
    key = userTokentxt.get()
    filePath = locationLabel.cget("text")
    urls = Lb1.get(0, 'end')
    allText = key + "\n" + filePath + "\n"
    for url in urls:
        allText += url + "\n"
    f = open(os.path.join(os.getcwd(), "discogSave.txt"), "w")
    f.write(allText)
    f.close()

def clickedLoad():
    f = open(os.path.join(os.getcwd(), "discogSave.txt"), "r")
    file = f.read()
    lines = file.splitlines()
    userTokentxt.delete(0,END)
    userTokentxt.insert(0,lines[0])
    locationLabel.config(text=lines[1])
    for i in range(2,len(lines)):
        Lb1.insert(END,lines[i])

def select_file():
    path = filedialog.askdirectory(title="Select a File")
    locationLabel.config(text=path)




def getDesktopReleases(dis):
    releases = []
    sub1 = "release/"
    sub2 = "-"
    for line in Lb1.get(0, 'end'):
        if len(line.strip()) != 0:
            id = ''.join(line.split(sub1)[1].split(sub2)[0])
            releases.append(dis.release(id))
    return releases

def runFun():
    if locationLabel.cget("text") == "Select a File Location!":
        messagebox.showerror("No File Location Selected", "Please select a file location")
    elif userTokentxt.get() == "":
        messagebox.showerror("No user token", "Please enter a user token")
    else:
        d = discogs_client.Client('my_user_agent/1.0', user_token=userTokentxt.get())
        releases = getDesktopReleases(d)
        columns = Lb2.get(0, 'end')
        f = open(os.path.join(locationLabel.cget("text"), "output.csv"), "w")
        f.write(
            ','.join(columns) + "\n"
        )
        f.close()
        for release in releases:
            csv = ""
            row = []
            if "Curator 949x" in columns:
                row.append("")
            if "Type 949t" in columns:
                row.append("")
            if "Shelfmark {087}" in columns:
                row.append("")  # shelfmarkCD
            if "Barcode{023}" in columns:
                row.append("")  # barcode
            if "Company {031}" in columns:
                row.append(discogs_scraper.getCompony(release))  # compony
            if "Label {032}" in columns:
                row.append(discogs_scraper.getLabel(release))  # label
            if "Label Match {035}" in columns:
                row.append(discogs_scraper.getLabelMatch(release))  # labelMatch
            if "Date {260}" in columns:
                row.append(discogs_scraper.getDate(release))  # date
            if "Copyright {536}" in columns:
                row.append("")
            if "Manufacture {044}" in columns:
                row.append(discogs_scraper.getCountry(release))
            if "Title {499}" in columns:
                row.append("\"" + release.title + "\"")  # title
            if "Contributor 1" in columns:
                row.append("")  # contributer1
            if "Contents note {505}" in columns:
                row.append("\"" + discogs_scraper.getTracks1(release) + "\"")  # Contents note {505}
                row.append("\"" + discogs_scraper.getTracks2(release) + "\"")  # 505-2
            for i in columns:
                if i.startswith("Genre"):
                    row.append("")  # genre
            if "Country {631}" in columns:
                row.append(discogs_scraper.getCountry(release))  # country
            if "Culture {632}" in columns:
                row.append("")
            if "Tag {650}" in columns:
                row.append("")
            if "Format {310}" in columns:
                row.append(discogs_scraper.getFormat(release))  # format
            if "Prod note {502}" in columns:
                row.append("")
            if "Doc {525}" in columns:
                row.append("")
            if "Copy condition {092}" in columns:
                row.append("B")  # copycondition code
            if "Copy note {956}" in columns:
                row.append("")
            if "Acq date {959}" in columns:
                row.append("")  # recording address
            if "Donor {548}" in columns:
                row.append("")  # recording address
            if "Series {440}" in columns:
                row.append("")  # recording address
            if "{312}" in columns:
                row.append("a")  # recording address
            if "Cat {971}" in columns:
                row.append("")  # recording address
            if "Recording address {502}" in columns:
                row.append("")  # recording address
            if "490 Collection" in columns:
                row.append("BPI Anti-Piracy Unit Donation")  # Collection
            if "351 Access" in columns:
                row.append("No copies to be made without permission of the donor")  # Access
            if "502 Bootleg note" in columns:
                row.append(discogs_scraper.getBootlegNote(release))  # Boolteg note
            for item in row:
                csv += str(item) + ","
            csv += "\n"
            f = open(os.path.join(locationLabel.cget("text"), "output.csv"), "a")
            f.write(csv)
            f.close()


root.rowconfigure(1, minsize=500)
root.columnconfigure(1, minsize=500)

urlFrame = Frame(root)

lbl = Label(urlFrame, text="Enter in URL")
lbl.grid(column=0, row=0)

txt = Entry(urlFrame, width=20)
txt.grid(column=1, row=0, sticky="ew")

userTokenlbl = Label(urlFrame, text="Enter in user token")
userTokenlbl.grid(column=0, row=1)

userTokentxt = Entry(urlFrame, width=20)
userTokentxt.grid(column=1, row=1, sticky="ew")

urlFrame.grid(column=0, row=0, sticky="ew")

entryFrame = Frame(root)

Lb1 = Listbox(entryFrame)
Lb1.grid(column=0, row=1, sticky="nsew")

buttonFrame = Frame(entryFrame)
addBtn = Button(buttonFrame, text="Add", command=clickedAdd)
deleteSelectedBtn = Button(buttonFrame, text="Delete", command=clickedDelete)
deleteLastBtn = Button(buttonFrame, text="Delete Last", command=clickedDeleteLast)
clearBtn = Button(buttonFrame, text="Clear", command=clickedClear)
# Set Button Grid


buttonFrame.grid(column=0, row=0, sticky="w")
addBtn.grid(column=0, row=0, sticky="w")
deleteSelectedBtn.grid(column=1, row=0, sticky="w")
deleteLastBtn.grid(column=2, row=0, sticky="w")
clearBtn.grid(column=3, row=0, sticky="w")

entryFrame.grid(column=0, row=1, sticky="nsew")

saveFrame = Frame(entryFrame)
saveBtn = Button(saveFrame, text="Save config", command=clickedSave)
loadBtn = Button(saveFrame, text="Load config", command=clickedLoad)

saveFrame.grid(column=0, row=2, sticky="w")
saveBtn.grid(column=0, row=0, sticky="w")
loadBtn.grid(column=1, row=0, sticky="w")


optionsFrame = Frame(root)

pathLabel = Label(optionsFrame, text="File Location")
pathButton = Button(optionsFrame, text="Select", command=select_file)
locationLabel = Label(optionsFrame, text="Select a File Location!")
pathLabel.grid(column=0,row=0)
pathButton.grid(column=0,row=1)
locationLabel.grid(column=0,row=2)

#List of columns
Lb2 = Listbox(optionsFrame)
for item in items:
    Lb2.insert(END,item)

deleteColumnButton = Button(optionsFrame, text="Delete Column", command=clickedDeleteColumn)
resetColumnsButton = Button(optionsFrame, text="Reset Columns", command=clickedResetColumn)
columnLabel = Label(optionsFrame, text="Columns")
columnLabel.grid(column=0,row=3)
Lb2.grid(column=0, row=4, sticky="ew")
deleteColumnButton.grid(column=0, row=5)
resetColumnsButton.grid(column=0, row=6)

runButton = Button(optionsFrame, text="Run", command=runFun)
runButton.grid(column=0, row=7)

optionsFrame.grid(column=1, row=1, sticky="ns")


root.bind("<Return>", enterPressed)
root.bind("<BackSpace>", backSpacePressed)

# Execute Tkinter
root.mainloop()
