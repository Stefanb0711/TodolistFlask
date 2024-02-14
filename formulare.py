from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length

class AddTodoTaskForm(FlaskForm):
    new_todo = StringField('ToDo hinzufügen', validators=[DataRequired()], render_kw={"placeholder": "ToDo hinzufügen", "style": "margin-top:50px;"})
    submit = SubmitField('Todo hinzufügen', render_kw={"type": "image", "src":"static/Bilder/plus.svg", "style": "filter: invert(100%);"})

class AddTodoAreaForm(FlaskForm):
    new_area = StringField(label="", validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Aufgabenbereich hinzufügen", "style": "margin-left:20px;"})
    submit = SubmitField('Hinzufügen', render_kw={"type": "image", "src": "static/Bilder/plus.svg", "style": "filter: invert(100%); width: 25px; height: 25px; margin-top: 5px;"})
