from tkinter import Tk, Label, StringVar, Button, Entry

# global declarations
global rows, cols
text_var = []   # empty arrays for your Entrys and StringVars
entries = []    # empty arrays for your Entrys and StringVars
global nbrNoeuds
nbrNoeuds = 0

# Designate Height and Width of our app
app_width = 400
app_height = 150
# declare the window
window = Tk()
window.title('TP4: Problem PVC - BILAL BELLI')
window.configure(bg='white')
# The Height and Width of our pc screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2 ) - (app_height / 2)
window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
# window.resizable(False, False)

# callback function to get your StringVars
def get_mat():
    matrix = []
    for i in range(rows):
        matrix.append([])
        for j in range(cols):
            matrix[i].append(text_var[i][j].get())
    print(matrix)

# function that show the input labels
def matrixInput():
    global nbrNoeuds
    nbrNoeuds = nbSommets.get()
    label1.destroy()
    nbSommets.destroy()
    global rows, cols
    rows, cols = (int(nbrNoeuds) , int(nbrNoeuds))
    # window.resizable(true, true)
    Label(window, text="Remplir la matrice d'Adjacence par les Couts", font=('arial', 10, 'bold'),
    bg="orange").place(x=15, y=20)
    button.place(x=310,y=20)
    button.configure(width=7)
    x2 = 0
    y2 = 0
    for i in range(rows):
        # append an empty list to your two arrays
        # so you can append to those later
        text_var.append([])
        entries.append([])
        for j in range(cols):
            # append your StringVar and Entry
            text_var[i].append(StringVar())
            entries[i].append(Entry(window, textvariable=text_var[i][j],width=3))
            entries[i][j].place(x=60 + x2, y=55 + y2)
            x2 += 30
        y2 += 30
        x2 = 0
        i+=1
        j+=1
    button.configure(command= get_mat)

# declaration objets d'affichage
label1 = Label(window, text="Entrer le nombre de Sommets", font=('arial', 10, 'bold'), bg="orange")
label1.place(x=110, y=15)
nbSommets = Entry(window,width=5, bg='black', foreground='white')
button = Button(window,text="Suivant", bg='orange', width=10,command= matrixInput, font=('arial', 10, 'bold'))

# affichage
nbSommets.place(x=195, y=45)
button.place(x=168,y=70)
window.mainloop()