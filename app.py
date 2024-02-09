from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from formulare import AddTodoTaskForm, AddTodoAreaForm
from flask_bootstrap import Bootstrap5
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = 'geheimeschluessel'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db.init_app(app)

class TodoBereich(db.Model):
    __tablename__ = "todo_bereich"
    id = db.Column(db.Integer, primary_key=True)
    todo_bereich_name = db.Column(db.String, nullable=False)
    todo_liste_element = db.relationship("TodoListeElement", back_populates="todo_bereich")

class TodoListeElement(db.Model):
    __tablename__ = "todo_liste_element"
    id = db.Column(db.Integer, primary_key=True)
    aufgabe = db.Column(db.String, nullable=False)
    todo_bereich_id = db.Column(db.Integer, db.ForeignKey("todo_bereich.id"), nullable=False)
    todo_bereich = db.relationship("TodoBereich", back_populates="todo_liste_element")

with app.app_context():
    db.create_all()

"""@app.route('/')
def start():  
    return render_template("start_andere_version.html")"""

todo_bereiche = []
todo_liste = []

@app.route("/", methods=['GET', 'POST'])
def start():
    #todo_bereiche_query = TodoBereich.query.all()
    #print(todo_bereiche_query.todo_bereich_name)
    add_todo_task_form = AddTodoTaskForm()
    add_todo_area_form = AddTodoAreaForm()
    #Todo Element
    if add_todo_task_form.validate_on_submit():
        new_todo = add_todo_task_form.new_todo.data

        todo_task = TodoListeElement(
            aufgabe=new_todo,
            todo_bereich_id = 1
            #Wird geändert

        )
        db.session.add(todo_task)
        db.session.commit()
        print(todo_task.aufgabe)

        todo_liste.append(new_todo)
        print(new_todo)
        return redirect(url_for("start", todo_bereiche=todo_bereiche, todo_liste = todo_liste))

    #Todo Bereich
    if add_todo_area_form.validate_on_submit():

        new_area = add_todo_area_form.new_area.data

        todo_area = TodoBereich(
            todo_bereich_name=new_area
        )
        db.session.add(todo_area)
        db.session.commit()


        todo_bereiche.append(new_area)
        return redirect(url_for("start", todo_bereiche=todo_bereiche, todo_liste = todo_liste))

    return render_template("start.html", add_todo_task_form = add_todo_task_form, todo_liste = todo_liste, add_todo_area_form = add_todo_area_form, todo_bereiche=todo_bereiche)

@app.route("/add-to-do", methods=['GET', 'POST'])
def add_to_do():

    return render_template("start_andere_version.html")


@app.route("/todo-liste-einsehen/<int:todo_bereich_id>", methods=['GET', 'POST'])
def todo_einsehen(todo_bereich_id):



    return render_template("start.html")

if __name__ == '__main__':
    app.run(debug =True, port=5001)
