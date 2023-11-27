from tkinter import Tk, font, Label, Entry, Button, messagebox, filedialog, END
import os


def handleOpenFileBtnClick():
    filedata = filedialog.askopenfile()
    if filedata is not None:
        libraryFileTxt.delete(0, END)
        libraryFileTxt.insert(0, filedata.name)


def handleRunBtnClick():
    parseFile = libraryFileTxt.get()
    schoolName = schoolTxt.get()

    if os.path.exists(parseFile):
        if len(schoolName) > 0:
            pass
        else:
            messagebox.showinfo("No School Name", "Please enter a school name...")
    else:
        messagebox.showinfo("Invalid Filepath", "The filepath you entered is not valid...")


window = Tk()
window.resizable(width=False, height=False)
window.geometry("400x145")
window.eval("tk::PlaceWindow . center")

font = font.nametofont("TkDefaultFont")
font.configure(size=14)

libraryFileLbl = Label(text="Library File:")
libraryFileTxt = Entry(font=("TkDefaultFont 12"))
libraryFileBtn = Button(text="...", command=handleOpenFileBtnClick)
schoolLbl = Label(text="School:")
schoolTxt = Entry(font=("TkDefaultFont 12"))
parseBtn = Button(text="Run", command=handleRunBtnClick)

libraryFileLbl.place(x=10, y=10)
libraryFileTxt.place(x=120, y=13, width=230, height=28)
libraryFileBtn.place(x=360, y=13, width=28, height=28)
schoolLbl.place(x=45, y=47)
schoolTxt.place(x=120, y=50, width=268, height=28)
parseBtn.place(x=238, y=88, width=150)

window.mainloop()
