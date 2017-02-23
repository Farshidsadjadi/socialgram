from flask import Flask, Blueprint, render_template, request
from project.apps.auth.form import RegistrationForm, LoginForm
from project.apps.auth.models import *

mod = Blueprint('store', __name__, url_prefix='/store')


@mod.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)
    new_user = User()
    if request.method == 'POST' and form.validate():
        form.populate_obj(new_user)
        new_user.save()
        return "success"
    return render_template("register.html", form_register=form)

@mod.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = User.userexist(email)
        print "Hi %s" % user.firstname


    return render_template("login.html",form_login=form)
