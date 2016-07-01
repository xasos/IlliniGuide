from app import app, db

db.create_all()
db.session.commit()
#port = int(os.environ.get('PORT', 5000))
app.run(debug=True)
