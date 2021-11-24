import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import workers
from subprocess import call
R_ID=[]
P_ID = []
P_NAME = []
P_PRICE = []
QTY = []
RETURNED = []
EXT_PRICE = []
DATE=[]
W_ID=[]
TOT=[]
stafflist=[]
DIS_P_ID=[]
DIS=[]
conn = sqlite3.connect('Z:\marathon.db')
print("Opened database successfully")
c = conn.cursor()
cursor = c.execute('''SELECT R_ID from ORDERID_RECEIVER;''')
for row in cursor:
    R_ID.append(row[0])
conn.commit()

def getdiscount():
    conn = sqlite3.connect('Z:\marathon.db')
    c = conn.cursor()
    '''###cursor = c.execute('Select BRAND_LIST.Brand,Discount.D_PERCENTAGEOFF from Discount inner join Brand_list ON Discount.B_ID=Brand_list.B_ID')
    for row in cursor:
        DISBRAND.append(row[0])
        DIS.append(row[1])
    conn.commit()'''
    cursor = c.execute(
        '''Select Product_List.P_ID,Discount.D_PERCENTAGEOFF from Discount inner join Product_List ON Discount.B_ID=Product_List.B_ID where Product_List.B_ID = Discount.B_ID''')
    for row in cursor:
        DIS_P_ID.append(row[0])
        DIS.append(row[1])
    conn.commit()
    conn.close()

def strike(text):
    result = ''
    for c in text:
        result = result + c + '\u0336'
    return result

def tvinsert():
    tv.delete(*tv.get_children())
    i=0
    y=0
    TOT=[]
    for x in P_ID:
        if RETURNED[i] == 0:
            y = y + float(P_PRICE[i]) * float(QTY[i])
            tv.insert(parent='', index=i, iid=i, text='',
                      values=(str(P_ID[i]), str(P_NAME[i]), str(P_PRICE[i]), str(QTY[i]), str(EXT_PRICE[i])))
        elif RETURNED[i] == 1:
            tv.insert(parent='', index=i, iid=i, text='',
                      values=(strike(str(P_ID[i])), strike(str(P_NAME[i])), strike(str(P_PRICE[i])), strike(str(QTY[i])), strike(str(EXT_PRICE[i]))))
        i = i + 1
    TOT.append(y)
    TOTAL.set("$ "+str(TOT[0]))
    return TOT[0]

def returnitem():
    select=[]
    select=tv.selection()
    print(P_ID[int(select[0])], P_NAME[int(select[0])], P_PRICE[int(select[0])], QTY[int(select[0])],EXT_PRICE[int(select[0])])
    print(tv.item(select,'values'))
    conn = sqlite3.connect('Z:\marathon.db')
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute('''UPDATE REceipt_item set RETURNED=1 WHERE R_ID=? and P_ID= ?''',(R_ID[0],P_ID[int(select[0])]))
    conn.commit()
    conn.close()
    P_ID.clear()
    P_NAME.clear()
    P_PRICE.clear()
    QTY.clear()
    RETURNED.clear()
    EXT_PRICE.clear()
    data()
    
def caldis():
    select = []
    select = tv.selection()
    i=0
    w=0
    z = 0
    for j in DIS_P_ID:
        if int(P_ID[int(select[0])]) == int(DIS_P_ID[z]):
            print(select[0],DIS_P_ID[z])
            tkinter.messagebox.showinfo('error','Discount item cannot return')
            w=1
            break
        z = z + 1
    if w == 0:
        returnitem()
    
            
def cancel():
    quit()

def data():
    conn = sqlite3.connect('Z:\marathon.db')
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute(
        '''select Receipt_item.P_id, Product_List.P_name, Product_List.P_price, Receipt_item.Qty, Receipt_item.Returned  from Receipt_item inner join Product_List on Receipt_item.P_id = Product_list.P_id where Receipt_item.R_ID=?;''',(R_ID[0],))
    for row in cursor:
        P_ID.append(row[0])
        P_NAME.append(row[1])
        P_PRICE.append(row[2])
        QTY.append(row[3])
        RETURNED.append(row[4])
        EXT_PRICE.append(float(row[2])*float(row[3]))
    conn.commit()
    conn.close()
    tvinsert()
