from tkinter import *
import tkinter.messagebox

class button:
    def __init__(self, window):
        frame = Frame(window)
        frame.pack()

        self.printButton = Button(frame, text = "Print", command = self.printMessage)
        self.printButton.pack(side = LEFT)

        self.quitButton = Button(frame, text="Quit", command = frame.quit)
        self.quitButton.pack(side=LEFT)

    def printMessage(self):
        print("Print Message")



window = Tk()
window.title("Wndow")
# window.geometry("500x500+100+200")

# ....................Images and Icons
# photo = PhotoImage(file="images.png")
# label = Label(window, image = photo)
# label.pack()

# ................Canvas Line and Shape
# canvas = Canvas(window, width = 300, height = 250)
# canvas.pack()
#
# line1 = canvas.create_line(0,0,300,250)
# line2 = canvas.create_line(0,250,300,0,fill = "red")
#
# box = canvas.create_rectangle(50,50,150,130,fill = "blue")
# canvas.delete(line1,line2)
# canvas.delete(ALL)

# .......................Message Box
# tkinter.messagebox.showinfo("Error Window", "Erro Errorrr Errorrrrr..")
# answer = tkinter.messagebox.askquestion("Quiz", "Do You Like Food..?")
# if answer == "yes":
#     print("Don't eat too much man..")


# .....................Menu Bar, Tool Bar, Status Bar
# def doNothing():
#     print("Do Nothing")
#
# menu = Menu(window)
# window.config(menu = menu)
#
# subMenu = Menu(menu)
# menu.add_cascade(label = "File", menu = subMenu)
# subMenu.add_command(label = "New Project...", command=doNothing)
# subMenu.add_command(label = "New...", command=doNothing)
# subMenu.add_separator()
# subMenu.add_command(label = "Exit", command=doNothing)
#
# editMenu = Menu(menu)
# menu.add_cascade(label = "Edit", menu = editMenu)
# editMenu.add_command(label = "Undo", command=doNothing)
# editMenu.add_command(label = "Redo", command=doNothing)
#
# toolBar = Frame(window, bg = "blue")
#
# insertButton = Button(toolBar, text = "Insert", command = doNothing)
# insertButton.pack(side = LEFT, padx = 2, pady = 2)
# printButton = Button(toolBar, text = "Print", command = doNothing)
# printButton.pack(side = LEFT, padx = 2, pady = 2)
# toolBar.pack(side = TOP, fill = X)
#
# status = Label(window, text = "Status", bd = 1, relief = SUNKEN, anchor = W)
# status.pack(side = BOTTOM, fill = X)


# ..................class object
# obj = button(window)

# .................Multiple Widgets
# def leftClick(event):
#     print("Left")
#
# def rightClick(event):
#     print("Right")
#
# frame = Frame(window, width = 300, height = 250)   # window geometry
# frame.bind("<Button-1>", leftClick)     #left click button
# frame.bind("<Button-3>", rightClick)    #right click button
# frame.pack()

# ..................Widgets
# def printN(event):
#     print("Osama Ahmed")
#
# button1 = Button(window, text = "Name")
# button1.bind("<Button-1>", printN)
# button1.pack(side = TOP)

# ............................Grid Layout
# labe1 = Label(window, text="Name")
# labe2 = Label(window, text="Password")
#
# entry1 = Entry(window)
# entry2 = Entry(window)
#
# labe1.grid(row = 0, sticky = E)
# labe2.grid(row = 2, sticky = E)
#
# entry1.grid(row = 0, column = 1)
# entry2.grid(row = 2, column = 1)
#
# checkBox = Checkbutton(window, text = "Keep me logged in")
# checkBox.grid(columnspan = 2)

# .......................Frames
# topFrame = Frame(window)
# topFrame.pack()
#
# bottomFrame = Frame(window)
# bottomFrame.pack(side = BOTTOM )

# ......................Buttons
# button1 = Button(topFrame, text = "Click", fg = "blue")
# button2 = Button(topFrame, text = "Click", fg = "green")
# button3 = Button(bottomFrame, text = "Click", fg = "red")
#
# button1.pack(side = LEFT)
# button2.pack(side = RIGHT)
# button3.pack(side = BOTTOM)

# ...........................Labels
# label = Label(window, text="Not Easy", bg = "blue", fg = "white")
# label.pack()
# labe2 = Label(window, text="Easy", bg = "black", fg = "white")
# labe2.pack(fill = X)
# labe3 = Label(window, text="Easy", bg = "black", fg = "white")
# labe3.pack(side = LEFT, fill = Y)

window.mainloop()

# import tkinter
#
# def createWindow():
#     window = tkinter.Tk()
#
#     window.title("Calculator")
#     window.geometry("500x500+100+200")
#     window.mainloop()
#
# if __name__ == "__main__":
#     createWindow()