from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary in-memory storage
notes = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        note = request.form.get("note")

        # validation
        if note and note.strip():
            notes.append(note.strip())

        # POST-REDIRECT-GET pattern (important)
        return redirect(url_for("home"))

    return render_template("index.html", notes=notes)

if __name__ == "__main__":
    app.run(debug=True)