def orderdetail():
    conn = sqlite3.connect('Z:\marathon.db')
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute('''select R_DATE,W_ID from Receipt_list where R_ID=?''',(R_ID[0],))
    for row in cursor:
        DATE.append("Order date:"+str(row[0]))
        W_ID.append(row[1])
    conn.commit()
    conn.close()

def worker():
    conn = sqlite3.connect('Z:\marathon.db')
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute('''select W_NAME from Staff_list''')
    for row in cursor:
        stafflist.append(row[0])
    conn.commit()
    conn.close()

def printpdf():
    conn = sqlite3.connect('Z:\marathon.db')
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute('''UPDATE Receipt_List SET EXT_PRICE=? WHERE R_ID=?''', (tvinsert(),R_ID[0]))
    conn.commit()
    conn.close()
    call(["python", 'print2file.py'])
    cancel()

######treeeview selection#######
def show_selected():
    print(tv.selection())
###############################

getdiscount()
ws = Tk()
ws.title('Return item')
ws['bg']="white"
Topframe=Frame(ws)
TFrame=Frame(Topframe)
title=Label(TFrame, text="Sales receipt")
title.pack()
TFrame.grid(row=0,column=0,sticky=tkinter.W)

orderdetail()

DFrame=Frame(Topframe)
Date=Label(DFrame, text=DATE[0])
Date.pack(side=tkinter.RIGHT)
DFrame.grid(row=0,column=1,sticky=tkinter.E)

TFrame=Frame(Topframe)
Time=Label(TFrame, text="Time")
Time.pack(side=tkinter.RIGHT)
TFrame.grid(row=1,column=1,sticky=tkinter.E)

Topframe.pack(fill='x')
Topframe.grid_columnconfigure(0, weight=1)


Middleframe = Frame(ws)

tvframe = Frame(Middleframe)
#######################treewiew#######################################
tv = ttk.Treeview(tvframe)
tv['columns']=("Item#","Item_name","Price","Qty","Ext_price")
tv.column('#0', width=0, stretch=NO)
tv.column("Item#", anchor=CENTER, width=80)
tv.column("Item_name", anchor=CENTER, width=80)
tv.column("Price", anchor=CENTER, width=80)
tv.column("Qty", anchor=CENTER, width=80)
tv.column("Ext_price", anchor=CENTER, width=80)

tv.heading('#0', text='', anchor=CENTER)
tv.heading("Item#", text='Item #', anchor=CENTER)
tv.heading("Item_name", text='Item name', anchor=CENTER)
tv.heading("Price", text='Price', anchor=CENTER)
tv.heading("Qty", text='Qty', anchor=CENTER)
tv.heading("Ext_price", text='Ext price', anchor=CENTER)


tv.pack()
############################################################
tvframe.grid(row=0,column=0)
Bsframe= Frame(Middleframe)
Button(Bsframe, text="Return item", command=caldis).grid(row=1,column=0)
Bsframe.grid(row=0,column=1)

worker = tkinter.StringVar(Middleframe)
OptionList=workers.data()
worker.set(OptionList[int(W_ID[0])-1])

opt = tkinter.OptionMenu(Middleframe, worker, *OptionList)
opt.config( font=('Helvetica', 12))
opt.grid(row=1,column=0,sticky=tkinter.W)


Middleframe.pack()

Bottomframe = Frame(ws)
numberframe=Frame(Bottomframe)
TOTAL=StringVar()
TOTAL.set("$ 0")
Tlabel = Label(numberframe, text="Total" )
Tlabel.grid(row=0,column=1,sticky=tkinter.E)
tlabel = Label(numberframe, textvariable=TOTAL)
tlabel.grid(row=0,column=2,sticky=tkinter.E)
numberframe.grid(row=0,column=0,sticky=tkinter.E)
Fframe=Frame(Bottomframe)
Button(Fframe, text="Cancel",command=cancel).grid(row=0,column=0)
Button(Fframe, text="Save & Print", command=printpdf).grid(row=0,column=2)
Fframe.grid(row=3,column=0,sticky=tkinter.E)
Bottomframe.pack(fill='x')
Bottomframe.grid_columnconfigure(0, weight=1)

data()

ws.mainloop()
