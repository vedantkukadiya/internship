<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False, unique=True)
    short_code = db.Column(db.String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"<URL {self.short_code}>"
=======
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False, unique=True)
    short_code = db.Column(db.String(10), nullable=False, unique=True)

    def __repr__(self):
        return f"<URL {self.short_code}>"
>>>>>>> 1d7298a06682074386338a8b158f825bd1f6cb26
