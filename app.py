from flask import Flask, render_template, request
from form import RegistrationForm
from models import *
from flask_mongoengine import MongoEngine
app = Flask(__name__)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        return "success"
    return render_template("register.html", form_register=form)

@app.route("/test", methods=['POST', 'GET'])
def hello():
    hasError = False
    fields = {
        "firstname": {
            "error": "",
            "val": None
        },
        "lastname": {
            "error": "",
            "val": None
        },
        "username": {
            "error": "",
            "val": None
        },
        "password": {
            "error": "",
            "val": None
        },
        "cpassword": {
            "error": "",
            "val": None
        },
        "age": {
            "error": "",
            "val": None
        },
        "email": {
            "error": "",
            "val": None
        },
    }
    if request.method == "POST":
        fields["firstname"]["val"] = request.form.get("firstname")
        fields["lastname"]["val"] = request.form.get("lastname")
        fields["username"]["val"] = request.form.get("username")
        fields["password"]["val"] = request.form.get("password")
        fields["cpassword"]["val"] = request.form.get("cpassword")
        fields["age"]["val"] = request.form.get("age")
        fields["email"]["val"] = request.form.get("email")
        if fields["password"]["val"] != fields["cpassword"]["val"]:
            fields["cpassword"]["error"] = "Password Not Matched!"
            hasError = True

        for field in fields:
            if fields[field]["val"] == "":
                fields[field]["error"] = "pleas fill {0}".format(field)
                hasError = True
        if hasError == False:
            user.insert_one({
                "firstname": fields["firstname"]["val"],
                "lastname": fields["lastname"]["val"],
                "username": fields["username"]["val"],
                "password": fields["password"]["val"],
                "age": fields["age"]["val"],
                "email": fields["email"]["val"]
            })
            return "success :)"


    return render_template("register2.html", fields=fields)



if __name__ == "__main__":
    connect('socialgram')
    app.run()