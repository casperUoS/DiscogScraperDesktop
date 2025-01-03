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
    items = ["Shelfmark CD", "Shelfmark LP", "Barcode{023}", "Company {031}", "Label {032}", "Label Match {035}",
             "Title", "Contributor 1", "Genre 1", "Genre 2", "Genre 3", "Genre 4", "Format {310}",
             "Recording address {502}", "Contents note [505]", "Contents note [505]", "Contents note [505]",
             "044 Country of manufacture [code]", "Date {260}", "092 (copy condition code)", "490 Collection",
             "351 Access", "502 Bootleg note"]
    Lb2.delete(0, END)
    for item in items:
        Lb2.insert(END, item)

def enterPressed(event):
    clickedAdd()

def backSpacePressed(event):
    clickedDelete()
    clickedDeleteColumn()



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
            if "Shelfmark CD" in columns:
                row.append("")  # shelfmarkCD
            if "Shelfmark LP" in columns:
                row.append("")  # shelfMarkLP
            if "Barcode{023}" in columns:
                row.append("")  # barcode
            if "Company {031}" in columns:
                row.append(discogs_scraper.getCompony(release))  # compony
            if "Label {032}" in columns:
                row.append(discogs_scraper.getLabel(release))  # label
            if "Label Match {035}" in columns:
                row.append(discogs_scraper.getLabelMatch(release))  # labelMatch
            if "Title" in columns:
                row.append("\"" + release.title + "\"")  # title
            if "Contributor 1" in columns:
                row.append("")  # contributer1
            for i in columns:
                if i.startswith("Genre"):
                    row.append("")  # genre
            if "Format {310}" in columns:
                row.append(discogs_scraper.getFormat(release))  # format
            if "Recording address {502}" in columns:
                row.append("")  # recording address
            if "Contents note [505]" in columns:
                row.append("\"" + discogs_scraper.getTracks1(release) + "\"")  # contentsNote1
                row.append("\"" + discogs_scraper.getTracks2(release) + "\"")  # contentsNote 2
                row.append("")  # contentsNote 3
            if "Copy note {956}" in columns:
                row.append("")
            if "044 Country of manufacture [code]" in columns:
                row.append(discogs_scraper.getCountry(release))  # country
            if "Date {260}" in columns:
                row.append(discogs_scraper.getDate(release))  # date
            if "092 (copy condition code)" in columns:
                row.append("B")  # copycondition code
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

optionsFrame = Frame(root)

pathLabel = Label(optionsFrame, text="File Location")
pathButton = Button(optionsFrame, text="Select", command=select_file)
locationLabel = Label(optionsFrame, text="Select a File Location!")
pathLabel.grid(column=0,row=0)
pathButton.grid(column=0,row=1)
locationLabel.grid(column=0,row=2)

#List of columns
Lb2 = Listbox(optionsFrame)
items = ["Shelfmark CD", "Shelfmark LP", "Barcode{023}", "Company {031}", "Label {032}", "Label Match {035}", "Title", "Contributor 1", "Genre 1", "Genre 2", "Genre 3", "Genre 4", "Format {310}", "Recording address {502}", "Contents note [505]", "Contents note [505]", "Contents note [505]", "Copy note {956}" ,"044 Country of manufacture [code]", "Date {260}", "092 (copy condition code)", "490 Collection", "351 Access", "502 Bootleg note"]
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
