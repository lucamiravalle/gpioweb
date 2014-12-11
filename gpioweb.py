
from flask import *
from flask.ext.bootstrap import Bootstrap
import datetime
import RPi.GPIO as GPIO
import os
from functools import wraps

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = 'L54u2pY9W8nkI1CWKN7n3ivq1SPy1jnt' #random key



now = datetime.datetime.now()
timeString = now.strftime("%Y-%m-%d %H:%M")
res = os.popen('vcgencmd measure_temp').readline()
res=res.replace("temp=","")

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route("/")
def hello():
   return render_template('login.html')
   
@app.route("/gpioweb")
@login_required
def home():
    message = "Logged in"
    templateData = {
        'message' : message,
        'time' : timeString,
        'temperature' : res
    }
    return render_template('gpioweb.html', **templateData)
   
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != 'test' or request.form['password'] != 'test':
                return 'Error'                
        else:
            session['logged_in']= True
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))    
    

@app.route("/heat")
@login_required
def actionheat():
    os.system("sudo irsend SEND_ONCE TOSHIBA KEY_POWER ")
    message = "Command received: heating up!"
    templateData = {
        'message' : message,
        'time' : timeString,
        'temperature' : res
    }
    return render_template('gpioweb.html', **templateData)
    
@app.route("/cool")
@login_required
def actioncool():
   # os.system("sudo irsend SEND_ONCE TOSHIBA KEY_POWER ")
    message = "Command received: cooling down!"
    templateData = {
        'message' : message,
        'time' : timeString,
        'temperature' : res
    }
    return render_template('gpioweb.html', **templateData)
    
@app.route("/temp")
@login_required
def actiontemp():
    #res = os.popen('vcgencmd measure_temp').readline()
    #res=res.replace("temp=","")
    temperature_file = open("out","r")
    res= temperature_file.readline()
    print res
    temperature_file.close()
    return res

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=442, debug=True)
