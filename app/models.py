from app import db
from operator import itemgetter

class Search(db.Model):
    __table__ = db.Model.metadata.tables['Search']
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80), unique=True)
    #role = db.Column(db.String(80), unique=False)

    def autosearch(querystring, dept=""):
        if dept == "":
            query = db.session.query(Search).filter(Search.name0.ilike('%' + str(querystring) + '%'))\
                    .order_by(Search.hits.desc())
            query2 = db.session.query(Search).filter(Search.name1.ilike('%' + str(querystring) + '%'))\
                    .order_by(Search.hits.desc())
        else:
            query = db.session.query(Search).filter(Search.role.in_(["class", "professor"])).filter(Search.dept==dept)\
                    .filter(Search.name0.ilike('%' + str(querystring) + '%')).order_by(Search.hits.desc())
            query2 = db.session.query(Search).filter(Search.role.in_(["class", "professor"])).filter(Search.dept==dept)\
                    .filter(Search.name1.ilike('%' + str(querystring) + '%')).order_by(Search.hits.desc())
        results = []
        results2 = []
        for mv in query:
            results.append((mv.name0, mv.hits))
        for mv in query2:
            results.append((mv.name1, mv.hits))
        results = sorted(results, key=itemgetter(1), reverse=True)
        for mv in results:
            results2.append(mv[0])
        return results2

class Reviews(db.Model):
    __table__ = db.Model.metadata.tables['Reviews']

class Metrics(db.Model):
    __table__ = db.Model.metadata.tables['Metrics']

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
