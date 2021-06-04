from App import db

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(), nullable=False)
    file = db.Column(db.LargeBinary(), nullable=False)