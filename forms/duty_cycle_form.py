from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class DutyCycleForm(FlaskForm):
    cycle = IntegerField('cycle', validators=[DataRequired()])

