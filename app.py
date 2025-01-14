from flask import Flask, render_template, redirect, url_for, request, flash
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
    todo_bereich_symbol = db.Column(db.String, nullable= False)
    todo_liste_element = db.relationship("TodoListeElement", back_populates="todo_bereich", cascade='all, delete-orphan')

class TodoListeElement(db.Model):
    __tablename__ = "todo_liste_element"
    id = db.Column(db.Integer, primary_key=True)
    aufgabe = db.Column(db.String, nullable=False)
    unerledigt = db.Column(db.Boolean, nullable=False, default = True)
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
    neue_todo_area_id = len(todo_bereiche_query)



    #Bereich der evtl gelöscht wird
    todo_id = request.args.get('todo_id')

    if not todo_id == None:
        neue_erledigte_todo = db.session.query(TodoListeElement).filter(TodoListeElement.id == todo_id).first()
        neue_erledigte_todo.unerledigt = False
        db.session.commit()


    todo_bereich_id = request.args.get("todo_bereich_id")
    print(f"TodoBereichid = {todo_bereich_id}")
    todo_bereich_name = request.args.get("todo_bereich_name")

    todo_liste_für_id = TodoListeElement.query.filter_by(todo_bereich_id=todo_bereich_id).all()

    todo_liste_für_id_unerledigt = [todo for todo in todo_liste_für_id if todo.unerledigt]

    todo_liste_für_id_erledigt = [todo for todo in todo_liste_für_id if not todo.unerledigt]

    erledigte_todos = request.args.get("erledigte_todos")
    if erledigte_todos == None:
        erledigte_todos = []

    print(f"Erledigte Todos: {todo_liste_für_id_erledigt}")


    icon_url = request.args.get('icon_url')
    if icon_url is None:
        icon_url = 'Bilder/list-task.svg'

    bereich_id_geändertes_icon = request.args.get("bereich_id_geändertes_icon")
    if bereich_id_geändertes_icon is None:
        bereich_id_geändertes_icon = 1

    print(f"Icon Url: {icon_url} und Bereichid: {bereich_id_geändertes_icon}")



    #if request.args.get("todo_liste_für_id") is None:
     #   todo_liste_für_id = []




    #global todo_liste_elemente

    #todo_liste_elemente = []
    #todo_liste_elemente = request.args.get("todo_liste_elemente")






    add_todo_task_form = AddTodoTaskForm()
    add_todo_area_form = AddTodoAreaForm()
    #Todo Element
    #if add_todo_task_form.validate_on_submit():
    if add_todo_task_form.validate_on_submit():
            new_todo = add_todo_task_form.new_todo.data
    
            todo_task = TodoListeElement(
                aufgabe=new_todo,
                todo_bereich_id = todo_bereich_id
                #Wird geändert
    
            )
            db.session.add(todo_task)
            db.session.commit()
    
    
            #todo_liste.append(new_todo)
            #todo_liste_elemente.append(new_todo)
            #print(todo_liste_elemente)
            return redirect(url_for("start", todo_bereich_id = todo_bereich_id))


    #Todo Bereich
    #if add_todo_area_form.validate_on_submit():
    if request.method == "POST" :

        #Checken wieviele Todobereiche es gibt. Bei 15 eine Fehlermeldung ausgeben
        todo_bereiche_query = TodoBereich.query.all()
        if len(todo_bereiche_query) >= 20:
            flash("Sie können kein TodoBereich mehr hinzufügen", "error")
            return redirect(url_for("dropdown_button"))



        new_area = add_todo_area_form.new_area.data

       # print(f"New Area Id: {new_area.id}")

        todo_area = TodoBereich(
            todo_bereich_name=new_area,
            todo_bereich_symbol= icon_url
        )
        db.session.add(todo_area)
        db.session.commit()

        neuste_todo_area = TodoBereich.query.filter_by(todo_bereich_name=new_area).first()

        #icon_url = request.args.get("icon_url")

        #print(f"New Area TodoBereichId {neuste_todo_area.id}")
        #todo_bereiche.append(new_area)
        todo_bereiche_query = TodoBereich.query.all()

        neue_todo_area_id = len(todo_bereiche_query)
        neuste_todo_area = TodoBereich.query.filter_by(id=neue_todo_area_id).first()
        print(f"Neuste Todoarea: {neuste_todo_area.todo_bereich_name}")

        #print(neue_todo_area_id)
        #neue_todo_area_id += 1

        return redirect(url_for("start", todo_bereiche_query=todo_bereiche_query,
                                neuste_todo_area = neuste_todo_area,neue_todo_area_id = neue_todo_area_id))


    return render_template("start.html", add_todo_task_form = add_todo_task_form,
                           todo_liste = todo_liste, add_todo_area_form = add_todo_area_form,
                           todo_bereiche=todo_bereiche, todo_bereiche_query=todo_bereiche_query, todo_liste_elemente = todo_liste_elemente, todo_bereich_name = todo_bereich_name,
                           todo_liste_für_id=todo_liste_für_id, icon_url=icon_url, bereich_id_geändertes_icon=bereich_id_geändertes_icon,
                           todo_bereich_id = todo_bereich_id, erledigte_todos = erledigte_todos, todo_liste_für_id_erledigt = todo_liste_für_id_erledigt,
                           todo_liste_für_id_unerledigt = todo_liste_für_id_unerledigt)



