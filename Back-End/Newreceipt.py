import tkinter
from tkinter import *
from tkinter import ttk
import workers
import sqlite3
import datetime
from subprocess import call

R_ID=[]
P_id=[]
P_name=[]
P_price=[]
qty=[]
extprice=[]
TOT=[]
DIS=[]
DISBRAND=[]
DIS_P_ID=[]
plspid=[]
global DISCOUNTNO
DISCOUNTNO=[0]
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

def fromproductlist():
    call(["python", 'productlist.py'])
    conn = sqlite3.connect('Z:\marathon.db')
    c = conn.cursor()
    plspid = []
    cursor = c.execute('''select P_id from TEMP_NEWORDER''')
    for row in cursor:
        plspid.append(row[0])
    p_id = str(plspid[-1])
    cursor = c.execute('''Select P_ID, P_name, P_PRICE from Product_List where P_ID=?''', (p_id,))
    print(p_id)
    if p_id in P_id:
        qty[P_id.index(p_id)] = qty[P_id.index(p_id)] + 1
        extprice[P_id.index(p_id)] = int(P_price[P_id.index(p_id)]) * int(qty[P_id.index(p_id)])
    else:
        for row in cursor:
            P_id.append(row[0])
            P_name.append(row[1])
            P_price.append(row[2])
            qty.append(1)
            extprice.append(row[2] * 1)
    conn.commit()
    conn.close()
    tvinsert()
    caldis()


def update():
    order=orderno()
    conn = sqlite3.connect('Z:\marathon.db')
    print("Opened database successfully")
    c = conn.cursor()
    i=0
    c.execute("PRAGMA foreign_keys = ON")
    conn.commit()
    c.execute("PRAGMA foreign_keys")
    c.fetchone()
    cursor = c.execute('''Select W_ID from Staff_List WHERE W_NAME = ?;''',(str(worker.get()),))
    for row in cursor:
        W_ID=row[0]
    conn.commit()
    '''
    print (orderno(),datetime.datetime.today().strftime('%d-%b-%Y'),W_ID,tvinsert())
    for x in P_id:
        print (orderno(),P_id[i],qty[i],0)
        print (len(P_id[i]))
        i=i+1
    '''
    cursor = c.execute('''INSERT INTO RECEIPT_LIST (R_ID, R_DATE, W_ID, EXT_PRICE, DISCOUNT, TOTAL) VALUES (?,?,?,?,?,?);''',
                       (str(order),str(datetime.datetime.today().strftime('%d-%b-%Y')),str(W_ID),tvinsert(),caldis(),float(tvinsert())-float(caldis())))
    conn.commit()
    for x in P_id:
        cursor = c.execute('''INSERT INTO RECEIPT_item (R_ID, P_ID, QTY, RETURNED) VALUES (?,?,?,?);''',
                           (str(order),P_id[i],qty[i],0))
        conn.commit()
        i=i+1
    print(str(order),)
    cursor = c.execute('''DELETE From ORDERID_RECEIVER;''')
    conn.commit()
    cursor = c.execute('''INSERT INTO ORDERID_RECEIVER VALUES (?);''', (str(order),))
    conn.commit()
    conn.close()
    call(["python", 'print2file.py'])
    cancel()

def orderno():
    conn = sqlite3.connect('Z:\marathon.db')
    print("Opened database successfully")
    R_ID=[]
    c = conn.cursor()
    cursor = c.execute('''Select R_ID from Receipt_List ORDER BY R_ID;''')
    for row in cursor:
        R_ID.append(row[0])
    print(int(R_ID[-1]))
    conn.commit()
    conn.close()
    orderno=int(R_ID[-1])+1
    noofzero=8-len(str(orderno))
    print(noofzero)
    strono=""
    for i in range(noofzero):
        strono=strono+"0"
    strono=strono+str(orderno)
    return strono

def cancel():
    quit()

######treeeview selection#######
def show_selected():
    print(tv.selection())
###############################

def caldis():
    i=0
    w=0
    DISCOUNTNum=0
    DISCOUNTNO.clear()
    for x in P_id:
        z = 0
        for j in DIS_P_ID:
            if int(P_id[i]) == int(DIS_P_ID[z]):
                print(P_id[i],DIS_P_ID[z])
                DISCOUNTNO.append(round(float(P_price[i]) * float(qty[i]) * (1 - float(DIS[z])), 1))
            z = z + 1
        i=i+1
    for l in DISCOUNTNO:
        DISCOUNTNum=DISCOUNTNum+DISCOUNTNO[w]
        w=w+1
    DISNO.set("$ " + str(round(DISCOUNTNum,1)))
    return round(DISCOUNTNum,1)

