import sqlite3
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import *
from tkinter.ttk import *
import sv_ttk
tk = Tk()
sv_ttk.use_light_theme()
tk.withdraw() #Hide tk

Home = Toplevel(tk) #Home page toplevel
Home.protocol("WM_DELETE_WINDOW", exit) #avoid running program after toplevel is closed.
Home.title("ScoreManager - Home")

#create add student window
AddPage = Toplevel(tk) #Add new student toplevel
AddPage.withdraw() #hide this TopLevel temporary
AddPage.title("Add new Student")
AddPage.protocol("WM_DELETE_WINDOW", AddPage.iconify)
Label(AddPage, text="Student Name").pack()
Student_Name_New = Entry(AddPage)
Student_Name_New.pack()
Label(AddPage, text="Student Score").pack()
Student_Score_New = Entry(AddPage)
Student_Score_New.pack()
Label(AddPage, text="Student Details").pack()
Student_Detail_New = Entry(AddPage)
Student_Detail_New.pack()

#create remove Student window:
RemovePage = Toplevel(tk)
RemovePage.withdraw()
AddPage.title("Add new Student")
AddPage.protocol("WM_DELETE_WINDOW", AddPage.iconify)
Label(AddPage, text="Enter Student Name:").pack()
Student_Name_Remove = Entry(RemovePage)
Student_Name_Remove.pack()

Buttons = LabelFrame(tk, text="Buttons")
Buttons.pack(fill="x", anchor="nw")
Add_Person_image = PhotoImage(file="Icons/AddPerson_Icons8.png")
Remove_Person_image = PhotoImage(file="Icons/icons8-remove-user-female-32.png")
OpenDatabase_image = PhotoImage(file="Icons/icons8-import-32.png")
save_changes_image = PhotoImage(file="Icons/icons8-save-32.png")

#Listboxs (Name of Student, Score, and Details.)
Listboxes = LabelFrame(tk, text="Students                       Scores                           Details")
Listboxes.pack(anchor="s")
Names = Listbox(Listboxes)
Names.grid(row=0, column=0)
Scores = Listbox(Listboxes)
Scores.grid(row=0, column=1)
Details = Listbox(Listboxes)
Details.grid(row=0, column=2)
ListScroll = Scrollbar(Listboxes)
ListScroll.grid(row=0, column=3, sticky="nse")
def ScrollAllListboxes(a):
    try:
        Names.yview(a[0], a[1], a[2])
        Scores.yview(a[0], a[1], a[2])
        Details.yview(a[0], a[1], a[2])
    except:
        Names.yview(a[0], a[1])
        Scores.yview(a[0], a[1])
        Details.yview(a[0], a[1])
for listbox in [Names, Scores, Details]:
    listbox.config(yscrollcommand=ListScroll.set)
ListScroll.config(command=lambda *args: ScrollAllListboxes([*args]))

#functions:
def Reload_Database():
    #Remove existing things from listboxes
    Names.delete(0, "end")
    Scores.delete(0, "end")
    Details.delete(0, "end")
    
    DisplayScores()
def AddNewStudent():
    Student_Name_New_ = Student_Name_New.get()
    Student_Score_New_ = Student_Score_New.get()
    Student_Detail_New_ = Student_Detail_New.get()

    Names.insert("end", Student_Name_New_)
    Scores.insert("end", Student_Score_New_)
    Details.insert("end", Student_Detail_New_)

    DatabaseCur.execute("INSERT INTO Students (Name, Score, Details) VALUES ('"+Student_Name_New_+"', '"+Student_Score_New_+"', '"+Student_Detail_New_+"')")
    Database.commit()
def del_student():
    name = Student_Name_Remove.get()
    command = "DELETE FROM Students\nWHERE Name = '" + name + "'"
    DatabaseCur.execute(command)
    Database.commit()

    Reload_Database()
def DisplayScores():
    tk.deiconify()
    Home.iconify()
    Students_Name = list(DatabaseCur.execute("SELECT Name FROM Students"))
    Students_Score = list(DatabaseCur.execute("SELECT Score FROM Students"))
    Students_Details = list(DatabaseCur.execute("SELECT Details FROM Students"))
    print(Students_Name)
    for Name in Students_Name:
        Names.insert("end", Name)
    for Score in Students_Score:
        Scores.insert("end", Score)
    for Detail in Students_Details:
        Details.insert("end", Detail)

def CreateDatabase():
    global Database, DatabaseCur
    NewDatabasePath = asksaveasfilename(title="Create Database", filetypes=(("Database", "*.db"), ("All Files", "*.*")), defaultextension="*.db")
    Database = sqlite3.connect(NewDatabasePath)
    DatabaseCur = Database.cursor()
def OpenDatabase():
    global Database, DatabaseCur
    NewDatabasePath = askopenfilename(title="Open Database", filetypes=(("Database", "*.db"), ("All Files", "*.*")), defaultextension="*.db")
    Database = sqlite3.connect(NewDatabasePath)
    DatabaseCur = Database.cursor()
    DisplayScores()

#Home Label and Buttons:
Add_Person_btn = Button(Buttons, image=Add_Person_image, command=AddPage.deiconify)
Add_Person_btn.pack(anchor="nw")
Button(Buttons, image=Remove_Person_image, command=RemovePage.deiconify).place(x=55)
Button(AddPage, command=AddNewStudent, text="Save").pack()
Button(RemovePage, command=del_student, text="Remove Student").pack()
Label(Home, text="Welcome! What would you like to do?", font=("Hey October", 24)).pack()
Button(Home, text="Create New Database", width=50, command=CreateDatabase).pack()
Button(Home, text="Open Existing Database", width=50, command=OpenDatabase).pack()
tk.mainloop()