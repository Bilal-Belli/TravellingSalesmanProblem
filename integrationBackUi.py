from tkinter import Tk, Label, StringVar, Button, Entry
import graph
import matplotlib.pyplot as plt
import time
import math
from itertools import permutations
from platform import system

# global declarations
global rows, cols
text_var = []   # empty arrays for your Entrys and StringVars
entries = []    # empty arrays for your Entrys and StringVars
global nbrNoeuds
nbrNoeuds = 0
EDGE_PATH_COLOR = "red"
global ADJLIST_GRAPH
ADJLIST_GRAPH = {}

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
    global ADJLIST_GRAPH
    ADJLIST_GRAPH = {}
    for i in range(rows):
        matrix.append([])
        for j in range(cols):
            matrix[i].append(text_var[i][j].get())
    for i in range(rows):
        monList = []
        for j in range(cols):
            if i==j:
                continue
            else:
                k = matrix[i][j]
                monList.append((str(j),int(k)))
        ADJLIST_GRAPH[str(i)] = monList
    print(ADJLIST_GRAPH)
    launchGraphPlotter()

# function that show the input labels
def matrixInput():
    global nbrNoeuds
    nbrNoeuds = nbSommets.get()
    label1.destroy()
    nbSommets.destroy()
    global rows, cols
    rows, cols = (int(nbrNoeuds) , int(nbrNoeuds))
    x = (screen_width / 2) - (700 / 2)
    y = (screen_height / 2 ) - (500 / 2)
    window.geometry(f'{700}x{500}+{int(x)}+{int(y)}')
    Label(window, text="Remplir la matrice d'Adjacence par les Couts", font=('arial', 10, 'bold'),
    bg="orange").place(x=15, y=20)
    button.place(x=310,y=20)
    button.configure(width=7)
    x2 = 0
    y2 = 0
    for i in range(rows):
        text_var.append([])
        entries.append([])
        for j in range(cols):
            text_var[i].append(StringVar())
            entries[i].append(Entry(window, textvariable=text_var[i][j],width=3))
            entries[i][j].place(x=60 + x2, y=55 + y2)
            x2 += 30
        y2 += 30
        x2 = 0
        i+=1
        j+=1
    button.configure(command= get_mat)

# needed algorithme for the exact one
def tsp(g, s):
    start = 0
    path = []
    n = len(g)
    vertex = []
    for i in range(n):
        if i != start:
            vertex.append(i)
    min_path = math.inf
    next_permutation = permutations(vertex)
    for i in next_permutation:
        current_pathweight = 0
        current_path = []
        k = start
        for j in i:
            current_pathweight += g[k][j]
            current_path.append((k, j))
            k = j
        current_pathweight += g[k][s]
        current_path.append((k, s))
        if current_pathweight < min_path:
            mipathn_path = current_pathweight
            path = current_path.copy()
    return path

# traveling salesman function (exact approach)
def tsp_path_exact(G: graph.Graph) -> list:
    g = G.tomatrix()
    start = 0
    path_idxs = tsp(g, start)
    cost = 0
    path = []
    for edge in path_idxs:
        i, j = edge
        path.append( (str(i+1), str(j+1)) )
        cost += g[i][j]
    return {'edges': path, 'cost': cost}

# checks if by adding an edge between u and v is gonna create a cycle in the graph g
def forms_cycle(g, u, v, last_visited=None) -> bool:
    if u == v :
        return True
    if u == None or len(g[u].adj) == 0 :
        return False
    next_neighbor = None
    for x,c in g[u].adj:
        if x != last_visited:
            next_neighbor = x
    return forms_cycle(g, next_neighbor, v, u)

# solve traveling salesman problem given a connexe graph (heuristic approach)
def tsp_path_heuristics(G: graph.Graph) -> list:
    g = graph.Graph(dict.fromkeys(G.vertices.keys(), set()))
    n = G.vertices_number()
    sorted_edges = sorted(G.unrepeated_edges(), key = lambda edge: edge[2])
    c = 0 
    i = 0 
    while c < n :
        u,v,cost = sorted_edges[i]
        if len(g[u].adj)<2 and len(g[v].adj)<2 and ((forms_cycle(g,u,v)==False and c<n-1) or (forms_cycle(g,u,v)==True and c==n-1)) :
            g.add_edge(u,v,cost)
            c+=1
        i+=1
    edges = g.unrepeated_edges()
    cost = sum([ c for u, v, c in edges ])
    path = [ (u, v) for u, v, w in edges ]
    return {'edges': path, 'cost': cost}

def tsp_path(G, tsp_func, alg_name):
    t = time.time()
    path = tsp_func(G)
    # print("path", path)
    dt = time.time() - t
    edge_color_key = {}
    for edge in path['edges']:
        u, v = edge
        edge_color_key[(u, v)] = EDGE_PATH_COLOR
        edge_color_key[(v, u)] = EDGE_PATH_COLOR
    title = f"\n {alg_name}\n tempsd'éxecution : {dt} secondes\n coût minimal : {path['cost']}"
    G.draw(edge_color_key=edge_color_key, title=title)

def plt_maximize():
    backend = plt.get_backend()
    cfm = plt.get_current_fig_manager()
    if backend == "wxAgg":
        cfm.frame.Maximize(True)
    elif backend == "TkAgg":
        if system() == "Windows":
            cfm.window.state("zoomed")  # This is windows only
        else:
            cfm.resize(*cfm.window.maxsize())
    elif backend == "QT4Agg":
        cfm.window.showMaximized()
    elif callable(getattr(cfm, "full_screen_toggle", None)):
        if not getattr(cfm, "flag_is_max", None):
            cfm.full_screen_toggle()
            cfm.flag_is_max = True
    else:
        raise RuntimeError("plt_maximize() is not implemented for current backend:", backend)

def launchGraphPlotter():
    global ADJLIST_GRAPH
    plt.figure(figsize=(16, 16), dpi=100)
    G = graph.Graph(ADJLIST_GRAPH)
    tsp_path(G, tsp_path_heuristics, "Algorithme pour solution approximative (heuristiques)")
    tsp_path(G, tsp_path_exact, "Algorithme pour solution complète")
    plt_maximize()
    plt.show()

# declaration objets d'affichage
label1 = Label(window, text="Entrer le nombre de Sommets", font=('arial', 10, 'bold'), bg="orange")
label1.place(x=110, y=15)
nbSommets = Entry(window,width=5, bg='black', foreground='white')
button = Button(window,text="Suivant", bg='orange', width=10,command= matrixInput, font=('arial', 10, 'bold'))

# affichage
nbSommets.place(x=195, y=45)
button.place(x=168,y=70)
window.mainloop()