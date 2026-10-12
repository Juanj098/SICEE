from app.extensions import db

class Investigador(db.Model):
    __tablename__ = "investigador"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)