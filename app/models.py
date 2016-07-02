from app import db, meta, engine, login_serializer
import os, base64, hashlib
from operator import itemgetter
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSONB
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin

''' Deliverables '''

Search = db.Table('Search', meta, autoload=True, autoload_with=engine)
Metrics = db.Table('Metrics', meta, autoload=True, autoload_with=engine)
Reviews = db.Table('Reviews', meta, autoload=True, autoload_with=engine)

class Search(db.Model):
    __tablename__ = "Search"


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
    __tablename__ = "Reviews"

class UserReviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    professor = db.Column(db.Text(), nullable=False)
    classname = db.Column(db.Text(), nullable=False)
    comments = db.Column(db.Text(), nullable=False)
    profdifficulty = db.Column(db.Numeric(), nullable=False)
    classdifficulty = db.Column(db.Numeric(), nullable=False)
    quality = db.Column(db.Numeric(), nullable=False)
    date = db.Column(db.Date(), nullable=False)

class Metrics(db.Model):
    __tablename__ = 'Metrics'


''' Users and Authentication '''

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    #SSO = db.Column(db.Boolean(), nullable=False)
    password = db.Column(db.LargeBinary())
    cookies = db.relationship('Cookie', backref='User', lazy='dynamic')
    #data = db.Column(JSONB)
    reviews = db.relationship('UserReviews', backref='User', lazy='dynamic')

    def get_auth_token(self):
        selector = os.urandom(16)
        validator = os.urandom(64)
        data = [base64.b64encode(selector).decode("utf-8"), base64.b64encode(validator).decode("utf-8")]
        db.session.add(Cookie(user_id = self.id, selector = selector, validator = hashlib.sha256(validator).digest()))
        db.session.commit()
        return login_serializer.dumps(data)

    #@staticmethod
    #def get(userid):
    #    return db.session.query(models.User).filter(models.User.id==userid).one_or_none()

class Cookie(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    selector = db.Column(db.LargeBinary())
    validator = db.Column(db.LargeBinary())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class GoogleOAuth(db.Model, OAuthConsumerMixin):
    __tablename__ = "flask_dance_googleoauth"
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)

class FacebookOAuth(db.Model, OAuthConsumerMixin):
    __tablename__ = "flask_dance_facebookoauth"
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
