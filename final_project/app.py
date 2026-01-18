from flask import Flask, render_template, request, redirect, abort
from models import db, URL
from urllib.parse import urlparse
import random
import string

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------------- FUNCTIONS ----------------

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def normalize_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url


def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc


# ---------------- ROUTES ----------------

@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    error = None

    if request.method == "POST":
        long_url = request.form.get("url", "").strip()
        long_url = normalize_url(long_url)

        if not is_valid_url(long_url):
            error = "Please enter a valid URL (must start with http:// or https://)"
            return render_template("home.html", data=None, error=error)

        # Check existing URL
        existing = URL.query.filter_by(long_url=long_url).first()
        if existing:
            short_url = existing.short_code
        else:
            while True:
                short_code = generate_short_code()
                if not URL.query.filter_by(short_code=short_code).first():
                    break

            new_url = URL(long_url=long_url, short_code=short_code)
            db.session.add(new_url)

            try:
                db.session.commit()
                short_url = short_code
            except:
                db.session.rollback()
                error = "Something went wrong. Try again."

    return render_template("home.html", data=short_url, error=error)


@app.route("/history")
def history():
    urls = URL.query.order_by(URL.id.desc()).all()
    return render_template("history.html", urls=urls)


@app.route("/<short_code>")
def redirect_to_original(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if not url:
        abort(404)

    return redirect(url.long_url)


if __name__ == "__main__":
    app.run(debug=True)
