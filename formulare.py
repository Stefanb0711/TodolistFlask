from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

class AddTodoTaskForm(FlaskForm):
    new_todo = StringField('ToDo hinzufügen', validators=[DataRequired()])
    submit = SubmitField('Todo hinzufügen', render_kw={"type": "image", "src": "static/plus-circle.svg"})

class AddTodoAreaForm(FlaskForm):
    new_area = StringField("Aufgabenbereich hinzufügen", validators=[DataRequired()])
    submit = SubmitField('Hinzufügen', render_kw={"type": "image", "src": "static/plus-circle.svg"})
