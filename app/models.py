from app import db

class Search(db.Model):
    __table__ = db.Model.metadata.tables['Search']
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80), unique=True)
    #role = db.Column(db.String(80), unique=False)

class Reviews(db.Model):
    __table__ = db.Model.metadata.tables['Reviews']

#    def __init__(self, name0, name1, role):
#        self.name = name
#        self.role = role
#
#class tester(db.Model):
#    __table__ = db.Model.metadata.tables['tester']
#
#    def __repr__(self):
#        return self.DISTRICT


#class User(db.Model):
#  id = db.Column(db.Integer, primary_key=True)
#  name = db.Column(db.String(100))
#  email = db.Column(db.String(100))
#  def __init__(self, name, email):
#    self.name = name
#    self.email = email
