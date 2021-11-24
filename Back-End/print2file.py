# imports module
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import B6
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle as PS
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT
import os
R_ID=[]
R_DATE=[]
W_ID=[]
worker=[]
TOTAL=[]
DISCOUNT=[]
EXT_TOTAL=[]
'''repeat value'''
P_ID=[]
P_NAME=[]
P_PRICE=[]
QTY=[]
RETURNED=[]
EXT_PRICE=[]

def strike(text):
    result = ''
    result = "<strike>"+text+"</strike>"
    return result

conn = sqlite3.connect('Z:\marathon.db')
print("Opened database successfully")
c = conn.cursor()
cursor = c.execute('''SELECT R_ID from ORDERID_RECEIVER;''')
for row in cursor:
    R_ID.append(row[0])
conn.commit()
cursor = c.execute('''SELECT R_DATE, W_ID, EXT_PRICE,DISCOUNT,TOTAL from REceipt_List WHERE R_ID = ?;''',(R_ID[0],))
for row in cursor:
    R_DATE.append(row[0])
    W_ID.append(row[1])
    TOTAL.append(row[2])
    DISCOUNT.append(row[3])
    EXT_TOTAL.append(row[4])
conn.commit()
cursor = c.execute('''select Receipt_item.P_id, Product_List.P_name, Product_List.P_price, Receipt_item.Qty, Receipt_item.Returned  from Receipt_item inner join Product_List on Receipt_item.P_id = Product_list.P_id where Receipt_item.R_ID=?;''',(R_ID[0],))
for row in cursor:
    P_ID.append(row[0])
    P_NAME.append(row[1])
    P_PRICE.append(row[2])
    QTY.append(row[3])
    RETURNED.append(int(row[4]))
    EXT_PRICE.append(int(row[2])*int(row[3]))
conn.commit()
cursor = c.execute('''select W_NAME from Staff_list WHERE W_ID = ?''',(W_ID[0],))
for row in cursor:
    worker.append(row[0])
conn.commit()
conn.close()
a=0
for y in P_ID:
    if int(RETURNED[a]) == 1:
        P_ID[a] = strike(str(P_ID[a]))
        P_NAME[a] = strike(str(P_NAME[a]))
        P_PRICE[a] = strike(str(P_PRICE[a]))
        QTY[a] = strike(str(QTY[a]))
        EXT_PRICE[a] = strike(str(EXT_PRICE[a]))
    a = a + 1
print(P_ID)


logo="logo.png"
text1="Order number : *#"+ str(R_ID[0])
text2="Order date : " + str(R_DATE[0])
text25="Staff handle : "+str(worker[0])
text3=str("Sub total : $" + str(TOTAL[0]))
text4=str("Discount: " + str(DISCOUNT[0]))
text5=str("Total : $" + str(float(TOTAL[0])-float(DISCOUNT[0])))

P1=Paragraph(text1, bulletText=None)
P2=Paragraph(text2, bulletText=None)
P25=Paragraph(text25, bulletText=None)
P3=Paragraph(text3,PS('New',alignment = TA_RIGHT), bulletText=None)
P4=Paragraph(text4,PS('New',alignment = TA_RIGHT), bulletText=None)
P5=Paragraph(text5,PS('New',alignment = TA_RIGHT), bulletText=None)

DATA1 = [
        ["Item No.","Item Name                                  ", "Qty", "Price"],
    ]
z=0
for x in P_ID:
    '''data=[str(P_ID[z]),str(P_NAME[z]),str(QTY[z]),str(EXT_PRICE[z])]'''
    data = [Paragraph(str(P_ID[z]), bulletText=None), Paragraph(str(P_NAME[z]), bulletText=None), Paragraph(str(QTY[z]), bulletText=None), Paragraph(str(EXT_PRICE[z]), bulletText=None)]
    DATA1.append(data)
    z=z+1

# creating a Base Document Template of page size A5
outfilename = str(R_ID[0])+".pdf"
outfiledir = """Z:\order"""
outfilepath = os.path.join( outfiledir, outfilename )
pdf = SimpleDocTemplate(outfilepath, pagesize=B6)

    # standard stylesheet defined within reportlab itself
styles = getSampleStyleSheet()

    # fetching the style of Top level heading (Heading1)
title_style = styles["Heading1"]

    # 0: left, 1: center, 2: right
title_style.alignment = 1

    # creating the paragraph with
    # the heading text and passing the styles of it
title = Image(logo, 4*inch, 1*inch)

spacer=Spacer(1, 12)

    # creates a Table Style object and in it,
    # defines the styles row wise
    # the tuples which look like coordinates
    # are nothing but rows and columns
style1 = TableStyle(
        [
        ("BACKGROUND", (0, 0), (3, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ]
    )

    # creates a table object and passes the style to it
table1 = Table(DATA1, style=style1)
# final step which builds the
# actual pdf putting together all the elements

pdf.build([title, spacer,P1,P2,P25,table1,spacer,P3,P4,P5])