def tvinsert():
    tv.delete(*tv.get_children())
    i=0

    y=0
    TOT=[]

    for x in P_id:
        tv.insert(parent='', index=i, iid=i, text='',
                  values=(str(P_id[i]), str(P_name[i]), str(P_price[i]), str(qty[i]), str(extprice[i])))
        y = y + float(P_price[i]) * float(qty[i])
        i = i + 1
    TOT.append(y)
    TOTAL.set("$ "+str(TOT[0]))
    return TOT[0]

def add():
    p_id=pid.get()
    conn = sqlite3.connect('Z:\marathon.db')
    print("Opened database successfully")
    c = conn.cursor()
    cursor = c.execute('''Select P_ID, P_name, P_PRICE from Product_List where P_ID=?''', (pid.get(),))
    if p_id in P_id:
        qty[P_id.index(p_id)]=qty[P_id.index(p_id)]+1
        extprice[P_id.index(p_id)]=int(P_price[P_id.index(p_id)])*int(qty[P_id.index(p_id)])
    else:
        for row in cursor:
            P_id.append(row[0])
            P_name.append(row[1])
            P_price.append(row[2])
            qty.append(1)
            extprice.append(row[2]*1)
    conn.commit()
    conn.close()
    tvinsert()
    caldis()

def delete_element(list_object, pos):
    if pos < len(list_object):
        list_object.pop(pos)

def minus():
    selectlist=tv.selection()
    selection=int(selectlist[0])
    qty[selection]=qty[selection]-1
    if int(qty[selection]) == 0:
        delete_element(P_id, selection)
        delete_element(P_name, selection)
        delete_element(P_price, selection)
        delete_element(qty, selection)
        delete_element(extprice, selection)
    else:
        extprice[selection] = int(P_price[selection]) * int(qty[selection])
    tvinsert()
    caldis()

def plus():
    selectlist=tv.selection()
    selection=int(selectlist[0])
    qty[selection]=qty[selection]+1
    extprice[selection] = int(P_price[selection]) * int(qty[selection])
    tvinsert()
    caldis()

getdiscount()
ws = Tk()
ws.title('New receipt')
ws['bg']="white"
Topframe=Frame(ws)
TFrame=Frame(Topframe)
title=Label(TFrame, text="Order Number : "+orderno())
title.pack()
TFrame.grid(row=0,column=0,sticky=tkinter.W)

DFrame=Frame(Topframe)
datetext=StringVar()
datetext.set(datetime.datetime.today().strftime('%d-%b-%Y'))
Date=Label(DFrame, textvariable=datetext)
Date.pack(side=tkinter.RIGHT)
DFrame.grid(row=0,column=1,sticky=tkinter.E)

Topframe.pack(fill='x')
Topframe.grid_columnconfigure(0, weight=1)

Sframe = Frame(ws)
plb=tkinter.Button(Sframe, text ="Product list", command=fromproductlist).grid(row=0,column=0,sticky=tkinter.W)
pid = StringVar()
SBox = Entry(Sframe, textvariable=pid)
SBox.grid(row=1,column=0,sticky=tkinter.W)
Sbutton= tkinter.Button(Sframe, text ="add", command=add)
Sbutton.grid(row=1,column=1,sticky=tkinter.W)
Sframe.pack(fill='x')

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
Button(Bsframe, text=" + ",command=plus).grid(row=0,column=0)
Button(Bsframe, text="  -  ",command=minus).grid(row=1,column=0)
Bsframe.grid(row=0,column=1)

worker = tkinter.StringVar(Middleframe)
OptionList=workers.data()
worker.set(OptionList[0])

opt = tkinter.OptionMenu(Middleframe, worker, *OptionList)
opt.config( font=('Helvetica', 12))
opt.grid(row=1,column=0,sticky=tkinter.W)

Middleframe.pack()

Bottomframe = Frame(ws)
numberframe=Frame(Bottomframe)
Dlabel = Label(numberframe, text="Discount")
Dlabel.grid(row=0,column=1,sticky=tkinter.E)
DISNO=StringVar()
DISNO.set("$ 0")
dlabel = Label(numberframe, textvariable=DISNO)
dlabel.grid(row=0,column=2,sticky=tkinter.E)
Tlabel = Label(numberframe, text="Total" )
Tlabel.grid(row=1,column=1,sticky=tkinter.E)
TOTAL=StringVar()
TOTAL.set("$ 0")
tlabel = Label(numberframe, textvariable=TOTAL)
tlabel.grid(row=1,column=2,sticky=tkinter.E)
numberframe.grid(row=0,column=0,sticky=tkinter.E)
Fframe=Frame(Bottomframe)
Button(Fframe, text="Cancel", command=cancel).grid(row=0,column=0)
Button(Fframe, text="Save & Print",command=update).grid(row=0,column=2)
Fframe.grid(row=3,column=0,sticky=tkinter.E)
Bottomframe.pack(fill='x')
Bottomframe.grid_columnconfigure(0, weight=1)

ws.mainloop()
