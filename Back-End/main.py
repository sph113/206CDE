import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import subprocess
from subprocess import call


global R_ID
R_DATE = []
W_NAME = []
EXT_PRICE = []
addfile='Newreceipt.py'
editfile='Editreceipt.py'
def data():
    conn = sqlite3.connect('Z:\marathon.db')
    print ("Opened database successfully")
    c = conn.cursor()
    cursor=c.execute('''select Receipt_List.r_id,Receipt_List.r_date,staff_List.w_name,Receipt_List.EXT_PRICE, Receipt_List.DISCOUNT from Receipt_List inner join staff_list on Receipt_List.w_id = staff_list.w_id ORDER BY Receipt_List.R_ID;''')
    global R_ID
    R_ID = []
    R_DATE = []
    W_NAME = []
    EXT_PRICE = []
    for row in cursor:
        R_ID.append(row[0])
        R_DATE.append(row[1])
        W_NAME.append(row[2])
        EXT_PRICE.append(row[3]-row[4])
    i=0
    for x in R_ID:
        tv.insert(parent='', index=i, iid=i, text='', values=(str(R_ID[i]), str(R_DATE[i]), str(W_NAME[i]), str(EXT_PRICE[i])))
        i=i+1
    conn.commit()
    conn.close()

def show_selected():
    print(tv.selection())

def add():
    call(["python", addfile])

def edit():
    conn = sqlite3.connect('Z:\marathon.db')
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute('''DELETE From ORDERID_RECEIVER;''')
    conn.commit()
    idselect=tv.selection()
    id=int(idselect[0])
    print(R_ID[id])
    cursor = c.execute('''INSERT INTO ORDERID_RECEIVER VALUES (?);''',(R_ID[id],))
    conn.commit()
    conn.close()
    call(["python", editfile])

def delete():
    res = tkinter.messagebox.askquestion('Confirmation', 'Are you sure you want to delete?')
    if res == 'yes':
        cdelete()

def cdelete():
    idselect = tv.selection()
    id = int(idselect[0])
    conn = sqlite3.connect('Z:\marathon.db')
    c = conn.cursor()
    cursor = c.execute('''DELETE From Receipt_List where R_ID=?;''', (R_ID[id],))
    conn.commit()
    cursor = c.execute('''DELETE From Receipt_item where R_ID=?;''', (R_ID[id],))
    conn.commit()
    conn.close()
    refresh()

def refresh():
    tv.delete(*tv.get_children())
    data()

ws = Tk()
ws.title('Order List')
ws['bg']="white"

Topframe=Frame(ws)
title=Label(Topframe, text="Sales receipt")
title.pack()
Topframe.pack()

midframe = Frame(ws)
tv = ttk.Treeview(midframe)
tv['columns']=("Order_id","Date","Worker","Ext_price")
tv.column('#0', width=0, stretch=NO)
tv.column("Order_id", anchor=CENTER, width=80)
tv.column("Date", anchor=CENTER, width=80)
tv.column("Worker", anchor=CENTER, width=80)
tv.column("Ext_price", anchor=CENTER, width=80)

tv.heading('#0', text='', anchor=CENTER)
tv.heading("Order_id", text='Order id', anchor=CENTER)
tv.heading("Date", text='Date', anchor=CENTER)
tv.heading("Worker", text='Worker', anchor=CENTER)
tv.heading("Ext_price", text='Ext price', anchor=CENTER)

data()

tv.pack()

Button(midframe, text="Refresh", command=refresh).pack()
bframe=Frame(midframe)
Button(bframe, text="New Order", command=add).grid(row=0,column=0)
Button(bframe, text="Return item",command=edit).grid(row=0,column=1)
Button(bframe, text="DELETE",command=delete).grid(row=0,column=2)
bframe.pack()

midframe.pack()
ws.mainloop()