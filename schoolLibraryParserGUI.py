from tkinter import Tk, font, Label, Entry, Button, messagebox, filedialog, END
import os
from lib.libraryParser import libraryParser

APP_NAME = "School Library Parser"
VERSION = "v1.0.0"


def enableWidgets(enable):
    val = "disabled"
    if enable:
        val = "normal"
    libraryFileTxt.config(state=val)
    libraryFileBtn.config(state=val)
    savePathTxt.config(state=val)
    savePathBtn.config(state=val)
    saveFileTxt.config(state=val)
    schoolTxt.config(state=val)
    parseBtn.config(state=val)


def clearWidgets():
    libraryFileTxt.delete(0, END)
    savePathTxt.delete(0, END)
    saveFileTxt.delete(0, END)
    schoolTxt.delete(0, END)


def handleOpenFileBtnClick():
    filedata = filedialog.askopenfile()
    if filedata is not None:
        libraryFileTxt.delete(0, END)
        libraryFileTxt.insert(0, filedata.name)


def handleOpenSaveDirBtnClick():
    dirdata = filedialog.askdirectory()
    if dirdata is not None:
        savePathTxt.delete(0, END)
        savePathTxt.insert(0, dirdata)


def handleSaveFileInput(event):
    currValue = saveFileTxt.get()
    if len(currValue) > 0 and not currValue.endswith('.csv'):
        saveFileTxt.insert(len(currValue), '.csv')


def handleRunBtnClick():
    parseFile = libraryFileTxt.get()
    saveDir = savePathTxt.get()
    saveFilename = saveFileTxt.get()
    schoolName = schoolTxt.get()

    if os.path.exists(parseFile):
        if os.path.exists(saveDir):
            if len(saveFilename) > 0:
                if len(schoolName) > 0 and saveFilename.endswith(".csv"):
                    enableWidgets(False)
                    parser = libraryParser(schoolName, parseFile, os.path.join(saveDir, saveFilename))
                    result = parser.parse(debug=False)
                    if result:
                        messagebox.showinfo("Parse Successful", "The parse was successful!\n{0} books parsed...\nSaved results to {1}".format(
                            parser.bookCount,
                            parser.savepath
                        ))
                        enableWidgets(True)
                        clearWidgets()
                    else:
                        messagebox.showerror("Parse Failed", "The parse has failed...\nPlease check all inputs and try again")
                        enableWidgets(True)
                else:
                    messagebox.showinfo("No School Name", "Please enter a school name...")
            else:
                messagebox.showinfo("Invalid Save Filename", "The filename you have entered is not valid")
        else:
            messagebox.showinfo("Invalid Save Directory", "The save directory you have entered is not valid...")
    else:
        messagebox.showinfo("Invalid Filepath", "The filepath you entered is not valid...")


# WINDOW SETUP
window = Tk()
window.title("{0} - {1}".format(APP_NAME, VERSION))
window.resizable(width=False, height=False)
window.geometry("610x245")
window.eval("tk::PlaceWindow . center")
# FONT SETUP
font = font.nametofont("TkDefaultFont")
font.configure(size=14)
# WIDGET SETUP
libraryFileLbl = Label(text="Library Filepath:")
libraryFileTxt = Entry(font=("TkDefaultFont 12"))
libraryFileBtn = Button(text="...", command=handleOpenFileBtnClick)
savePathLbl = Label(text="Save Directory:")
savePathTxt = Entry(font=("TkDefaultFont 12"))
savePathBtn = Button(text="...", command=handleOpenSaveDirBtnClick)
saveFileLbl = Label(text="Save Filename:")
saveFileTxt = Entry(font=("TkDefaultFont 12"))
schoolLbl = Label(text="School:")
schoolTxt = Entry(font=("TkDefaultFont 12"))
parseBtn = Button(text="Run", command=handleRunBtnClick)
# WIDGET PLACEMENT
libraryFileLbl.place(x=10, y=10)
libraryFileTxt.place(x=156, y=13, width=406, height=28)
libraryFileBtn.place(x=570, y=13, width=28, height=28)
savePathLbl.place(x=19, y=47)
savePathTxt.place(x=156, y=50, width=406, height=28)
savePathBtn.place(x=570, y=50, width=28, height=28)
saveFileLbl.place(x=20, y=84)
saveFileTxt.place(x=156, y=87, width=442, height=28)
schoolLbl.place(x=83, y=121)
schoolTxt.place(x=156, y=124, width=442, height=28)
parseBtn.place(x=156, y=161, width=442, height=70)
# WIDGET BINDS
saveFileTxt.bind("<FocusOut>", handleSaveFileInput)
# MAINTAIN APP
window.mainloop()
