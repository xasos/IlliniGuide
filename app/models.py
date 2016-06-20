from app import db

class searchtest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    role = db.Column(db.String(80), unique=False)

    def __init__(self, name, role):
        self.name = name
        self.role = role


#class User(db.Model):
#  id = db.Column(db.Integer, primary_key=True)
#  name = db.Column(db.String(100))
#  email = db.Column(db.String(100))
#  def __init__(self, name, email):
#    self.name = name
#    self.email = email
