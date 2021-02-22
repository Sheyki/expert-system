import csv
import tkinter as tk
from tkinter import messagebox

# GUI guide: https://realpython.com/python-gui-tkinter/#adding-a-widget
# dataset: https://www.kaggle.com/anthonypino/melbourne-housing-market

# vars
csv_file = "melb_data.csv"
data_all = []
columns = ["Parametr", "Wartość (min)", "Wartość (max)", "Istotność"]
rows = ["Cena", "Pokoje", "Odleglosc od centrum", "Sypialnie", "Łazienki", "Miejsce parkingowe"]

# load data
with open(csv_file, newline='') as file:
    line = csv.reader(file, delimiter=',', quotechar='|')
    for row in line:
        new_row = [row[4], row[2], row[8], row[10], row[11], row[12], row[13], row[19], row[0], row[1],
                   row[15], row[17], row[18]]
        data_all.append(new_row)
order = data_all[0]
del(data_all[0])

for k in range(len(data_all)):
    for j in range(7):
        if data_all[k][j] == '':
            data_all[k][j] = 0
        else:
            data_all[k][j] = float(data_all[k][j])

data_col = [[row[0] for row in data_all],
            [row[1] for row in data_all],
            [row[2] for row in data_all],
            [row[3] for row in data_all],
            [row[4] for row in data_all],
            [row[5] for row in data_all],
            [row[6] for row in data_all],
            [row[7] for row in data_all],
            [row[8] for row in data_all]]


def sort_order():
    sort_order_ = []
    for i in range(len(rows)-1):
        sort_order_.append([w[i].get(), i])
    new_sort = sorted(sort_order_, reverse=True)
    return new_sort


def key_func(item):
    # |(średnia min/max)-cena|
    new_v = []
    for i in range(len(rows)-1):
        new_v.append(abs(((va[i].get()+vi[i].get())/2)-item[i]))
    new_order = sort_order()
    key = []
    for i in range(len(rows)-1):
        key.append(new_v[new_order[i][1]])
    return tuple(key)


def suggestion():
    data_new = sorted(data_all, key=key_func)
    in_b = False
    iter = -1
    while in_b == False and iter < len(data_new)-1:
        in_b = True
        iter = iter+1
        s = data_new[iter]
        for i in range(len(w)):
            if (s[i] > va[i].get() or s[i] < vi[i].get()):
                in_b = False
    if in_b == True:
        print(s)
        formatted_text = "Adres: "+str(s[7])+", "+str(s[8])+", "+str(s[9])+"\nCena: "+str(s[0])+"\nRok budowy: "+str(s[10])+"\nPokoje: "+str(s[1])+", sypialnie: "+str(s[3])+", łazienki: "+str(s[4])+"\nMiejsca parkingowe: "+str(s[5])
    else:
        formatted_text = "Jeden z podanych parametrów nie mógł zostać spełniony.\nSpróbuj podać mniej restrykcyjne parametry."
    messagebox.showinfo("Propozycja", formatted_text)


def update():
    for i in range(len(vi)):
        vi[i].configure(to=va[i].get())
        va[i].configure(from_=vi[i].get())
    window.after(100, update)


window = tk.Tk()
window.title("System Ekspertowy - zakup domu w Melbourne")
n = []
vi = []
va = []
w = []
for i in range(len(rows)):
    for j in range(4):
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=5, pady=5)
        if i > 0:
            if j == 0:  # name
                n.append(tk.Label(master=frame, text=rows[i-1]))
                n[-1].pack()
            elif j == 1:  # value
                vi.append(tk.Scale(master=frame, from_=min(data_col[i-1]), to=max(data_col[i-1]), orient=tk.HORIZONTAL))
                vi[-1].pack()
            elif j == 2:  # value
                va.append(tk.Scale(master=frame, from_=min(data_col[i-1]), to=max(data_col[i-1]), orient=tk.HORIZONTAL))
                va[-1].set(max(data_col[i-1]))
                va[-1].pack()
            elif j == 3:  # weight
                w.append(tk.Scale(master=frame, from_=0, to=100, orient=tk.HORIZONTAL))
                w[-1].set(50)
                w[-1].pack()
        else:  # column titles
            t = tk.Label(master=frame, text=columns[j])
            t.pack()
confirm = tk.Button(window, text="Zatwierdz", command=suggestion)
confirm.grid()
blank = tk.Label(master=window, text="\n")
blank.grid()
window.after(100, update)
window.mainloop()
