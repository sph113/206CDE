import tkinter
from tkinter import *
from tkinter import ttk
import sqlite3

P_id=[]
P_name=[]
P_price=[]

def data():
    i=0
    conn = sqlite3.connect('Z:\marathon.db')
    c = conn.cursor()
    cursor = c.execute('''select P_id, P_NAME, P_PRICE from Product_List ORDER BY P_id;''')
    for row in cursor:
        P_id.append(row[0])
        P_name.append(row[1])
        P_price.append(row[2])
    for x in P_id:
        ptv.insert(parent='', index=i, iid=i, text='',
                  values=(str(P_id[i]), str(P_name[i]), str(P_price[i])))
        i = i + 1
    conn.commit()
    conn.close()
def additem():
    sel=ptv.selection()
    conn = sqlite3.connect('Z:\marathon.db')
    c = conn.cursor()
    cursor = c.execute('''Delete from TEMP_NEWORDER''')
    cursor = c.execute('''INSERT INTO TEMP_NEWORDER (P_id,QTY) VALUES(?,1)''',(P_id[int(sel[0])],))
    conn.commit()
    quit()


pl = Tk()
tvframe=Frame(pl)
ptv = ttk.Treeview(tvframe)
ptv['columns'] = ("Pid", "Pname", "Pprice")
ptv.column('#0', width=0, stretch=NO)
ptv.column("Pid", anchor=CENTER, width=80)
ptv.column("Pname", anchor=CENTER, width=80)
ptv.column("Pprice", anchor=CENTER, width=80)

ptv.heading('#0', text='', anchor=CENTER)
ptv.heading("Pid", text='Id', anchor=CENTER)
ptv.heading("Pname", text='Product', anchor=CENTER)
ptv.heading("Pprice", text='Price', anchor=CENTER)
data()
ptv.pack()
tvframe.grid(row=0, column=0)

add=Button(pl, text="Add", command=additem)
add.grid(row=0, column=1)
pl.mainloop()