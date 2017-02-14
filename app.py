from flask import Flask, render_template, request
from form import RegistrationForm, LoginForm
from models import *

app = Flask(__name__)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)
    new_user = User()
    if request.method == 'POST' and form.validate():
        form.populate_obj(new_user)
        new_user.save()
        return "success"
    return render_template("register.html", form_register=form)

@app.route("/login", methods=['POST', 'GET'])
@def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():





if __name__ == "__main__":
    connect('socialgram')
    app.run()