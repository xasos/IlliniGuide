from app import app, db, manager

manager.run()
#port = int(os.environ.get('PORT', 5000))
app.run(debug=True)