# Keine sichtbaren Routes

@app.route("/todo-liste-einsehen/<int:todo_bereich_id>", methods=['GET', "POST"])
def todo_einsehen(todo_bereich_id):
    global todo_liste_elemente

    todo_bereich_name = request.args.get('bereich_name')

    todo_bereich_id = todo_bereich_id
    #print((f"TodobereichId: {todo_bereich_id}"))

    todo_bereich = TodoBereich.query.get(todo_bereich_id)

    print(f" TodoBereichName = {todo_bereich.todo_bereich_name}")

    #todo_liste_für_id = TodoListeElement.query.filter_by(todo_bereich_id=todo_bereich.id).all()
    #todo_liste_elemente = [element.aufgabe for element in todo_liste_für_id]



    return redirect(url_for("start", todo_bereich_id=todo_bereich_id,
                            todo_bereich_name = todo_bereich.todo_bereich_name,
                            todo_liste_elemente = todo_liste_elemente))

    #return render_template("todo_einsehen.html", todo_liste_elemente = todo_liste_elemente)

@app.route("/todo-erledigt/<int:todo_id>", methods=["GET", "POST"])
def todo_erledigt(todo_id):

    todo_bereich_id = request.args.get('todo_bereich_id')

    neue_erledigte_todo = db.session.query(TodoListeElement).filter(TodoListeElement.id == todo_id).first()
    neue_erledigte_todo.unerledigt = False
    db.session.commit()

    #Erledigte Todos finden
    erledigte_todos = db.session.query(TodoListeElement).filter(TodoListeElement.todo_bereich_id == todo_bereich_id, TodoListeElement.unerledigt == False).all()


    return redirect(url_for("start", erledigte_todos = erledigte_todos))

@app.route("/dropdown-button")
def dropdown_button():
    todo_bereiche_query = TodoBereich.query.all()

    print(f"Länge Todobereiche{len(todo_bereiche_query)}")

    letzter_bereich_id = len(todo_bereiche_query)

    #icon_url = "Bilder/stars.svg"

    icon_url = request.args.get("icon_url")

    if icon_url is None:
        icon_url = "Bilder/stars.svg"


    print(f"{icon_url}")

    #if icon_url is N

    return render_template("todo_einsehen.html", todo_bereiche_query = todo_bereiche_query, icon_url = icon_url, letzter_bereich_id = letzter_bereich_id)



@app.route("/post-löschen/<int:bereich_id>")
def todo_bereich_löschen(bereich_id):

    zu_löschender_todo_bereich = TodoBereich.query.get(bereich_id)
    print(f"Zu löschender Todobereich: {zu_löschender_todo_bereich}")
    db.session.delete(zu_löschender_todo_bereich)
    db.session.commit()

    return redirect(url_for("start"))

@app.route("/todo-löschen/<int:todo_id>")
def todo_löschen(todo_id):

    todo_bereich_id = request.args.get("todo_bereich_id")

    zu_löschende_todo_aufgabe = TodoListeElement.query.get(todo_id)
    db.session.delete(zu_löschende_todo_aufgabe)
    db.session.commit()

    return redirect(url_for("todo_einsehen", todo_bereich_id=todo_bereich_id))

@app.route("/bereich-markierung-ändern/<int:bereich_id>")
def bereich_markierung_ändern(bereich_id):

    print(f"BereichMarkierungÄndern bereichid: {bereich_id}")

    icon_url = request.args.get('icon_url')

    print(icon_url)

    return redirect(url_for("start", bereich_id_geändertes_icon = bereich_id, icon_url = icon_url))


if __name__ == '__main__':
    app.run(debug =True, port=5001)
