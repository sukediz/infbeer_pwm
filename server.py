import os
from flask import Flask

SECRET_KEY = os.urandom(32)

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from flask import render_template, redirect, url_for, request

from duty_cycle_manager import DutyCycleManager

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

class DutyCycleForm(FlaskForm):
    cycle = IntegerField('cycle', validators=[DataRequired()])

dc = DutyCycleManager()

@app.route('/', methods=["GET", "POST"])
def index():
    curr_dc = dc.get_cycle()
    form = DutyCycleForm(cycle=dc.get_cycle())
    if request.method == 'POST':
        app.logger.error(request.form.get('cycle'))
        dc.set_cycle(app, int(request.form.get('cycle')))
        app.logger.error(dc.get_cycle())
    d = {
        "duty_cycle": curr_dc
    }
    return render_template("dutycycle.html", form=form, **d)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
