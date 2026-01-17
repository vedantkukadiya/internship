from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    username = request.args.get("name")

    if username:
        username_upper = username.upper()
        name_length = len(username)
        current_time = datetime.now().strftime("%I:%M %p")
    else:
        username_upper = None
        name_length = None
        current_time = None

    return render_template(
        "index.html",
        username=username_upper,
        length=name_length,
        time=current_time
    )

if __name__ == "__main__":
    app.run(debug=True)
