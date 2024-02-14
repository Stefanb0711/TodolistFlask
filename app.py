from flask import Flask, render_template, redirect, url_for, request
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
todo_liste_elemente =[]

@app.route("/", methods=['GET', 'POST'])
def start():
    global todo_liste_elemente
    #Abfrage der Datenbak für schon vorhandene td-Bereiche
    todo_bereiche_query = TodoBereich.query.all()

    #for todo_bereich in todo_bereiche_query:
       # print(f"odobereichquery: {todo_bereich.todo_bereich_name}")


    todo_bereich_id = request.args.get("todo_bereich_id")
    todo_bereich_name = request.args.get("todo_bereich_name")

    #global todo_liste_elemente

    #todo_liste_elemente = []
    #todo_liste_elemente = request.args.get("todo_liste_elemente")
    for element in todo_liste_elemente:
        print(f"Todolisteelement: {element}")

    print(f"TodobereichId: {todo_bereich_id}")

    add_todo_task_form = AddTodoTaskForm()
    add_todo_area_form = AddTodoAreaForm()
    #Todo Element
    #if add_todo_task_form.validate_on_submit():
    if request.method == 'POST':
        new_todo = add_todo_task_form.new_todo.data

        todo_task = TodoListeElement(
            aufgabe=new_todo,
            todo_bereich_id = todo_bereich_id
            #Wird geändert

        )
        db.session.add(todo_task)
        db.session.commit()


        todo_liste.append(new_todo)
        todo_liste_elemente.append(new_todo)
        print(todo_liste_elemente)
        return redirect(url_for("start", todo_bereiche=todo_bereiche, todo_liste_elemente = todo_liste_elemente))

    #Todo Bereich
    #if add_todo_area_form.validate_on_submit():
    if request.method == "POST":

        new_area = add_todo_area_form.new_area.data

        todo_area = TodoBereich(
            todo_bereich_name=new_area
        )
        db.session.add(todo_area)
        db.session.commit()


        todo_bereiche.append(new_area)
        return redirect(url_for("start", todo_bereiche=todo_bereiche, todo_liste = todo_liste))

    return render_template("start.html", add_todo_task_form = add_todo_task_form,
                           todo_liste = todo_liste, add_todo_area_form = add_todo_area_form,
                           todo_bereiche=todo_bereiche, todo_bereiche_query=todo_bereiche_query, todo_liste_elemente = todo_liste_elemente, todo_bereich_name = todo_bereich_name)





# Keine sichtbaren Routes

@app.route("/todo-liste-einsehen/<int:todo_bereich_id>", methods=['GET', "POST"])
def todo_einsehen(todo_bereich_id):
    global todo_liste_elemente

    todo_bereich_name = request.args.get('todo_bereich_name')

    #print((f"TodobereichId: {todo_bereich_id}"))

    todo_bereich = TodoBereich.query.get(todo_bereich_id)
    print(f" TodoBereichName = {todo_bereich.todo_bereich_name}")

    todo_liste_für_id = TodoListeElement.query.filter_by(todo_bereich_id=todo_bereich.id).all()
    todo_liste_elemente = [element.aufgabe for element in todo_liste_für_id]

    for element in todo_liste_für_id:
        print(f"TodoListeFürId: {element}")



#todo_liste_laden = TodoListeElement.query.filter_by(todo_bereich_id = todo_bereich_id).all()
#print(todo_liste_laden)
    #for listenelement in todo_liste_laden:
        #print(listenelement.aufgabe)

    return redirect(url_for("start", todo_liste_elemente=todo_liste_elemente, todo_bereich_id=todo_bereich.id, todo_bereich_name = todo_bereich.todo_bereich_name))

    #return render_template("todo_einsehen.html", todo_liste_elemente = todo_liste_elemente)

"""@app.route("/todo-erledigt/<int:todo_id>", methods=["GET", "POST"])
def todo_erledigt(todo_id):
    #todo_id = request.args.get("todo_id")
    #print(f"Todoid = {todo_id}")

    return redirect(url_for("start"))"""

@app.route("/dropdown-button")
def dropdown_button():
    form = AddTodoAreaForm()
    task_form = AddTodoTaskForm()

    return render_template("todo_einsehen.html", form = form, add_todo_area_form = form, task_form = task_form, todo_liste_elemente = todo_liste_elemente)

if __name__ == '__main__':
    app.run(debug =True, port=5001)
