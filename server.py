import os
from flask import Flask

SECRET_KEY = os.urandom(32)

from flask import render_template, redirect, url_for, request

#from duty_cycle_manager import DutyCycleManager
from forms.duty_cycle_form import DutyCycleForm
from db import *

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

#dc = DutyCycleManager()

@app.route('/', methods=["GET", "POST"])
def index():
    form = DutyCycleForm()
    if request.method == 'POST':
        #POST
        cycle = int(request.form.get('cycle'))
        DutyCycle.set_cycle(cycle)
        d = {
            "duty_cycle": cycle
        }
        return render_template("dutycycle.html", form=form, **d)
    else:
        #GET
        d = {
            "duty_cycle": DutyCycle.get_cycle()
        }
        return render_template("dutycycle.html", form=form, **d)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
