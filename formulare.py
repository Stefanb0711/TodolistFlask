from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length

class AddTodoTaskForm(FlaskForm):
    new_todo = StringField('ToDo hinzufügen', validators=[DataRequired()], render_kw={"placeholder": "ToDo hinzufügen", "style": "margin-top:50px;", "class": "form-control"})
    submit = SubmitField('Todo hinzufügen', render_kw={"type": "image", "src":"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16'  fill='white' class='bi bi-plus' viewBox='0 0 16 16'%3E%3Cpath d='M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4'/%3E%3C/svg%3E", "style": "margin-top:53px; ", "class": "btn btn-primary"})

class AddTodoAreaForm(FlaskForm):
    new_area = StringField(label="", validators=[DataRequired(), Length(max=50)], render_kw={"placeholder": "Aufgabenbereich hinzufügen", "style": "margin-left:20px;"})
    submit = SubmitField('Hinzufügen', render_kw={"type": "image", "src": "static/Bilder/plus.svg", "style": "filter: invert(100%); width: 25px; height: 25px; margin-top: 5px;"})
