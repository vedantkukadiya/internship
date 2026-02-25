<<<<<<< HEAD
from flask import Flask, render_template, request

app = Flask(__name__)

notes = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form.get("note")

        if note:  # avoid None / empty values
            notes.append(note)

    return render_template("home.html", notes=notes)

if __name__ == "__main__":
    app.run(debug=True)
=======
from flask import Flask, render_template, request

app = Flask(__name__)

notes = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form.get("note")

        if note:  # avoid None / empty values
            notes.append(note)

    return render_template("home.html", notes=notes)

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 1d7298a06682074386338a8b158f825bd1f6cb26
