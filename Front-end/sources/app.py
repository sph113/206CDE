from flask import *
app = Flask(__name__)


def printr():
    redirect('http://xnobe.synology.me/order/'+'00000016'+'.pdf')

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/',methods=['POST'])
def texts():
    R_ID = request.form["txt"]
    print(R_ID)
    return redirect('http://xnobe.synology.me/order/'+R_ID+'.pdf',code=303)

if __name__ == '__main__':
    app.run(debug=True)
