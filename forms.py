from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import URL, NumberRange,  Optional


class Add_pet(FlaskForm):

         name       = StringField("Name")
         species    = SelectField("Species")
         photo      = StringField("Photo URL", validators=[URL(message='Please enter a valid URL'), Optional()])
         age        = IntegerField("Age", validators=[NumberRange(min=0, max=30, message='The age must be between 0 and 30!')])
         notes      = TextAreaField("Notes")
         available  = BooleanField("Available")